git add .
git commit -m "Almost Hourly Update"
git push origin main

fin=$(date '+%Y-%m-%d %H:%M:%S')
echo "update repo at ${fin}" >> cronlog.txt
