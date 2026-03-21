#!/bin/bash
echo "🌐 Paste Ngrok URL:"
read NEW_URL
sed -i "s|const API_URL = \".*\";|const API_URL = \"$NEW_URL\";|g" ui/index.html
git add .
git commit -m "Update Tunnel: $NEW_URL"
git push origin main
echo "🚀 DONE! Check Pi Browser."
