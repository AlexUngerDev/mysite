pipeline {
    agent any
    environment {
        DOCKER_HOST = '172.17.0.1'
        VERSION=sh(returnStdout: true, script: '''grep 'version' package.json | cut -d '"' -f4 | head -n 1''')
    }
    stages {
        stage('clone') {
            steps {
                git branch: "main", credentialsId: 	"github", url: "https://github.com/AlexUngerDev/Node3-weather-website.git"
            }
        }
        stage('build') {
            steps {
                sh 'echo version is $VERSION'
                sh 'docker build -t alexunger/weatherwebsite:$VERSION .'
            }
        }
        stage('push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
                    sh 'docker push alexunger/weatherwebsite:$VERSION'
                }
            }
        }
        stage('create deployment and service') {
            steps {
                withKubeConfig([credentialsId: 'k3s-config']) {
                    sh 'kubectl create namespace weather'
                    sh 'kubectl apply -f deploy/weather-deployment.yaml'
                    sh 'kubectl apply -f deploy/weather-service.yaml'
                }

            }
        }
    }
}