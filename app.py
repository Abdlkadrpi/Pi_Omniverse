from flask import Flask, render_template_string
import sys
import os

sys.path.append(os.getcwd())
from core.pi_rc1_token import UnitToken
from core.ai_oracle import evaluate_content

app = Flask(__name__)

@app.route('/')
def dashboard():
    token = UnitToken()
    score = evaluate_content('VIDEO')
    # محاكاة الربح للقائد
    tax = (score * 0.1) * 0.05
    
    html_template = """
    <html>
        <head><title>Pi-Omniverse Dashboard</title></head>
        <body style="background-color: #1a1a1a; color: #ffd700; font-family: Arial; text-align: center; padding-top: 50px;">
            <h1>🛡️ مركز تحكم Pi-Omniverse</h1>
            <div style="border: 2px solid #ffd700; display: inline-block; padding: 20px; border-radius: 15px;">
                <h2>حالة المدينة: <span style="color: #00ff00;">نشطة ✅</span></h2>
                <hr style="border-color: #ffd700;">
                <h3>💰 أرباح القائد الحالية: {{ tax }} $UNIT</h3>
                <p>إجمالي تقييمات الذكاء الاصطناعي اليوم: {{ score }}</p>
            </div>
            <br><br>
            <p>تم الاتصال بنجاح بنواة Pi Network</p>
        </body>
    </html>
    """
    return render_template_string(html_template, tax=tax, score=score)

if __name__ == '__main__':
    print("🚀 المدينة الآن على الرابط: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)