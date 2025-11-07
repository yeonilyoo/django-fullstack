pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'yeonilyoo'
        IMAGE_NAME = 'django-web'
        GIT_CREDENTIALS_ID = 'github_cred'
        DOCKER_CREDENTIALS_ID = 'docker_cred'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/yeonilyoo/django-fullstack.git',
                    credentialsId: "${GIT_CREDENTIALS_ID}"
            }
        }

        stage('Get Git Hash') {
            steps {
                script {
                    GIT_HASH = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    echo "Git Hash: ${GIT_HASH}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker-compose build"
                    sh "docker tag ${IMAGE_NAME}:latest ${DOCKER_REGISTRY}/${IMAGE_NAME}:${GIT_HASH}"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin ${DOCKER_REGISTRY}"
                        sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${GIT_HASH}"
                    }
                }
            }
        }

        stage('Update YAML with New Image Tag') {
            steps {
                script {
                    sh """
                        sed -i 's|image: yeonilyoo/django-web:.*|image: yeonilyoo/django-web:${GIT_HASH}|' k8s/05_web-deployment.yaml

                    """
                }
            }
        }

        stage('Commit & Push YAML Changes') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIALS_ID}", passwordVariable: 'GIT_PASS', usernameVariable: 'GIT_USER')]) {
                        sh """
                            git config user.name "Jenkins"
                            git config user.email "jenkins@example.com"
                            git fetch origin
                            git checkout -B deploy
                            git merge origin/master
                            git add k8s/05_web-deployment.yaml
                            git commit -m "Update image tag to ${GIT_HASH} [ci skip]"
                            git push https://${GIT_USER}:${GIT_PASS}@github.com/yeonilyoo/django-fullstack.git deploy
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            sh "docker logout ${DOCKER_REGISTRY}"
        }
    }
}
