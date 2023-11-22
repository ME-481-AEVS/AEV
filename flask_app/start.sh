#!/usr/bin/env bash

sudo gunicorn --bind 0.0.0.0:80 --workers 3 run:app
