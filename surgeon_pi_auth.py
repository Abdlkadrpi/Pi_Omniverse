import os
import re
import subprocess

# إعدادات المسارات
FILE_PATH = "ui/index.html"
API_URL = "https://kind-insects-hunt.loca.lt" # الرابط المستقر الذي يعمل لديك الآن

def surgeon_inject():
    print("--- [ 💉 Starting Surgical Injection: Pi SDK ] ---")
    
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found!")
        return

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. حقن مكتبة Pi SDK في الـ <head>
    if 'sdk.minepi.com' not in content:
        print("Injecting Pi SDK Library...")
        content = content.replace('</head>', '<script src="https://sdk.minepi.com/pi-sdk.js"></script>\n</head>')

    # 2. حقن منطق التوثيق (Authentication Logic)
    auth_script = f"""
    <script>
    const Pi = window.Pi;
    Pi.init({{ version: "2.0", sandbox: true }});

    async function authPi() {{
        try {{
            console.log("Requesting Pi Auth...");
            const scopes = ['username', 'payments'];
            const auth = await Pi.authenticate(scopes, (payment) => {{}});
            
            // تحديث الواجهة باسم القائد عبد القادر الحقيقي من Pi
            const userElement = document.querySelector('.user-name') || document.body;
            if(userElement) {{
                userElement.innerHTML = "Welcome, @" + auth.user.username;
                userElement.style.color = "#00ffcc";
            }}
            alert("Welcome to Omniverse, @" + auth.user.username);
            
            // إرسال البيانات للسيرفر المحلي في طرابلس
            fetch("{API_URL}/register", {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ username: auth.user.username, uid: auth.user.uid }})
            }}).catch(e => console.log("Local server offline, but Pi Auth Success!"));

        }} catch (err) {{
            console.error("Auth failed:", err);
        }}
    }}
    // تشغيل التوثيق تلقائياً
    authPi();
    </script>
    """

    if 'authPi()' not in content:
        print("Injecting Auth Logic...")
        content = content.replace('</body>', auth_script + '\n</body>')

    # حفظ التعديلات
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("Surgery Completed Successfully!")

    # 3. الرفع التلقائي لـ GitHub
    print("--- [ 🚀 Syncing with GitHub ] ---")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Surgical Update: Pi SDK Authentication Integrated"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Everything is Live on GitHub!")
    except Exception as e:
        print(f"Git Error: {e}")

if __name__ == "__main__":
    surgeon_inject()