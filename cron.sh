#!/bin/sh
python3 src/fund.py cron

message=$(date '+%Y-%m-%d %H:%M:%S')
git add .
git commit -m "$message"
git subtree push --prefix src heroku main

echo "cron commit at ${message}" >> cronlog.txt

