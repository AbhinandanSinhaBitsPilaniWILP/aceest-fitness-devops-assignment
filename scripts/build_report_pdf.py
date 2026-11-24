"""Render REPORT.md as a submission-ready PDF with readable tables and links."""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "REPORT.md"
OUTPUT = ROOT / "outputs" / "DevOps_Assignment_Final_Report.pdf"


def inline_markup(text: str) -> str:
    text = html.escape(text, quote=False)

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        url = match.group(2)
        return f'<link href="{html.escape(url, quote=True)}" color="#0d7490"><u>{label}</u></link>'

    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    return text.replace("  ", "<br/>")


class ReportDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=20 * mm,
            bottomMargin=18 * mm,
            title="ACEest Fitness DevOps Assignment Report",
            author="Abhinandan Sinha",
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates([report_page_template(frame)])


def report_page_template(frame: Frame):
    from reportlab.platypus import PageTemplate

    def decorate(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D8E2EA"))
        canvas.setLineWidth(0.5)
        canvas.line(document.leftMargin, 13 * mm, A4[0] - document.rightMargin, 13 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#607080"))
        canvas.drawString(document.leftMargin, 8 * mm, "ACEest Fitness DevOps Assignment")
        canvas.drawRightString(A4[0] - document.rightMargin, 8 * mm, f"Page {document.page}")
        canvas.restoreState()

    return PageTemplate(id="report", frames=[frame], onPage=decorate)


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=colors.HexColor("#0D5B6E"), alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle(name="ReportSubtitle", parent=styles["Normal"], fontSize=9.5, leading=13, textColor=colors.HexColor("#607080"), alignment=TA_CENTER, spaceAfter=14))
    styles.add(ParagraphStyle(name="H2Report", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#0D5B6E"), spaceBefore=12, spaceAfter=6, keepWithNext=True))
    styles.add(ParagraphStyle(name="H3Report", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=colors.HexColor("#183A4A"), spaceBefore=8, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle(name="BodyReport", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=colors.HexColor("#182230"), spaceAfter=6))
    styles.add(ParagraphStyle(name="BulletReport", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.1, leading=12.5, leftIndent=12, firstLineIndent=-7, bulletIndent=0, spaceAfter=3))
    styles.add(ParagraphStyle(name="SmallReport", parent=styles["BodyText"], fontSize=8, leading=10, textColor=colors.HexColor("#607080"), spaceAfter=4))
    styles.add(ParagraphStyle(name="TableHeaderReport", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.3, leading=9, textColor=colors.white))
    styles.add(ParagraphStyle(name="TableBodyReport", parent=styles["BodyText"], fontSize=7.2, leading=9, textColor=colors.HexColor("#182230")))
    styles.add(ParagraphStyle(name="CodeReport", parent=styles["Code"], fontName="Courier", fontSize=7.4, leading=9.2, leftIndent=6, rightIndent=6, backColor=colors.HexColor("#F3F6F8"), borderColor=colors.HexColor("#D8E2EA"), borderWidth=0.5, borderPadding=6))
    return styles


def build() -> Path:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    doc = ReportDocTemplate(str(OUTPUT))
    story = []
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    i = 0
    first_title = True
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 2))
            i += 1
            continue
        if line.startswith("~~~"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("~~~"):
                code.append(lines[i])
                i += 1
            story.append(Preformatted("\n".join(code), styles["CodeReport"]))
            i += 1
            continue
        if line.startswith("| "):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                if not all(set(cell) <= {"-", ":", " "} for cell in row):
                    rows.append(row)
                i += 1
            if rows:
                width = len(rows[0])
                data = []
                for row_index, row in enumerate(rows):
                    row += [""] * (width - len(row))
                    style_name = "TableHeaderReport" if row_index == 0 else "TableBodyReport"
                    data.append([Paragraph(inline_markup(cell), styles[style_name]) for cell in row[:width]])
                table = Table(data, colWidths=[doc.width / width] * width, repeatRows=1, hAlign="LEFT")
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0D7490")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6F8")]),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D8E2EA")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]))
                story.extend([Spacer(1, 4), table, Spacer(1, 6)])
            continue
        if line.startswith("# "):
            title = inline_markup(line[2:])
            story.append(Paragraph(title, styles["ReportTitle"] if first_title else styles["H2Report"]))
            first_title = False
        elif line.startswith("## "):
            story.append(Paragraph(inline_markup(line[3:]), styles["H2Report"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), styles["H3Report"]))
        elif line.startswith("- ["):
            checked = line.startswith("- [x]")
            content = line[5:] if checked else line[5:]
            story.append(Paragraph(("[x] " if checked else "[ ] ") + inline_markup(content), styles["BulletReport"], bulletText="•"))
        elif line.startswith("- "):
            story.append(Paragraph(inline_markup(line[2:]), styles["BulletReport"], bulletText="•"))
        elif re.match(r"^\d+\. ", line):
            content = re.sub(r"^\d+\. ", "", line)
            story.append(Paragraph(inline_markup(content), styles["BulletReport"], bulletText="•"))
        elif line == "---":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#D8E2EA"), spaceBefore=4, spaceAfter=8))
        else:
            story.append(Paragraph(inline_markup(line), styles["BodyReport"]))
        i += 1
    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(build())

