#!/bin/zsh
cd ~/Documents/output/myprotein-2026-09-21/raw/yt
Y="yt-dlp --sleep-requests 1"
# canale brand: top video per views
$=Y --flat-playlist --dump-json "https://www.youtube.com/user/MyproteinIT/videos" > channel_flat.jsonl 2>channel.err
# ricerca video di terzi
for q in "myprotein recensione" "myprotein opinioni" "proteine myprotein vale la pena" "myprotein vs prozis" "myprotein impact whey recensione italiano"; do
  $=Y --flat-playlist --dump-json "ytsearch15:$q" >> search_flat.jsonl 2>>search.err
done
echo done
