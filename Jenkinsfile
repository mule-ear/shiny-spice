pipeline {
    agent all
    stages {
        stage('build') {
            steps {
                sh -c 'gcc test.c -o test'
            }
        }
    }
}
