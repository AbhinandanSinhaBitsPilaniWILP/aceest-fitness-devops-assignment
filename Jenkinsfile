pipeline {
    agent { label 'linux-python-docker' }

    options {
        timestamps()
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
    }

    parameters {
        string(name: 'IMAGE_TAG', defaultValue: '', description: 'Optional image tag; defaults to build number')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: false, description: 'Push the image using the configured Docker Hub credential')
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Deploy to the configured Kubernetes context')
        choice(name: 'DEPLOYMENT_STRATEGY', choices: ['rolling', 'blue-green', 'canary', 'shadow', 'ab'], description: 'Kubernetes delivery strategy')
    }

    environment {
        IMAGE_NAME = "${env.DOCKERHUB_NAMESPACE ?: 'your-dockerhub-user'}/aceest-fitness"
        IMAGE_TAG = "${params.IMAGE_TAG ?: "build-${env.BUILD_NUMBER}"}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install --disable-pip-version-check -r requirements-dev.txt'
            }
        }

        stage('Unit tests') {
            steps {
                sh '.venv/bin/python -m pytest --cov=src/aceest --cov-report=xml --cov-report=term-missing'
            }
            post {
                always {
                    junit testResults: 'test-results.xml', allowEmptyResults: true
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Quality') {
            steps {
                sh '.venv/bin/ruff check src tests scripts'
                withSonarQubeEnv('sonarqube') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build --tag "$IMAGE_NAME:$IMAGE_TAG" --tag "$IMAGE_NAME:latest" .'
            }
        }

        stage('Push image') {
            when {
                expression { return params.PUSH_IMAGE }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USER" --password-stdin'
                    sh 'docker push "$IMAGE_NAME:$IMAGE_TAG"'
                    sh 'docker push "$IMAGE_NAME:latest"'
                }
            }
        }

        stage('Deploy') {
            when {
                expression { return params.DEPLOY }
            }
            steps {
                sh 'bash deploy/k8s/scripts/deploy.sh "$DEPLOYMENT_STRATEGY" "$IMAGE_NAME:$IMAGE_TAG"'
            }
        }

        stage('Smoke test') {
            when {
                expression { return params.DEPLOY }
            }
            steps {
                sh 'bash deploy/k8s/scripts/smoke-test.sh'
            }
        }
    }

    post {
        failure {
            script {
                // rollback the last deployment when a post-deploy pipeline fails
                if (params.DEPLOY) {
                    sh 'kubectl rollout undo deployment/aceest-fitness --namespace aceest --ignore-not-found=true || true'
                }
            }
        }
        always {
            archiveArtifacts artifacts: 'coverage.xml,*.log', allowEmptyArchive: true
        }
    }
}

