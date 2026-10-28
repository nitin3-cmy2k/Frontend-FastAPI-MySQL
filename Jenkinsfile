pipeline {
    agent any

    environment {
        // Replace with your actual Docker Hub username
        DOCKER_REGISTRY_USER = 'nitin3cmy2k 
        DOCKER_HUB_USER= 'nitin3cmy2k'
        DOCKER_HUB_PASSWORD = 'shivshakti@#2026'         
        FRONTEND_IMAGE       = 'frontend'
        BACKEND_IMAGE        = 'backend'
        IMAGE_TAG            = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pulls code from your Git repository
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
                    echo 'Logging into Docker Hub and pushing images...'
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USER')]) {
                        sh "echo ${DOCKER_HUB_PASSWORD} | docker login -u ${DOCKER_HUB_USER} --password-stdin"
                        
                        // Push Frontend
                        sh "docker push ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:latest"
                        
                        // Push Backend
                        sh "docker push ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo 'Deploying application stack to VirtualBox K8s Cluster...'
                    
                    // 1. Deploy MySQL Database first
                    sh "kubectl apply -f k8s/mysql-deployment.yaml"
                    
                    // 2. Update and deploy FastAPI Backend
                    sh "sed -i 's|${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:latest|${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG}|g' k8s/backend-deployment.yaml"
                    sh "kubectl apply -f k8s/backend-deployment.yaml"
                    
                    // 3. Update and deploy Frontend
                    sh "sed -i 's|${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:latest|${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG}|g' k8s/frontend-deployment.yaml"
                    sh "kubectl apply -f k8s/frontend-deployment.yaml"
                }
            }
        }
        
        stage('Verify Deployment Status') {
            steps {
                echo 'Checking status of deployed components...'
                sh "kubectl get pods -o wide"
                sh "kubectl get services"
            }
        }
    }

    post {
        always {
            echo 'Cleaning up local runner Docker images to save space...'
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${FRONTEND_IMAGE}:latest || true"
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:${IMAGE_TAG} || true"
            sh "docker rmi ${DOCKER_REGISTRY_USER}/${BACKEND_IMAGE}:latest || true"
        }
    }
}

