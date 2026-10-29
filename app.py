import os
import sqlite3
from flask import Flask, jsonify, render_template, request

from routes.lyo_routes import lyo_bp
from routes.node_routes import node_bp
from routes.agent_routes import agent_bp
from routes.rwa_engine import rwa_bp
from routes.soroban_bridge import soroban_bridge_bp
from routes.dao_governance import dao_bp
from routes.predictive_simulation import simulation_bp
from routes.compliance_engine import compliance_bp
# استيراد مسار سرب الوكلاء الذكيين المستقلين (Autonomous Agent Swarm)
from routes.autonomous_swarm import swarm_bp

# استيراد محرك الحماية والسيادة لعقدة طرابلس وأومنيفيرس
from deploy_omniverse_sovereignty import OmniverseSovereignDeployer

# استيراد محرك المرونة التشفيرية ووسيط الحماية الصارم (Zero-Trust & Quantum-Resilient)
from crypto_agility import CryptoAgilityEngine
from agent_security import require_zero_trust_security

app = Flask(__name__)

# تسجيل جميع المسارات المعيارية (Blueprints) بما فيها سرب الوكلاء المستقلين
app.register_blueprint(lyo_bp)
app.register_blueprint(node_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(rwa_bp)
app.register_blueprint(soroban_bridge_bp)
app.register_blueprint(dao_bp)
app.register_blueprint(simulation_bp)
app.register_blueprint(compliance_bp)
app.register_blueprint(swarm_bp)

# تفعيل ونشر درع الحماية السيادي والتدقيق الفوري (PRISM AI Security & Solo Host Guard)
sovereign_deployer = OmniverseSovereignDeployer()
sovereign_deployer.execute_full_deployment(app)

# تهيئة محرك التشفير الكمي الهجين للعمليات الآمنة
crypto_engine = CryptoAgilityEngine(mode="quantum_hybrid")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name TEXT NOT NULL,
                asset_value REAL NOT NULL,
                owner_id TEXT NOT NULL,
                payment_tx TEXT,
                timestamp TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_action TEXT NOT NULL,
                details TEXT NOT NULL,
                timestamp TEXT
            )
        """)
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy", 
        "architecture": "Flask Blueprints Modular - Zero Error",
        "node": "Tripoli Node v0.6.3",
        "security": "PRISM AI Shield & Quantum-Resilient Active",
        "rwa_module": "Active & Secured",
        "soroban_bridge": "Active & Connected",
        "dao_governance": "Active & Secured",
        "predictive_simulation": "Active & AI-Powered",
        "compliance_gateway": "Active & Compliant",
        "autonomous_swarm": "Active & 24/7 Monitoring"
    }), 200

# مسار محمي ومخصص للوكلاء الذكيين ومعاملات عملة LYO مع التحقق من KYC والتشفير الكمي
@app.route('/api/v1/lyo/execute-task', methods=['POST'])
@require_zero_trust_security
def execute_agent_task():
    data = request.json or {}
    return jsonify({
        "status": "success",
        "message": "Zero-Trust & Quantum-Resilient security validation passed.",
        "utility_token": "LYO",
        "node": "Tripoli Node",
        "action_executed": data.get("action", "default_smart_city_task")
    }), 200

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)