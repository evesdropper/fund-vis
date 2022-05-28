#!/bin/sh
cd src
python3 fund.py cron
cd ..
message=$(date '+%Y-%m-%d %H:%M:%S')
git add .
git commit -m "add entry at ${message}"
echo "cron commit at ${message}" >> cronlog.txt


