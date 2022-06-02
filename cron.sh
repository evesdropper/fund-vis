#!/bin/sh
cd /mnt/c/Users/Evelyn/Documents/tonk/fund-vis
cd src
python3 fund.py cron
cd ..
message=$(date '+%Y-%m-%d %H:%M:%S')
git add src/saved/fundv2.txt
git commit -m "add entry at ${message}"
echo "cron commit at ${message}" >> .cronlog.txt
cd src
python3 fund.py check

