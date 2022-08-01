pipeline {
  agent {
    docker {
      image 'python:alpine3.7'
      args '-p 5000:5000'
    }

  }
  stages {
    stage('Build') {
      steps {
        echo 'Building..'
        sh 'apk add py3-pip'
        sh 'apk add --update alpine-sdk'
        sh 'pip install --upgrade pip setuptools wheel'
        sh 'apk add --update --no-cache g++ gcc libxml2-dev libxslt-dev python-dev libffi-dev  make'
        sh 'apk add --no-cache libressl-dev musl-dev libffi-dev'
        sh 'pip install -r requirements.txt'
        sh 'python ./netconf\\ menu/menu.py'
        sh 'python ./netconf\\ menu/tests.py &'
      }
    }

    stage('Test') {
      post {
        always {
          junit 'test-reports/*.xml'
        }

      }
      steps {
        echo "${env.NODE_NAME}"
        sh 'ls'
        sh 'ls ./netconf\\ menu/'
        sh 'pip install -r requirements.txt'
        sh 'python ./netconf\\ menu/tests.py'
      }
    }

    stage('Deploy') {
      steps {
        echo 'Deploying....'
      }
    }

  }
  environment {
    registry = 'antonpast/netconf'
    registryCredential = 'dockerhub'
    dockerImage = ''
  }
}