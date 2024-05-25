pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                try {
                    sh 'docker compose -f docker-compose.test.yml up --build -d'
                } catch (e) {
                    echo 'Error: ${e.getMessage()}'
                } finally {
                    sh 'docker-compose stop'
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}