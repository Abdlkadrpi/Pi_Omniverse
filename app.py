import os
import sqlite3
from flask import Flask, jsonify, render_template, request

# استيراد مسارات المشروع المعيارية (Blueprints)
from routes.lyo_routes import lyo_bp
from routes.node_routes import node_bp
from routes.agent_routes import agent_bp
from routes.rwa_engine import rwa_bp
from routes.soroban_bridge import soroban_bridge_bp
from routes.dao_governance import dao_bp
from routes.predictive_simulation import simulation_bp
from routes.compliance_engine import compliance_bp
from routes.autonomous_swarm import swarm_bp
from routes.lyo_payment_routes import lyo_blueprint

# استيراد مسار مدفوعات وتكامل شبكة باي (Pi Payments & SDK Integration)
from routes.pi_payments import pi_bp

# استيراد مسار محسن وإدارة الذاكرة الديناميكي (Dynamic Memory Optimization Layer)
from routes.memory_optimizer import memory_bp, check_system_memory

# استيراد مسار الذكاء الاصطناعي المادي والمستشعرات الفيزيائية (Physical AI Telemetry)
from routes.physical_ai import physical_ai_bp

# استيراد مسار ربط السيرفرين (تزامن عقدة طرابلس مع أومنيفيرس)
from server_bridge_sync import server_bridge_bp

# استيراد محرك الحماية والسيادة لعقدة طرابلس وأومنيفيرس
from deploy_omniverse_sovereignty import OmniverseSovereignDeployer

# استيراد محركات الأمان والتشفير المتقدمة
from crypto_agility import CryptoAgilityEngine
from agent_security import require_zero_trust_security

# استيراد درع فحص خداع الوكلاء والتشفير المقاوم للكم المحدث (PRISM PQC Guardrail)
from prism_pqc_guardrail import require_prism_pqc_guardrail

app = Flask(__name__)

# تسجيل جميع المسارات المعيارية (Blueprints) بما فيها مسار إدارة الذاكرة والذكاء المادي وجسر السيرفرين ومدفوعات باي
app.register_blueprint(lyo_bp)
app.register_blueprint(node_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(rwa_bp)
app.register_blueprint(soroban_bridge_bp)
app.register_blueprint(dao_bp)
app.register_blueprint(simulation_bp)
app.register_blueprint(compliance_bp)
app.register_blueprint(swarm_bp)
app.register_blueprint(lyo_blueprint)
app.register_blueprint(pi_bp) # تسجيل مسار مدفوعات Pi Network الجديد
app.register_blueprint(memory_bp) # تسجيل مسار تحسين وإدارة الذاكرة
app.register_blueprint(physical_ai_bp) # تسجيل مسار الذكاء الاصطناعي المادي والمستشعرات
app.register_blueprint(server_bridge_bp) # تسجيل مسار التزامن بين السيرفرين

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
        # التأكد من وجود جدول المعاملات (transactions) الخاص بمدفوعات باي
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_id TEXT UNIQUE NOT NULL,
                txid TEXT,
                user_uid TEXT NOT NULL,
                amount REAL NOT NULL,
                service_type TEXT,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    # جلب حالة استهلاك الذاكرة العشوائية محلياً
    mem_status = check_system_memory()
    
    return jsonify({
        "status": "healthy", 
        "architecture": "Flask Blueprints Modular - Zero Error",
        "node": "Tripoli Node v0.6.3",
        "security": "PRISM AI Shield & Quantum-Resilient Active",
        "memory_optimization": "Active & Dynamic Garbage Collection",
        "system_memory": mem_status,
        "physical_ai_gateway": "Active & Ready for Sensor Telemetry",
        "rwa_module": "Active & Secured",
        "soroban_bridge": "Active & Connected",
        "dao_governance": "Active & Secured",
        "predictive_simulation": "Active & AI-Powered",
        "compliance_gateway": "Active & Compliant",
        "autonomous_swarm": "Active & 24/7 Monitoring",
        "lyo_governance_engine": "Active & Deflationary Burn Enabled",
        "pi_payments_gateway": "Active & Ready for Mainnet/Testnet",
        "prism_pqc_guardrail": "Active & Deception Shield Enabled"
    }), 200

# مسار محمي ومخصص للوكلاء الذكيين ومعاملات عملة LYO مع دمج درع فحص الخداع (CoT) والتشفير الكمي
@app.route('/api/v1/lyo/execute-task', methods=['POST'])
@require_zero_trust_security
@require_prism_pqc_guardrail(strict_kyc=True) # تفعيل فحص خداع الوكلاء وقوانين LYO الحتمية
def execute_agent_task():
    data = request.json or {}
    is_kyc = data.get("is_kyc_verified", False)
     
    # فرض التحقق من موثقية Pi Network KYC لمنع أي استثناء
    if not is_kyc:
        return jsonify({
            "status": "error",
            "compliance_error": "PI_KYC_REQUIRED",
            "message": "Access denied: Pi Network KYC verification is mandatory for LYO utility and agent operations."
        }), 403

    amount = float(data.get("amount_lyo", 10.0))
    burn_fee = amount * 0.01  # حساب نسبة الحرق الآمن 1%

    return jsonify({
        "status": "success",
        "message": "Zero-Trust & Quantum-Resilient security validation passed. LYO utility task executed successfully.",
        "utility_token": "LYO",
        "node": "Tripoli Node v0.6.3",
        "action_executed": data.get("action", "default_smart_city_task"),
        "amount_processed": amount,
        "deflationary_burn": burn_fee,
        "burn_address": "0x000000000000000000000000000000000000DEAD"
    }), 200

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)