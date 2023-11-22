#!/usr/bin/env bash

# sudo gunicorn --bind 0.0.0.0:80 --threads 3 --timeout 0 run:app
sudo gunicorn --bind 0.0.0.0:443 --threads 3 --certfile ssl/server.pem --keyfile ssl/server.key --timeout 0 run:app
