#!/bin/bash
HTML_FILE="ui/index.html"

# إعادة بناء الملف بهيكل نظيف جداً ومتوافق مع متصفح باي
cat << 'HTML' > $HTML_FILE
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omniverse Hub | أومني فيرس</title>
    <style>
        body { background: #0b0e14; color: white; font-family: sans-serif; text-align: center; display: flex; flex-direction: column; justify-content: center; height: 100vh; margin: 0; }
        .logo { font-size: 3rem; font-weight: bold; color: #ffcc00; text-shadow: 0 0 20px #ffcc00; }
        .status-box { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin: 20px; border: 1px solid #333; }
        .btn { background: #ffcc00; color: #000; border: none; padding: 15px 30px; border-radius: 8px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; }
    </style>
</head>
<body>
    <div class="logo">OMNIVERSE HUB</div>
    <div class="status-box">
        <h3>مرحباً بك يا قائد عبد القادر</h3>
        <p id="system-msg">جاري فحص اتصال السيرفر المحلي...</p>
        <div id="api-data" style="color: #00ff00; font-family: monospace;"></div>
    </div>
    
    <button onclick="window.location.href='https://sandbox.minepi.com/_sandbox/authorize'" class="btn">🔑 تفعيل Sandbox</button>

    <script>
        // محاولة الاتصال بالسيرفر بطريقة لا تسبب تعليق المتصفح
        async function checkServer() {
            try {
                const res = await fetch('http://10.86.224.153:5000/', { mode: 'cors' });
                const data = await res.json();
                document.getElementById('system-msg').innerText = "✅ متصل بالسيرفر المحلي";
                document.getElementById('api-data').innerText = "Commander: " + data.commander;
            } catch (e) {
                document.getElementById('system-msg').innerText = "⚠️ السيرفر المحلي غير مرئي (تأكد من الـ Wi-Fi)";
            }
        }
        checkServer();
    </script>
</body>
</html>
HTML

# الرفع لـ GitHub
git add .
git commit -m "إصلاح الشاشة البيضاء وتحسين التوافق مع متصفح باي"
git push origin main
echo "✅ تم الإصلاح! انتظر دقيقة ثم حدث الصفحة في هاتفك."
