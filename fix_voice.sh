#!/bin/bash
HTML_FILE="ui/index.html"
sed -i 's/window.speechSynthesis.speak(msg);/window.speechSynthesis.cancel(); setTimeout(() => { window.speechSynthesis.speak(msg); }, 200);/g' $HTML_FILE
git add .
git commit -m "تحسين استجابة الصوت في متصفح باي"
git push origin main
echo "✅ تم تحسين الصوت! حدث الصفحة واضغط على الكرة مرتين."
