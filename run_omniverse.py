import os
import subprocess
import re
import time
import sys

def launch_tunnel():
    print("Starting Global Tunnel via Cloudflare...")
    
    cloudflared_path = os.path.join(os.getcwd(), "cloudflared.exe")
    if not os.path.exists(cloudflared_path):
        print("Error: cloudflared.exe not found!")
        return None, None

    # Connect to local port 5000
    tunnel_cmd = f'"{cloudflared_path}" tunnel --url http://127.0.0.1:5000'
    
    # We use stderr=subprocess.STDOUT because cloudflared logs to stderr
    process = subprocess.Popen(tunnel_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    
    url = None
    print("Waiting for Global Link (this may take 15-45 seconds)...")
    
    start_time = time.time()
    while time.time() - start_time < 60:  # Increased timeout to 60 seconds
        line = process.stdout.readline()
        if not line: break
        
        # Look for the specific pattern of trycloudflare
        if ".trycloudflare.com" in line and "https://" in line:
            # We filter out the generic 'api.trycloudflare.com'
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match and "api.trycloudflare.com" not in match.group():
                url = match.group()
                break
        time.sleep(0.1)
    
    return url, process

def update_ui_with_global_url(url):
    html_path = os.path.join("src", "ui", "index.html")
    if os.path.exists(html_path):
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            pattern = r'const API_URL\s*=\s*".*";'
            replacement = f'const API_URL = "{url}";'
            
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Success: UI Updated with {url}")
        except Exception as e:
            print(f"Warning: UI Update failed: {e}")

if __name__ == "__main__":
    # Clean old processes
    os.system('taskkill /f /im cloudflared.exe >nul 2>&1')
    
    global_url, tunnel_proc = launch_tunnel()

    if global_url:
        update_ui_with_global_url(global_url)
        print("\n" + "="*60)
        print(f"OMNIVERSE IS NOW LIVE!")
        print(f"Public Link: {global_url}/ui/index.html")
        print("="*60 + "\n")
        
        try:
            print("Starting Flask Server...")
            subprocess.run([sys.executable, "app.py"])
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            if tunnel_proc:
                tunnel_proc.terminate()
    else:
        print("Error: Could not capture a unique tunnel URL.")
        print("Please try running the command again.")
        if tunnel_proc: tunnel_proc.terminate()