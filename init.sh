#!/bin/bash

apt-get update
/usr/local/bin/python -m pip install --upgrade pip
pip install requests
pip install python-dotenv

/usr/local/bin/python /app/notionsync.py