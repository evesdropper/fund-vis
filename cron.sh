#!/bin/sh
cd src
python3 fund.py cron
cd ..
message=$(date '+%Y-%m-%d %H:%M:%S')
git add .
git commit -m "add entry at ${message}"
git subtree push --prefix src heroku main

echo "cron commit at ${message}" >> /mnt/c/Users/Evelyn/Documents/tonk/fund-vis/cronlog.txt

