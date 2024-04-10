#!/usr/bin/env bash

# sudo gunicorn --bind 0.0.0.0:80 --threads 3 --timeout 0 run:app
sudo gunicorn --bind 0.0.0.0:443 --threads 4 --certfile ssl/cert.pem --keyfile ssl/key.pem --timeout 0 run:app
