pipeline {
  agent any

  environment {
    // Add virtual environment path if using venv (optional)
    PYTHONPATH = "."
  }

  stages {
    stage('Clone Repository') {
      steps {
        echo 'Cloning Selenium Python test repo...'
        git url: 'https://github.com/KA1823/selenium_automation.git'
      }
    }

    stage('Set Up Environment') {
      steps {
        echo 'Installing Python dependencies...'
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Run Selenium Tests') {
      steps {
        echo 'Executing Selenium Python tests...'
        // Replace below command based on your test framework
        // For unittest:
        sh 'python -m unittest discover tests'
        // Or for pytest:
        // sh 'pytest tests/ --junitxml=reports/results.xml'
      }
    }

    stage('Publish Test Results') {
      when {
        expression { fileExists('reports/results.xml') }
      }
      steps {
        echo 'Publishing test results...'
        junit 'reports/results.xml'
      }
    }
  }

  post {
    always {
      echo 'Cleaning up...'
      // Optional: clean temp files, screenshots, etc.
    }
    failure {
      echo 'Build failed. Check test logs.'
    }
    success {
      echo 'Build and tests succeeded.'
    }
  }
}
