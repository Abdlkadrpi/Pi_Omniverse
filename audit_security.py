import os
import re

# الكلمات المفتاحية الحساسة التي يحظر وجودها في الأكواد
SENSITIVE_PATTERNS = [
    r"api[_-]?key\s*=\s*['\"](?!None|os\.)[\w-]{16,}['\"]",
    r"password\s*=\s*['\"].+['\"]",
    r"secret[_-]?key\s*=\s*['\"].+['\"]",
    r"sk_live_[0-9a-zA-Z]{24,}",
    r"ghp_[0-9a-zA-Z]{36}"
]

EXCLUDED_DIRS = {'.git', '__pycache__', 'venv', 'env', 'downloads'}

def scan_codebase(root_dir="."):
    print(f"[*] Starting local security scan in: {os.path.abspath(root_dir)}")
    violations = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # استبعاد المجلدات غير المرغوب فحصها
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        
        for file in filenames:
            if file.endswith(('.py', '.json', '.env', '.yaml', '.yml', '.html')) and file != 'audit_security.py':
                file_path = os.path.join(dirpath, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for pattern in SENSITIVE_PATTERNS:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                violations += 1
                                print(f"[!] Warning: Potential secret found in {file_path} matching pattern {pattern}")
                except Exception as e:
                    pass

    if violations == 0:
        print("[+] Security Scan Passed: No hardcoded secrets or API keys detected in source files.")
    else:
        print(f"[!] Security Scan Finished with {violations} potential issues found. Please review and move secrets to environment variables (.env).")

if __name__ == "__main__":
    scan_codebase()