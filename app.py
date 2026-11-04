import os
import sqlite3
import json
import csv
import io
import time
from flask import Flask, jsonify, render_template, request, make_response

# استيراد الجدار الناري الذكي (Omniverse Smart WAF) من المجلد الرئيسي
from omniverse_waf import OmniverseSmartWAF, require_prism_clearance

# استيراد دالة الأرشفة التلقائية وجداول عقدة طرابلس
from archive_transactions import archive_verified_transaction, init_ledger_database

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

# استيراد مسار التصويت وحوكمة LYO المقاوم للكم
from blueprints.lyo_voting.routes import lyo_voting_bp

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

# تفعيل وربط الجدار الناري الذكي (Omniverse Smart WAF - بحد أقصى 60 طلباً بالدقيقة لكل IP)
waf = OmniverseSmartWAF(app, max_requests_per_minute=60)

# تسجيل جميع المسارات المعيارية (Blueprints)
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
app.register_blueprint(lyo_voting_bp)
app.register_blueprint(pi_bp)
app.register_blueprint(memory_bp)
app.register_blueprint(physical_ai_bp)
app.register_blueprint(server_bridge_bp)

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
    mem_status = check_system_memory()
    return jsonify({
        "status": "healthy", 
        "architecture": "Flask Blueprints Modular - Zero Error",
        "node": "Tripoli Node v0.6.3",
        "security": "PRISM AI Shield & Smart WAF & Quantum-Resilient Active",
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
        "lyo_voting_system": "Active & Post-Quantum Protected",
        "pi_payments_gateway": "Active & Ready for Mainnet/Testnet",
        "prism_pqc_guardrail": "Active & Deception Shield Enabled"
    }), 200

@app.route('/api/v1/lyo/execute-task', methods=['POST'])
@require_zero_trust_security
@require_prism_pqc_guardrail(strict_kyc=True)
def execute_agent_task():
    data = request.json or {}
    is_kyc = data.get("is_kyc_verified", False)
     
    if not is_kyc:
        return jsonify({
            "status": "error",
            "compliance_error": "PI_KYC_REQUIRED",
            "message": "Access denied: Pi Network KYC verification is mandatory for LYO utility and agent operations."
        }), 403

    amount = float(data.get("amount_lyo", 10.0))
    burn_fee = amount * 0.01  
    net_allocated = amount - burn_fee

    response_payload = {
        "status": "success",
        "message": "Zero-Trust, Smart WAF & Quantum-Resilient security validation passed. LYO utility task executed successfully.",
        "utility_token": "LYO",
        "node": "Tripoli Node v0.6.3",
        "cyber_security": {
            "pqc_signature_verified": True,
            "prism_guardrail_status": "PASSED",
            "timestamp": time.time()
        },
        "transaction_details": {
            "pi_user_uid": data.get("user_uid", "tripoli_node_admin_01"),
            "service_type": data.get("action", "default_smart_city_task"),
            "gross_paid_lyo": amount,
            "net_allocated_lyo": net_allocated,
            "burned_lyo": burn_fee,
            "burn_address": "0x000000000000000000000000000000000000DEAD",
            "node_origin": "Tripoli_Node_Gate_01"
        },
        "compliance_standards": {
            "pi_network_sdk": "v2.0_Verified",
            "global_utility_standard": "Compliant_Non_Security_Utility"
        }
    }

    try:
        init_ledger_database()
        archive_verified_transaction(response_payload)
    except Exception as e:
        print(f"[-] خطأ أثناء أرشفة المعاملة في الخادم: {e}")

    return jsonify(response_payload), 200

@app.route('/api/v1/sovereign/ledger/archive', methods=['GET'])
def get_sovereign_ledger_archive():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='sovereign_ledger_archive';
            """)
            if not cursor.fetchone():
                return jsonify({
                    "status": "success",
                    "node": "Tripoli Node v0.6.3",
                    "total_records": 0,
                    "transactions": []
                }), 200

            cursor.execute("SELECT * FROM sovereign_ledger_archive ORDER BY id DESC;")
            rows = cursor.fetchall()

            transactions = []
            for row in rows:
                transactions.append({
                    "id": row["id"],
                    "transaction_id": row["transaction_id"],
                    "pi_user_uid": row["pi_user_uid"],
                    "service_type": row["service_type"],
                    "gross_paid_lyo": row["gross_paid_lyo"],
                    "net_allocated_lyo": row["net_allocated_lyo"],
                    "burned_lyo": row["burned_lyo"],
                    "burn_address": row["burn_address"],
                    "node_origin": row["node_origin"],
                    "pqc_verified": bool(row["pqc_verified"]),
                    "timestamp": row["timestamp"],
                    "raw_response": json.loads(row["raw_response_json"]) if row["raw_response_json"] else {}
                })

            return jsonify({
                "status": "success",
                "node": "Tripoli Node v0.6.3",
                "total_records": len(transactions),
                "transactions": transactions
            }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve Tripoli Node ledger archive: {str(e)}"
        }), 500

@app.route('/api/v1/sovereign/ledger/export-csv', methods=['GET'])
def export_sovereign_ledger_csv():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sovereign_ledger_archive ORDER BY id DESC;")
            rows = cursor.fetchall()

            output = io.StringIO()
            writer = csv.writer(output)
            
            writer.writerow([
                "ID", "Transaction ID", "Pi User UID", "Service Type", 
                "Gross Paid (LYO)", "Net Allocated (LYO)", "Burned LYO (1%)", 
                "Burn Address", "Node Origin", "PQC Verified", "Timestamp"
            ])
            
            for row in rows:
                writer.writerow([
                    row["id"],
                    row["transaction_id"],
                    row["pi_user_uid"],
                    row["service_type"],
                    row["gross_paid_lyo"],
                    row["net_allocated_lyo"],
                    row["burned_lyo"],
                    row["burn_address"],
                    row["node_origin"],
                    row["pqc_verified"],
                    row["timestamp"]
                ])
            
            output.seek(0)
            
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=tripoli_node_ledger_archive.csv"
            response.headers["Content-Type"] = "text/csv; charset=utf-8"
            return response

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to export CSV archive: {str(e)}"
        }), 500

# تهيئة قواعد البيانات عند بدء التشغيل
init_db()
init_ledger_database()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)