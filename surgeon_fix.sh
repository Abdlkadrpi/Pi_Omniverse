#!/bin/bash
HTML_FILE="ui/index.html"
echo "🎯 جاري إجراء العملية الجراحية لملف $HTML_FILE..."
sed -i '/<body>/a \    <div id="dev-tools" style="position:fixed;top:0;left:0;z-index:9999;background:rgba(0,0,0,0.8);color:white;padding:10px;width:100%;text-align:center;"> <button onclick="window.location.href='\''https://sandbox.minepi.com/_sandbox/authorize'\''" style="background:#ffcc00;color:black;border:none;padding:10px 20px;border-radius:5px;font-weight:bold;cursor:pointer;">⚠️ اضغط هنا لتفعيل الرمز ⚠️</button> </div>' $HTML_FILE
git add .
git commit -m "إضافة زر الطوارئ لتفعيل الـ Sandbox"
git push origin main
echo "✅ اكتملت العملية الجراحية والرفع لـ GitHub!"
