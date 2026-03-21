#!/bin/bash
NEW_URL="https://quiet-needles-play.loca.lt"
FILE_PATH="ui/index.html"

echo "🔄 Updating API URL..."
sed -i "s|const API_URL = \".*\";|const API_URL = \"$NEW_URL\";|g" "$FILE_PATH"

echo "📤 Pushing to GitHub..."
git add .
git commit -m "Auto-sync with localtunnel"
git push origin main

echo "✅ Done! Check your Pi Browser now."