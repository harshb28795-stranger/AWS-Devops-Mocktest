pipeline {
    agent any

    environment {
        APP_NAME = "aws-devops-mock-lab"
        ARTIFACT_DIR = "artifacts"
        ARTIFACT_NAME = "aws-devops-mock-lab.zip"
    }

    stages {

        stage('Checkout Source') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                sh '''
                    python3 --version
                    pip3 --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    pip3 install --user -r requirements.txt
                '''
            }
        }

        stage('Bandit Security Scan') {
            steps {
                sh '''
                    mkdir -p reports

                    bandit -r app -f txt -o reports/bandit-report.txt || true

                    cat reports/bandit-report.txt
                '''
            }
        }

        stage('Package Application') {
            steps {
                sh '''
                    rm -rf artifacts
                    mkdir -p artifacts

                    zip -r artifacts/aws-devops-mock-lab.zip \
                        app \
                        static \
                        instance \
                        run.py \
                        config.py \
                        requirements.txt \
                        README.md
                '''
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'artifacts/*.zip'
            }
        }

        stage('Deploy using Ansible') {
            steps {
                dir('ansible') {
                    sh '''
                        ansible-playbook deploy.yml
                    '''
                }
            }
        }
    }

    post {

        always {
            echo "Pipeline execution completed."
        }

        success {
            echo "Deployment completed successfully."
        }

        failure {
            echo "Pipeline failed."
        }
    }
}
