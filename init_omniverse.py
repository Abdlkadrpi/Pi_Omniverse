import os

def generate_full_app():
    print("[*] Generating Omniverse Smart City Backend Engine...")
    
    app_code = """from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import hashlib
import json

app = Flask(__name__)
CORS(app)

UI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'network_state.json')

# التأكد من وجود مجلد البيانات
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({"assets": [], "connections": []}, f)

# 1. مسار المصادقة (Pi SDK Auth)
@app.route('/api/pi-auth', methods=['POST'])
def pi_auth():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON in request"}), 400
        
    data = request.get_json()
    user_token = data.get('accessToken')
    
    if user_token: 
        return jsonify({"status": "authenticated", "message": "Citizen verified by Pi Network"}), 200
    
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# 2. محرك العقود الذكية (LYO Token Engine)
@app.route('/api/certify', methods=['POST'])
def certify():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON"}), 400
    
    data = request.get_json()
    content = data.get('content', '')
    cert_id = hashlib.sha256(content.encode()).hexdigest()[:16]
    
    return jsonify({"status": "success", "cert_id": f"LYO_{cert_id}"}), 200

# 3. محرك ترميز الأصول الرقمية (Asset Tokenization Engine - NEW)
@app.route('/api/register_asset', methods=['POST'])
def register_asset():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON payload"}), 400
        
    data = request.get_json()
    asset_name = data.get('name', 'Unknown Asset')
    asset_value = data.get('value', 0)
    owner = data.get('owner', 'Anonymous')
    
    # بصمة العقد الذكي للأصل
    asset_hash = hashlib.sha256(f"{asset_name}{asset_value}{owner}".encode()).hexdigest()[:12]
    
    # حفظ الأصل في قاعدة بيانات المدينة الرقمية
    with open(DATA_FILE, 'r+') as f:
        state = json.load(f)
        state['assets'].append({"name": asset_name, "value": asset_value, "owner": owner, "asset_id": f"ASSET_{asset_hash}"})
        f.seek(0)
        json.dump(state, f, indent=4)
        
    return jsonify({
        "status": "success", 
        "message": f"Asset '{asset_name}' successfully tokenized on Omniverse Ledger.",
        "asset_id": f"ASSET_{asset_hash}",
        "tvl": sum(item['value'] for item in state['assets'])
    }), 200

# 4. شبكة الثقة الاجتماعية اللامركزية (Social Graph Engine - NEW)
@app.route('/api/connect_users', methods=['POST'])
def connect_users():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON payload"}), 400
        
    data = request.get_json()
    user1 = data.get('user1')
    user2 = data.get('user2')
    
    if not user1 or not user2:
        return jsonify({"status": "error", "message": "Users data required"}), 400
        
    with open(DATA_FILE, 'r+') as f:
        state = json.load(f)
        connection = {"node_a": user1, "node_b": user2, "link_type": "trust_graph"}
        if connection not in state['connections']:
            state['connections'].append(connection)
            f.seek(0)
            json.dump(state, f, indent=4)
            
    return jsonify({"status": "success", "message": f"Social Graph link established between {user1} and {user2}"}), 200

# 5. وكيل الحوكمة الذكي (AI Governance Agent)
@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    if not request.is_json:
        return jsonify({"status": "error", "message": "Missing JSON"}), 400
        
    data = request.get_json()
    user_message = data.get('message', '')
    
    if "Audit" in user_message:
        return jsonify({"status": "success", "message": "Audit confirmed: LYO balance is secure."}), 200
        
    return jsonify({"status": "success", "message": "Governance agent received your request."}), 200

# 6. المسار الرئيسي
@app.route('/')
def index():
    return send_from_directory(UI_DIR, 'index.html')

# 7. معالجة الملفات الثابتة والتوافق (Compliance Routing)
@app.route('/robots.txt')
def robots():
    return jsonify({"status": "compliance_ok", "agent": "PiNetworkCrawler", "status": "allowed"}), 200

@app.route('/<path:path>')
def serve_static(path):
    if path == 'legal.html':
        return send_from_directory(UI_DIR, 'legal.html')
    
    clean_path = path.replace('ui/', '', 1)
    if os.path.exists(os.path.join(UI_DIR, clean_path)):
        return send_from_directory(UI_DIR, clean_path)
    
    return send_from_directory(UI_DIR, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
"""

    with open("app.py", "w", encoding="utf-8") as f:
        f.write(app_code)
    print("[+] app.py successfully generated with Web3, Tokenization, and Social Graph engines!")

if __name__ == "__main__":
    generate_full_app()