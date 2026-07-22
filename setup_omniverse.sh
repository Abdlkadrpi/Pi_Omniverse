#!/bin/bash
# Omniverse Smart City Auto-Scaler Script

echo "Starting Omniverse Optimization..."

# 1. التأكد من المسارات الصحيحة
if [ ! -d "ui" ]; then
  echo "Error: UI folder not found. Please move it to root."
  exit 1
fi

# 2. تحديث app.py لدعم الـ API Stats (حل أخطاء 404)
cat <<EOF > app.py
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(BASE_DIR, 'ui')

@app.route('/')
def index():
    return send_from_directory(UI_DIR, 'index.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "status": "operational",
        "total_citizens": 60000000,
        "network": "Pi Mainnet Ready"
    }), 200

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(UI_DIR, path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
EOF

echo "App.py optimized for API stability."

# 3. التأكد من ملف المتطلبات (requirements.txt)
echo "gunicorn" > requirements.txt
echo "flask" >> requirements.txt
echo "flask-cors" >> requirements.txt

echo "Optimization Complete. Ready for deployment."