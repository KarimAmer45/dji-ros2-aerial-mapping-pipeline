pipeline {
  agent any
  options {
    timestamps()
  }
  stages {
    stage('Install') {
      steps {
        sh 'python3 -m pip install --user -e . pytest'
      }
    }
    stage('Test') {
      steps {
        sh 'python3 -m pytest -q'
      }
    }
    stage('Package sanity') {
      steps {
        sh 'python3 -m compileall src tests'
      }
    }
  }
}