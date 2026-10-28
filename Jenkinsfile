pipeline {
    agent any

    environment {
        DOCKER_REGISTRY_USER = 'nitin3cmy2k' 
        FRONTEND_IMAGE       = 'frontend'
        BACKEND_IMAGE        = 'backend'
        IMAGE_TAG            = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            parallel {
                stage('Build Frontend') {
                    steps {
                        script {
                            echo 'Building Frontend Docker Image...'
                            sh "docker build -t ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG} ./frontend"
                            sh "docker tag ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG} ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:latest"
                        }
                    }
                }
                stage('Build Backend') {
                    steps {
                        script {
                            echo 'Building FastAPI Backend Docker Image...'
                            sh "docker build -t ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG} ./backend"
                            sh "docker tag ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG} ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:latest"
                        }
                    }
                }
            }
        }

        stage('Push to Registry') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USER')]) {
                        sh "echo ${DOCKER_HUB_PASSWORD} | docker login -u ${DOCKER_HUB_USER} --password-stdin"
                        sh "docker push ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:latest"
                        sh "docker push ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -f k8s/mysql-deployment.yaml"
                    
                    sh "sed -i 's|${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:latest|${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG}|g' k8s/backend-deployment.yaml"
                    sh "kubectl apply -f k8s/backend-deployment.yaml"
                    
                    sh "sed -i 's|${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:latest|${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG}|g' k8s/frontend-deployment.yaml"
                    sh "kubectl apply -f k8s/frontend-deployment.yaml"
                }
            }
        }
    }

    post {
        always {
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:latest || true"
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:latest || true"
        }
    }
}

