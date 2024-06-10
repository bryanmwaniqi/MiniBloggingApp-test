pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                    docker version
                    docker compose version
                    docker compose -f docker-compose.test.yml up --build -d
                  '''
            }
        }
        stage('Test') {
            steps {
                sh 'docker exec -t test1api pytest'
                echo 'testcomplete'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
    post {
        always {
            sh 'docker compose down -v'
        }
    }
}