#!/bin/bash
HTML_FILE="ui/index.html"

cat << 'HTML' > $HTML_FILE
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omniverse Hub | AI Agent</title>
    <style>
        body { background: #0b1218; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; overflow: hidden; height: 100vh; display: flex; flex-direction: column; justify-content: center; }
        .logo { font-size: 2.5rem; font-weight: bold; color: #ffcc00; text-shadow: 0 0 30px rgba(255,204,0,0.5); margin-bottom: 10px; }
        .ai-agent { width: 100px; height: 100px; background: radial-gradient(circle, #ffcc00, #aa8800); border-radius: 50%; margin: 0 auto 20px; box-shadow: 0 0 20px #ffcc00; animation: pulse 2s infinite; cursor: pointer; }
        @keyframes pulse { 0% { transform: scale(1); box-shadow: 0 0 20px #ffcc00; } 50% { transform: scale(1.1); box-shadow: 0 0 40px #ffcc00; } 100% { transform: scale(1); box-shadow: 0 0 20px #ffcc00; } }
        .status-card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 20px; margin: 0 20px; border: 1px solid rgba(255,204,0,0.2); }
        .btn-copy { background: linear-gradient(45deg, #ffcc00, #ffa500); color: black; border: none; padding: 12px 25px; border-radius: 10px; font-weight: bold; margin-top: 15px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="ai-agent" onclick="speak()"></div>
    <div class="logo">OMNIVERSE HUB</div>
    <div class="status-card">
        <h2 id="greeting">مرحباً بك يا قائد عبد القادر</h2>
        <p id="ai-msg">أنا مساعدك الذكي، جاري ربط الأنظمة...</p>
        <p id="server-status" style="color: #ff4444;">⚠️ السيرفر المحلي: غير متصل</p>
        <button class="btn-copy" onclick="copyCode()">📋 نسخ رمز التفعيل</button>
    </div>

    <script>
        function speak() {
            alert("قائد عبد القادر، أنظمة أومني فيرس تحت أمرك!");
        }
        function copyCode() {
            navigator.clipboard.writeText('LZ6QDDDK');
            alert("تم نسخ الرمز! اذهب الآن لـ develop.pi والصقه هناك.");
        }
        async function checkServer() {
            try {
                const res = await fetch('http://10.86.224.153:5000/');
                const data = await res.json();
                document.getElementById('server-status').innerText = "✅ السيرفر المحلي: متصل (Online)";
                document.getElementById('server-status').style.color = "#00ff00";
                document.getElementById('ai-msg').innerText = "الأنظمة تعمل بكفاءة، بانتظار أوامرك.";
            } catch (e) { }
        }
        setInterval(checkServer, 3000);
    </script>
</body>
</html>
HTML

git add .
git commit -m "إطلاق المساعد الذكي وتحسين واجهة المستخدم"
git push origin main
echo "✅ تم إطلاق المساعد الذكي! حدث الصفحة في هاتفك الآن."
