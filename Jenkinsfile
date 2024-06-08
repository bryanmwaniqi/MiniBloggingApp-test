pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh '''
                    docker info
                    docker version
                    docker compose version
                    curl --version
                  '''
                // sh 'docker exec -it test1api pytest'
            }
        }
        stage('Test') {
            steps {
                // sh 'docker exec -it test1api pytest'
                echo 'testcomplete'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}