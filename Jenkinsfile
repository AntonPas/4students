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
        sh '''apk add py3-pip
'''
        sh 'apk add --update alpine-sdk'
        sh 'pip install --upgrade pip setuptools wheel'
        sh 'apk add --no-cache jpeg-dev zlib-dev libffi-dev'
        sh '''apk add --no-cache --virtual .build-deps build-base linux-headers 
   
'''
        sh '''apk add --update --no-cache         redis py3-paramiko
        py3-flask py3-jinja2         py3-markupsafe         py3-lxml '''
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