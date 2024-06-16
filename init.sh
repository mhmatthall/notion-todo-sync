#!/bin/bash
# ---------
# Script to setup notionsync inside a Docker container
#     I'm using the official Python docker image
#     I've mapped /app to the repo containing the code on the server
#     This script is being cron'd by the host to run every minute

echo "------------------------------------------------"
echo "--------- $(date +"%T") -----------------------------"
echo "--------- Starting /app/init.sh ----------------"
echo "------------------------------------------------"


# Setup
apt-get update
/usr/local/bin/python -m pip install --upgrade pip
pip install requests
pip install python-dotenv

# Run
echo "--------- Running /app/notionsync.py -----------"
/usr/local/bin/python /app/notionsync.py


echo "------------------------------------------------"
echo "--------- $(date +"%T") -----------------------------"
echo "--------- Finished /app/init.sh ----------------"
echo "------------------------------------------------"