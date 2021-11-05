    pipeline {
        agent any
        environment {
            DOCKER_HOST = '172.17.0.1'
        }
        stages {
            stage('clone') {
                steps {
                    git branch: "master",
                    credentialsId: "github",
                    url: "https://github.com/AlexUngerDev/mysite.git"
                }
            }
            stage('build') {
                steps {
                    sh 'echo version is $VERSION'
                    sh 'docker build -t alexunger/mysite:$VERSION .'
                }
            }
            stage('push') {
                steps {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
                        sh 'docker push alexunger/mysite:$VERSION'
                    }
                }
            }
        }
    }