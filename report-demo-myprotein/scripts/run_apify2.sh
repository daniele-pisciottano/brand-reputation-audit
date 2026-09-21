#!/bin/zsh
TOKEN=$(cat ~/.config/apify_token)
R=~/Documents/output/myprotein-2026-09-21/raw
run(){ curl -s -X POST "https://api.apify.com/v2/acts/$1/run-sync-get-dataset-items?token=$TOKEN&format=json&timeout=600" -H "Content-Type: application/json" -d "$2" -o "$R/$3"; echo "$3 $(python3 -c "import json;print(len(json.load(open('$R/$3'))))" 2>&1)"; }
run apify~instagram-scraper '{"directUrls":["https://www.instagram.com/myproteinit/"],"resultsType":"posts","resultsLimit":50,"addParentData":false}' instagram_posts.json &
run clockworks~tiktok-comments-scraper "{\"postURLs\":$(cat ~/Documents/output/myprotein-2026-09-21/tiktok_top_urls.json),\"commentsPerPost\":30}" tiktok_comments.json &
wait
