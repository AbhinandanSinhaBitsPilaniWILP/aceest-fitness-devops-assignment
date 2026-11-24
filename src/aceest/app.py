"""Small Flask service for ACEest Fitness client and progress management."""

from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, current_app, g, jsonify, render_template, request


SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    goal TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    weight_kg REAL NOT NULL,
    workout_minutes INTEGER NOT NULL,
    notes TEXT NOT NULL DEFAULT '',
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
);
"""

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Create a configured ACEest Flask application."""

    project_root = Path(__file__).resolve().parents[2]
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config.from_mapping(
        DATABASE=str(Path(app.instance_path) / "aceest.db"),
        JSON_SORT_KEYS=True,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    with app.app_context():
        _init_db()

    @app.teardown_appcontext
    def close_database(_error: BaseException | None) -> None:
        database = g.pop("database", None)
        if database is not None:
            database.close()

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify(service="aceest-fitness", status="ok", version="1.0.0")

    @app.get("/api/clients")
    def list_clients():
        rows = get_db().execute(
            "SELECT id, name, email, goal, created_at FROM clients ORDER BY id"
        ).fetchall()
        return jsonify(clients=[dict(row) for row in rows])

    @app.post("/api/clients")
    def create_client():
        payload = request.get_json(silent=True) or {}
        name = str(payload.get("name", "")).strip()
        email = str(payload.get("email", "")).strip().lower()
        goal = str(payload.get("goal", "")).strip()
        if not name or not email:
            return jsonify(error="name and email are required"), 400
        if not EMAIL_PATTERN.match(email):
            return jsonify(error="email must be valid"), 400

        database = get_db()
        try:
            cursor = database.execute(
                "INSERT INTO clients (name, email, goal, created_at) VALUES (?, ?, ?, ?)",
                (name, email, goal, _utc_now()),
            )
            database.commit()
        except sqlite3.IntegrityError:
            return jsonify(error="email already exists"), 409

        row = database.execute(
            "SELECT id, name, email, goal, created_at FROM clients WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
        return jsonify(client=dict(row)), 201

    @app.get("/api/clients/<int:client_id>")
    def get_client(client_id: int):
        database = get_db()
        client_row = database.execute(
            "SELECT id, name, email, goal, created_at FROM clients WHERE id = ?",
            (client_id,),
        ).fetchone()
        if client_row is None:
            return jsonify(error="client not found"), 404
        progress_rows = database.execute(
            """SELECT id, client_id, weight_kg, workout_minutes, notes, recorded_at
               FROM progress WHERE client_id = ? ORDER BY id DESC""",
            (client_id,),
        ).fetchall()
        return jsonify(client=dict(client_row), progress=[dict(row) for row in progress_rows])

    @app.post("/api/clients/<int:client_id>/progress")
    def record_progress(client_id: int):
        database = get_db()
        client_exists = database.execute(
            "SELECT 1 FROM clients WHERE id = ?", (client_id,)
        ).fetchone()
        if client_exists is None:
            return jsonify(error="client not found"), 404

        payload = request.get_json(silent=True) or {}
        try:
            weight_kg = float(payload["weight_kg"])
            workout_minutes = int(payload["workout_minutes"])
        except (KeyError, TypeError, ValueError):
            return jsonify(error="weight_kg and workout_minutes are required"), 400
        if weight_kg < 0 or workout_minutes < 0:
            return jsonify(error="progress values must not be negative"), 400

        cursor = database.execute(
            """INSERT INTO progress
               (client_id, weight_kg, workout_minutes, notes, recorded_at)
               VALUES (?, ?, ?, ?, ?)""",
            (
                client_id,
                weight_kg,
                workout_minutes,
                str(payload.get("notes", "")).strip(),
                _utc_now(),
            ),
        )
        database.commit()
        row = database.execute(
            """SELECT id, client_id, weight_kg, workout_minutes, notes, recorded_at
               FROM progress WHERE id = ?""",
            (cursor.lastrowid,),
        ).fetchone()
        return jsonify(progress=dict(row)), 201

    return app


def get_db() -> sqlite3.Connection:
    """Return the request-scoped SQLite connection."""

    if "database" not in g:
        database = sqlite3.connect(Path(current_app.config["DATABASE"]))
        database.row_factory = sqlite3.Row
        database.execute("PRAGMA foreign_keys = ON")
        g.database = database
    return g.database


def _init_db() -> None:
    database = get_db()
    database.executescript(SCHEMA)
    database.commit()

