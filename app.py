from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # هذا السطر هو "الجسر" الذي يسمح لهاتفك بالاتصال باللابتوب

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "city": "Omniverse Hub",
        "commander": "Abdlkadr",
        "message": "Welcome to the Smart City Backend V1.0"
    })

@app.route('/api/status')
def get_status():
    # هنا سنربط لاحقاً حالة الـ Pi Node الخاص بك
    return jsonify({"node_status": "Active", "sync_level": "99%"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)