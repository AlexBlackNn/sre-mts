#!/bin/bash
helm install weather weather
helm install ingress-controller mts-ingress-nginx
helm install ingress mts-ingress