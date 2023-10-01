#!/bin/bash

kubectl port-forward service/crnn 10001:10001 &
kubectl port-forward service/dbnet 10000:10000 &
kubectl port-forward service/libretranslate-svc 5000:5000 &
kubectl port-forward service/ocr-minio 9000:9000 &
kubectl port-forward service/ocr-minio 9200:9200 &

