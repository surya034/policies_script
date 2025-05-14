pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/surya034/policies_script.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Inject .env File') {
            steps {
                withCredentials([file(credentialsId: 'ENV_FILE', variable: 'ENV_FILE_PATH')]) {
                    sh 'cp $ENV_FILE_PATH .env'
                }
            }
        }

        stage('Run Script') {
            steps {
                sh '''
                source venv/bin/activate
                python script.py
                '''
            }
        }
    }
}
