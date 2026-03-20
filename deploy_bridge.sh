#!/bin/bash

# 1. تحديد ملف الواجهة
HTML_FILE="ui/index.html"
SERVER_IP="10.86.224.153"

echo "🎯 جاري حقن ذكاء السيرفر في $HTML_FILE..."

# 2. إضافة كود الاتصال بالسيرفر قبل نهاية وسم الـ body
# سيقوم هذا الكود بمحاولة الاتصال بسيرفر اللابتوب وعرض النتيجة
sed -i "/<\/body>/i \
    <div id='api-status' style='position:fixed; bottom:20px; right:20px; background:rgba(0,0,0,0.7); color:#00ff00; padding:10px; border-radius:10px; font-family:monospace; border:1px solid #00ff00; z-index:10000;'> \
        📡 System: <span id='status-val'>Connecting...</span><br> \
        👤 User: <span id='user-val'>...</span> \
    </div> \
    <script> \
        async function checkOmniverseServer() { \
            try { \
                const response = await fetch('http://$SERVER_IP:5000/'); \
                const data = await response.json(); \
                document.getElementById('status-val').innerText = data.status; \
                document.getElementById('user-val').innerText = data.commander; \
                console.log('✅ Connected to Omniverse Backend'); \
            } catch (e) { \
                document.getElementById('status-val').innerText = 'Offline'; \
                document.getElementById('status-val').style.color = 'red'; \
            } \
        } \
        checkOmniverseServer(); \
        setInterval(checkOmniverseServer, 5000); \
    </script>" $HTML_FILE

# 3. الرفع التلقائي لـ GitHub
echo "🚀 جاري الرفع إلى القلعة الرقمية (GitHub)..."
git add .
git commit -m "تفعيل الربط الحي بين الواجهة وسيرفر اللابتوب المحلي"
git push origin main

echo "✅ تم الرفع بنجاح! مدينتك الذكية الآن متصلة بعقلك المدبر."
