pipeline {
  agent {
    docker {
      args '-p 5000:5000'
      image 'alpine3.8'
    }

  }
  stages {
    stage('Build') {
      steps {
        echo 'Building..'
        sh 'apk add --update alpine-sdk'
        sh '''apk add --update --no-cache
        redis python3 py3-cffi py3-paramiko py3-flask py3-jinja2 py3-markupsafe py3-lxml'''
        sh 'python3 -m ensurepip'
        sh ' pip3 install -U pip'
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