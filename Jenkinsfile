    pipeline {
        agent any
        environment {
            DOCKER_HOST = '172.17.0.1'
            VERSION=sh(returnStdout: true, script: '''cat mysite/__init__.py | grep __version__ | cut -d '=' -f2 | cut -c 2- | cut -c -3''')
        }
        stages {
            stage('clone') {
                steps {
                    git branch: "master", credentialsId: 	"github", url: "https://github.com/AlexUngerDev/mysite.git"
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
            stage('create deployment and service') {
                steps {
                    withKubeConfig([credentialsId: 'k3s-config']) {
                        sh """#!/bin/bash
                        set -x
                        python3 -c "import sys;lines=sys.stdin.read();print (lines.replace('DOCKERTAG',str($VERSION)))" < deploy/deployment.yaml > deploy/deployment_ver.yaml
                        kubectl create namespace mysite || true
                        kubectl apply -f deploy/postgres-configmap.yaml
                        kubectl apply -f deploy/deployment_postgres.yaml
                        kubectl apply -f deploy/service_postgres.yaml
                        kubectl apply -f deploy/deployment_ver.yaml
                        kubectl apply -f deploy/service.yaml
                        """
                    }
                }
            }
        }
    }