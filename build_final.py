import os
import sys

# هيكل البيانات
project_data = {
    "core": {
        "pi_rc1_token.py": "class UnitToken:\n    def __init__(self):\n        self.owner_tax_rate = 0.05\n    def process_reward(self, user, score):\n        base = score * 0.1\n        tax = base * self.owner_tax_rate\n        print(f'\\n--- 💰 سجل الأرباح ---')\n        print(f'المستخدم: {user} | حصة القائد: {tax:.4f} $UNIT')\n        return base - tax",
        "ai_oracle.py": "def evaluate_content(content_type):\n    return 95 if content_type == 'VIDEO' else 60"
    },
    "agents": {"security_agent.py": "def check_kyc(): return True"},
    "ui": {"dashboard.html": "<h1>Pi-Omniverse</h1>"}
}

# التنفيذ
for folder, files in project_data.items():
    if not os.path.exists(folder): os.makedirs(folder)
    for name, content in files.items():
        with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
            f.write(content)

print("🚀 تم بناء مجلدات وملفات المدينة بنجاح!")

# تشغيل المحاكاة فوراً
sys.path.append(os.getcwd())
from core.pi_rc1_token import UnitToken
from core.ai_oracle import evaluate_content

token = UnitToken()
score = evaluate_content('VIDEO')
token.process_reward('User_Alpha', score)
