#!/bin/bash
HTML_FILE="ui/index.html"

cat << 'HTML' > $HTML_FILE
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omniverse Hub | Final Sync</title>
    <style>
        body { background: #080a0f; color: white; font-family: sans-serif; text-align: center; margin: 0; padding-top: 30px; }
        .logo { font-size: 2.2rem; font-weight: bold; color: #ffcc00; text-shadow: 0 0 20px #ffcc00; margin-bottom: 20px; letter-spacing: 2px; }
        .ai-agent { width: 110px; height: 110px; background: radial-gradient(circle, #ffcc00, #ff8800); border-radius: 50%; margin: 0 auto 30px; box-shadow: 0 0 30px #ffcc00; animation: pulse 1.5s infinite; cursor: pointer; border: 3px solid rgba(255,255,255,0.2); }
        @keyframes pulse { 0%, 100% { transform: scale(1); filter: brightness(1); } 50% { transform: scale(1.1); filter: brightness(1.2); } }
        .grid { display: flex; justify-content: center; gap: 15px; padding: 0 20px; }
        .card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,204,0,0.3); padding: 20px; border-radius: 20px; flex: 1; backdrop-filter: blur(10px); }
        .card-title { font-size: 0.75rem; color: #ffcc00; margin-bottom: 10px; }
        .card-val { font-size: 1.2rem; font-weight: bold; }
        #server-status { margin-top: 25px; font-weight: bold; padding: 10px; border-radius: 10px; display: inline-block; }
        .btn-fix { display: none; background: #ff4444; color: white; border: none; padding: 10px 20px; border-radius: 10px; margin-top: 15px; cursor: pointer; text-decoration: none; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="ai-agent" onclick="speak()"></div>
    <div class="logo">OMNIVERSE HUB</div>

    <div class="grid">
        <div class="card">
            <div class="card-title">Pi Node</div>
            <div id="node-status" class="card-val" style="color: #ffaa00;">Searching...</div>
        </div>
        <div class="card">
            <div class="card-title">AI Sync</div>
            <div class="card-val" style="color: #00ff00;">99.9%</div>
        </div>
    </div>

    <div id="server-status" style="color: #ff4444;">🔴 السيرفر: غير متصل</div>
    <br>
    <a id="fix-link" href="http://10.91.114.153:5000" target="_blank" class="btn-fix">⚠️ اضغط هنا لتفعيل الاتصال المحلي</a>

    <script>
        function speak() {
            const msg = new SpeechSynthesisUtterance("مرحباً بك يا قائد عبد القادر. أنظمة أومني فيرس في انتظار المزامنة النهائية.");
            msg.lang = 'ar-SA';
            window.speechSynthesis.speak(msg);
        }

        async function checkServer() {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 1500);
                
                const res = await fetch('http://10.91.114.153:5000/', { signal: controller.signal });
                if(res.ok) {
                    document.getElementById('server-status').innerText = "✅ السيرفر المحلي: متصل بنجاح";
                    document.getElementById('server-status').style.color = "#00ff00";
                    document.getElementById('node-status').innerText = "Synced ✅";
                    document.getElementById('node-status').style.color = "#00ff00";
                    document.getElementById('fix-link').style.display = "none";
                }
            } catch (e) {
                document.getElementById('fix-link').style.display = "inline-block";
            }
        }
        setInterval(checkServer, 2000);
        checkServer();
    </script>
</body>
</html>
HTML

git add .
git commit -m "إضافة كود المزامنة القسرية والزر الذكي"
git push origin main
echo "✅ تم التحديث النهائي! اتبع تعليمات القائد الآن."
