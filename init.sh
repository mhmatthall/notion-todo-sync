#!/bin/bash

# I'm using notion-todo-sync inside a docker container so it needs some setup
#     I'm using the official Python docker image
#     I've mapped /app to the repo containing the code on the server
#
# Also, my server requires extra faff to get dockerfiles going so I'm just using this nasty shell script -- I don't care :))

apt-get update
/usr/local/bin/python -m pip install --upgrade pip
pip install requests
pip install python-dotenv

/usr/local/bin/python /app/notionsync.py
