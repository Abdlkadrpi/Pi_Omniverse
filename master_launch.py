import os
import subprocess
import time
import re
import sys

# إجبار البايثون على استخدام ترميز UTF-8 لتجنب أخطاء اللغة العربية
sys.stdout.reconfigure(encoding='utf-8')

FILE_PATH = "ui/index.html"
PORT = "5000"

def launch():
    print("-" * 40)
    print("Starting Pi_Omniverse Master System...")
    print("-" * 40)

    # 1. تشغيل سيرفر الملفات المحلي
    print("Step 1: Launching Local Python Server on Port 5000...")
    subprocess.Popen(f"start powershell -Command python -m http.server {PORT}", shell=True)
    time.sleep(2)

    # 2. إنشاء نفق الـ SSH
    print("Step 2: Creating Global SSH Tunnel...")
    # حذف ملف اللوج القديم إذا وجد
    if os.path.exists("tunnel.log"):
        os.remove("tunnel.log")
        
    ssh_cmd = f"ssh -o ServerAliveInterval=30 -R 80:localhost:{PORT} nokey@localhost.run"
    # تشغيل النفق وتحويل المخرجات لملف نصي
    subprocess.Popen(f"powershell -Command \"{ssh_cmd} | Tee-Object -FilePath tunnel.log\"", shell=True)
    
    print("Waiting for link extraction (10 seconds)...")
    time.sleep(10) 

    # 3. استخراج الرابط من ملف الـ Log
    new_url = ""
    if os.path.exists("tunnel.log"):
        try:
            with open("tunnel.log", "r", encoding="utf-16") as f: # الويندوز غالباً يسجل بـ utf-16
                log_content = f.read()
        except:
            with open("tunnel.log", "r", encoding="utf-8", errors="ignore") as f:
                log_content = f.read()
                
        match = re.search(r'https://[a-z0-9-]+\.lhr\.life', log_content)
        if match:
            new_url = match.group(0)

    if not new_url:
        print("\n[!] Could not find link automatically.")
        new_url = input("Please PASTE the .lhr.life link from the black window: ").strip()

    print(f"URL Detected: {new_url}")

    # 4. تحديث ملف HTML
    print("Step 3: Updating index.html with new URL...")
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated_content = re.sub(r'const API_URL = ".*?";', f'const API_URL = "{new_url}";', content)
        
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("File updated successfully.")

    # 5. الرفع لـ GitHub
    print("Step 4: Syncing with GitHub...")
    os.system("git add .")
    os.system('git commit -m "Automated System Update"')
    os.system("git push origin main")

    print("-" * 40)
    print("MISSION ACCOMPLISHED!")
    print(f"1. Open Tunnel: {new_url}")
    print(f"2. Open App: https://abdlkadrpi.github.io/Pi_Omniverse/ui/index.html")
    print("-" * 40)

if __name__ == "__main__":
    launch()