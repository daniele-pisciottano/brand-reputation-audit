#!/bin/zsh
TOKEN=$(cat ~/.config/apify_token)
R=~/Documents/output/myprotein-2026-09-21/raw
run(){ curl -s -X POST "https://api.apify.com/v2/acts/$1/run-sync-get-dataset-items?token=$TOKEN&format=json&timeout=600" -H "Content-Type: application/json" -d "$2" -o "$R/$3"; echo "$3 $(python3 -c "import json;print(len(json.load(open('$R/$3'))))" 2>&1)"; }
for s in 1 2 3 4 5; do
 run azzouzana~trustpilot-scraper "{\"company\":\"myprotein.it\",\"maxItems\":50,\"sortBy\":\"recency\",\"filterStars\":[\"$s\"],\"filterLanguages\":\"it\",\"filterDateRange\":\"last12months\",\"includeReviewsDistribution\":true,\"includeBusinessDetails\":true}" trustpilot_${s}star.json &
done
run apify~instagram-scraper '{"directUrls":["https://www.instagram.com/myprotein_it/"],"resultsType":"posts","resultsLimit":50,"addParentData":false}' instagram_posts.json &
run clockworks~tiktok-scraper '{"profiles":["myprotein"],"hashtags":["myproteinitalia","myprotein"],"resultsPerPage":25,"proxyCountryCode":"IT","shouldDownloadVideos":false,"shouldDownloadCovers":false}' tiktok_posts.json &
wait
