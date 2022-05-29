git subtree push --prefix src heroku main

fin=$(date '+%Y-%m-%d %H:%M:%S')
echo "update app at ${fin}" >> cronlog.txt
