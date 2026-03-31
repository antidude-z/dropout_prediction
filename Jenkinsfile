pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mlflow_pipeline:latest'
        MODEL_CONTAINER = 'ml_model'
        UI_CONTAINER = 'mlflow_ui'
    }

    stages {
        stage('Download') {
            steps {
                echo 'Downloading repository...'
                git url: 'https://github.com/antidude-z/dropout_prediction.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME} -f ./docker/Dockerfile --build-arg LIGHTWEIGHT=${params.LIGHTWEIGHT} ."
            }
        }

        stage('Clean + Train') {
            steps {
                echo 'Retraining all models...'
                sh "./docker/scripts/train.sh"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying best model with mlflow models serve...'
                sh "./docker/scripts/deploy.sh"
            }
        }

        stage('Health Check') {
            steps {
                echo 'Running health check...'
                sh "docker exec ${MODEL_CONTAINER} python -u /app/health_check.py"
            }
        }
    }

    post {
        success {
            script {
                sh "./docker/scripts/serve_ui.sh"
            }
        }
    }
}
