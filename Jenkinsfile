pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    try {
                        sh 'docker compose -f docker-compose.test.yml up --build -d'
                    } catch (e) {
                        echo 'Error: ${e.getMessage()}'
                    } finally {
                        sh 'docker-compose stop'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                sh 'docker exec -it test1api pytest'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}