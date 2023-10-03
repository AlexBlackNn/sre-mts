#!/bin/bash

minikube start --container-runtime=containerd --cpus 4 --memory 9000

ingress_enable=$(minikube addons list  | grep ingress | grep enable | wc -l)

if [ ${ingress_enable} -gt 0 ]; then
  echo "ingress is already enable."
else
  echo "install ingress"
  minikube addons enable ingress
fi


helm install weather weather
helm install ingress ingress