    pipeline {
        agent any
        environment {
            DOCKER_HOST = '172.17.0.1'
            VERSION=sh(returnStdout: true, script: '''cat mysite/__init__.py | grep __version__ | cut -d '=' -f2 | cut -c 2- | cut -c -3''')
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
                    sh 'sudo docker build --network common -t alexunger/mysite:$VERSION .'
                }
            }
            stage('push') {
                steps {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'sudo docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
                        sh 'sudo docker push alexunger/mysite:$VERSION'
                    }
                }
            }
        }
    }