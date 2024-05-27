pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker run python:3.6-alpine'
                echo 'testcomplete'
            }
        }
        stage('Test') {
            steps {
                echo 'success'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}