#!/bin/sh
python src/fund.py cron

message=$(date '+%Y-%m-%d %H:%M:%S')
git add .
git commit -m "$message"
git subtree push --prefix src heroku main
