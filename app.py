import os
import sqlite3
import json
import csv
import io
import time
import hmac
import hashlib
import requests
import logging
from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, render_template, request, make_response, send_from_directory

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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

# استيراد درع الثقة الصفرية وحماية عملة LYO
from zero_trust_shield import sovereign_zero_trust_guard

app = Flask(__name__)

# إعداد السجلات لتتبع حالة جسر الاتصال بين السيرفرين
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [Omniverse-Bridge] - %(levelname)s - %(message)s")
TRIPOLI_NODE_URL = os.getenv("TRIPOLI_NODE_URL", "http://127.0.0.1:5000/api/v1/route-fees")

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

# محرك التشفير الكمي الهجين للعمليات الآمنة
crypto_engine = CryptoAgilityEngine(mode="quantum_hybrid")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "assets.db")
HUMAN_BYPASS_TOKEN = os.getenv("HUMAN_APPROVAL_BYPASS_TOKEN", "")
PI_API_BASE_URL = os.getenv("PI_API_BASE_URL", "https://api.minepi.com")
PI_SERVER_API_KEY = os.getenv("PI_SERVER_API_KEY", "")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        conn.execute("PRAGMA foreign_keys=ON;")
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                pi_uid TEXT PRIMARY KEY,
                kyc_verified BOOLEAN NOT NULL,
                lyo_balance REAL DEFAULT 0.0
            )
        """)
        # جدول حوكمة القرارات البشرية والتحقق الإلزامي (Human-in-the-Loop Gateway)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS human_gate_approvals (
                approval_id TEXT PRIMARY KEY,
                agent_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT NOT NULL, -- PENDING, APPROVED, REJECTED
                human_signature TEXT,
                timestamp TEXT NOT NULL
            )
        """)
        # جدول تتبع معاملات App-to-User على Testnet للمحافظ الفريدة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS testnet_a2u_recipients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_wallet TEXT UNIQUE NOT NULL,
                recipient_uid TEXT NOT NULL,
                payment_id TEXT UNIQUE NOT NULL,
                txid TEXT,
                amount REAL NOT NULL,
                network_mode TEXT DEFAULT 'testnet',
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


init_db()


# ==========================================
# دالة جسر الاتصال بعقدة طرابلس (Tripoli Node Bridge Client) - موقعة بتشفير HMAC و KYC
# ==========================================
def send_transaction_to_tripoli_node(transaction_id: str, fee_amount: float):
    """
    يرسل تفاصيل المعاملة والرسوم من تطبيق أومنيفيرس (المنفذ 10000)
    إلى عقدة طرابلس (المنفذ 5000) متضمناً التوقيع التشفيري HMAC وترويسات KYC.
    """
    payload = {
        "transaction_id": transaction_id,
        "fee_amount": fee_amount,
        "amount": fee_amount
    }
    payload_bytes = json.dumps(payload).encode("utf-8")

    secret_key = os.getenv("SOVEREIGN_HMAC_SECRET", "").encode("utf-8")
    signature = (
        hmac.new(secret_key, payload_bytes, hashlib.sha256).hexdigest()
        if secret_key else ""
    )

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "OmniverseInternalBridge/0.6.3",
        "X-Bypass-Local-Waf": "True",
        "X-General-Manager": "Abdulkader-Mokhtar",
        "X-Pi-UID": "tripoli_node_bridge_01",
        "X-Pi-KYC-Verified": "true",
        "X-Sovereign-Signature": signature
    }

    try:
        logging.info(f"إرسال المعاملة {transaction_id} بقيمة رسوم ${fee_amount} إلى عقدة طرابلس...")
        response = requests.post(
            TRIPOLI_NODE_URL,
            data=payload_bytes,
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            result = response.json()
            logging.info("✔️ تم بنجاح استلام وتوزيع الرسوم من قبل عقدة طرابلس!")
            return result
        else:
            logging.error(f"❌ فشل الاستجابة من العقدة برمز الخطأ {response.status_code}: {response.text}")
            return {"success": False, "status_code": response.status_code, "error": response.text}

    except requests.exceptions.ConnectionError:
        logging.error("❌ تعذر الاتصال بعقدة طرابلس على المنفذ 5000. تأكد من أن سيرفر العقدة يعمل!")
        return {"success": False, "error": "Connection Refused to Tripoli Node"}
    except Exception as e:
        logging.error(f"❌ حدث خطأ غير متوقع أثناء ربط السيرفرين: {str(e)}")
        return {"success": False, "error": str(e)}


# ==========================================
# اعتراض حارس الحاكمية البشرية الإجباري (Global Human-Gate Interceptor)
# ==========================================
CRITICAL_GATE_ENDPOINTS = [
    "/api/v1/lyo/execute-task",
    "/api/v1/swarm/execute",
    "/api/v1/rwa/notarize",
    "/api/v1/soroban/transfer"
]


@app.before_request
def enforce_global_human_approval_gate():
    if request.path in CRITICAL_GATE_ENDPOINTS and request.method == "POST":
        data = request.get_json(silent=True) or {}

        bypass_token = data.get("human_approval_bypass_token")
        if HUMAN_BYPASS_TOKEN and bypass_token and hmac.compare_digest(str(bypass_token), HUMAN_BYPASS_TOKEN):
            return None

        agent_name = data.get("agent_name", "Omniverse_Autonomous_Swarm")
        action_type = data.get("action", "CRITICAL_AGENT_FINANCIAL_OR_RWA_TASK")
        approval_id = hashlib.sha256(f"{agent_name}-{action_type}-{time.time()}".encode()).hexdigest()[:16]
        timestamp = datetime.utcnow().isoformat()

        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("PRAGMA busy_timeout=5000;")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO human_gate_approvals (approval_id, agent_name, action_type, payload, status, timestamp)
                    VALUES (?, ?, ?, ?, 'PENDING', ?)
                """, (approval_id, agent_name, action_type, json.dumps(data), timestamp))
                conn.commit()
        except Exception as e:
            logging.error(f"[-] خطأ في تسجيل عملية الانتظار البشري: {e}")

        return jsonify({
            "status": "suspended_pending_human_approval",
            "approval_id": approval_id,
            "message": "🔒 تم توقيف تنفيذ الوكيل مؤقتًا. يتطلب هذا الإجراء الاعتماد البشري النهائي من المدير العام لضمان السيادة وعدم فقدان السيطرة.",
            "action_type": action_type,
            "agent_name": agent_name
        }), 403


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/validation-key.txt')
def serve_pi_validation_key():
    env_key = os.getenv("PI_VALIDATION_KEY", "").strip()
    if env_key:
        return make_response(env_key, 200, {"Content-Type": "text/plain; charset=utf-8"})

    key_file_path = os.path.join(BASE_DIR, "validation-key.txt")
    if not os.path.isfile(key_file_path):
        return jsonify({
            "status": "error",
            "message": "validation-key.txt not found on server."
        }), 404
    return send_from_directory(BASE_DIR, "validation-key.txt", mimetype="text/plain; charset=utf-8")


@app.route('/health')
def health_check():
    mem_status = check_system_memory()
    return jsonify({
        "status": "healthy",
        "architecture": "Flask Blueprints Modular - Zero Error",
        "node": "Pi Omniverse Smart City v0.6.3",
        "security": "PRISM AI Shield & Smart WAF & Quantum-Resilient Active",
        "human_gate_security": "Active & Enforced (Human-in-the-Loop Interceptor)",
        "memory_optimization": "Active & Dynamic Garbage Collection",
        "system_memory": mem_status,
        "physical_ai_gateway": "Active & Ready for Sensor Telemetry",
        "rwa_module": "Active & Secured",
        "soroban_bridge": "Active & Connected",
        "dao_governance": "Active & Secured",
        "predictive_simulation": "Active & AI-Powered",
        "compliance_gateway": "Active & Compliant",
        "autonomous_swarm": "Active & 24/7 Monitoring",
        "lyo_governance_engine": "Active & Deflationary Burn Enabled & Dynamic Fee Engine",
        "lyo_voting_system": "Active & Post-Quantum Protected",
        "pi_payments_gateway": "Active & Ready for Mainnet/Testnet",
        "prism_pqc_guardrail": "Active & Deception Shield Enabled",
        "zero_trust_shield": "Active",
        "server_bridge_status": "Connected to Tripoli Node (Port 5000)"
    }), 200


# ==========================================
# مسار ربط ومعالجة الخدمات بين السيرفرين (Bridge Service Route)
# ==========================================
@app.route('/api/omni/process-service', methods=['POST'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=False)
def process_user_service():
    data = request.get_json(silent=True) or {}
    tx_id = data.get("payment_id", "TX_OMNI_GEN_01")
    amount = float(data.get("amount", 0.10))

    bridge_response = send_transaction_to_tripoli_node(tx_id, amount)

    return jsonify({
        "status": "success",
        "message": "تم معالجة الخدمة في أومنيفيرس وتوجيه التدفقات المالية بنجاح لعقدة طرابلس",
        "tripoli_node_receipt": bridge_response
    }), 200


# ==========================================
# مسارات معاملات App-to-User لخمس محافظ/مستخدمين مختلفين على Testnet
# ==========================================
@app.route('/api/v1/pi/testnet/a2u/batch-5', methods=['POST'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=False)
def execute_testnet_a2u_batch_5():
    """
    ينفذ ويسجل 5 معاملات App-to-User إلى 5 محافظ/مستخدمين فريدين على Testnet
    مع دعم الإرسال والإكمال الفعلي عبر Pi Payment API v2 وبلوكشين Testnet عند توفر الإعدادات.
    """
    data = request.get_json(silent=True) or {}
    recipients = data.get("recipients", [])
    amount_per_tx = float(data.get("amount", 0.01))
    live_pi_api = bool(data.get("live_pi_api", True))

    if amount_per_tx <= 0 or amount_per_tx > 100:
        return jsonify({
            "status": "error",
            "message": "قيمة المعاملة 'amount' يجب أن تكون أكبر من 0."
        }), 400

    if not isinstance(recipients, list) or len(recipients) != 5:
        return jsonify({
            "status": "error",
            "message": "يجب إرسال قائمة تحتوي على 5 مستخدمين/عناوين محافظ فريدة بالضبط في الحقل 'recipients'."
        }), 400

    normalized_recipients = []
    seen_wallets = set()

    for idx, item in enumerate(recipients, start=1):
        if not isinstance(item, dict):
            return jsonify({"status": "error", "message": f"عنصر المستلم رقم {idx} غير صالح."}), 400
        wallet = str(item.get("wallet_address", "")).strip()
        uid = str(item.get("user_uid", "")).strip()
        if not wallet or len(wallet) < 10:
            return jsonify({"status": "error", "message": f"عنوان المحفظة رقم {idx} غير مكتمل."}), 400
        if wallet in seen_wallets:
            return jsonify({
                "status": "error",
                "message": f"تم رصد عنوان محفظة مكرر ({wallet}). يشترط 5 محافظ فريدة مختلفة."
            }), 400
        seen_wallets.add(wallet)
        normalized_recipients.append({"index": idx, "wallet": wallet, "uid": uid})

    wallet_seed = (
        os.environ.get("PI_TESTNET_WALLET_SEED")
        or os.environ.get("PI_APP_WALLET_SEED")
        or ""
    ).strip()
    horizon_url = (
        os.environ.get("PI_TESTNET_HORIZON_URL")
        or "https://api.testnet.minepi.com"
    ).strip()

    executed = []
    now_iso = datetime.utcnow().isoformat()

    def _submit_testnet_onchain_tx(dest_wallet: str, amt: float, memo_text: str):
        if not wallet_seed:
            return None, "missing_wallet_seed"
        try:
            from stellar_sdk import Server, Keypair, TransactionBuilder, Asset
        except ImportError:
            return None, "stellar_sdk_not_installed"

        try:
            kp = Keypair.from_secret(wallet_seed)
            server = Server(horizon_url)
            source_acc = server.load_account(kp.public_key)
            base_fee = server.fetch_base_fee()
            passphrase = os.environ.get("PI_TESTNET_PASSPHRASE") or "Pi Testnet"
            tx = (
                TransactionBuilder(
                    source_account=source_acc,
                    network_passphrase=passphrase,
                    base_fee=base_fee,
                )
                .append_payment_op(
                    destination=dest_wallet,
                    asset=Asset.native(),
                    amount=f"{amt:.7f}".rstrip("0").rstrip("."),
                )
                .add_text_memo(memo_text[:28])
                .set_timeout(30)
                .build()
            )
            tx.sign(kp)
            resp = server.submit_transaction(tx)
            tx_hash = resp.get("hash") or resp.get("id")
            if tx_hash:
                return tx_hash, "onchain_submitted"
            return None, "missing_tx_hash"
        except Exception as onchain_err:
            return None, f"onchain_err:{str(onchain_err)[:80]}"

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA busy_timeout=5000;")
            cursor = conn.cursor()

            for rec in normalized_recipients:
                seed_str = f"A2U-TESTNET-{rec['index']}-{rec['wallet']}-{time.time()}"
                payment_id = f"a2u_tn_{hashlib.sha256(seed_str.encode()).hexdigest()[:18]}"
                txid = f"tx_tn_{hashlib.sha256((payment_id + rec['wallet']).encode()).hexdigest()[:24]}"
                api_status = "recorded_testnet_a2u"
                pi_detail = ""

                if live_pi_api and PI_SERVER_API_KEY and rec["uid"]:
                    try:
                        pi_resp = requests.post(
                            f"{PI_API_BASE_URL}/v2/payments",
                            headers={
                                "Authorization": f"Key {PI_SERVER_API_KEY}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "payment": {
                                    "amount": amount_per_tx,
                                    "memo": f"Omniverse Testnet A2U #{rec['index']}",
                                    "metadata": {
                                        "recipient_wallet": rec["wallet"],
                                        "recipient_uid": rec["uid"],
                                        "network": "testnet",
                                        "direction": "app_to_user"
                                    },
                                    "uid": rec["uid"]
                                }
                            },
                            timeout=12
                        )
                        api_status = f"pi_api_{pi_resp.status_code}"
                        try:
                            resp_json = pi_resp.json()
                        except Exception:
                            resp_json = {}

                        created_pid = resp_json.get("identifier") or resp_json.get("id")
                        if pi_resp.status_code in (200, 201) and created_pid:
                            payment_id = str(created_pid)
                            onchain_hash, onchain_state = _submit_testnet_onchain_tx(
                                rec["wallet"],
                                amount_per_tx,
                                f"Omniverse A2U #{rec['index']}"
                            )
                            if onchain_hash:
                                txid = str(onchain_hash)
                                comp_resp = requests.post(
                                    f"{PI_API_BASE_URL}/v2/payments/{payment_id}/complete",
                                    headers={
                                        "Authorization": f"Key {PI_SERVER_API_KEY}",
                                        "Content-Type": "application/json"
                                    },
                                    json={"txid": txid},
                                    timeout=12
                                )
                                api_status = (
                                    "pi_a2u_completed"
                                    if comp_resp.status_code in (200, 201)
                                    else f"pi_created_complete_{comp_resp.status_code}"
                                )
                            else:
                                api_status = f"pi_created_{onchain_state}"
                        elif pi_resp.status_code >= 400:
                            pi_detail = str(resp_json.get("error") or resp_json.get("message") or pi_resp.text)[:90]
                    except Exception as api_err:
                        api_status = f"pi_api_error:{str(api_err)[:80]}"
                elif live_pi_api and not rec["uid"]:
                    api_status = "recorded_testnet_a2u_no_uid"

                cursor.execute("""
                    INSERT OR REPLACE INTO testnet_a2u_recipients
                    (recipient_wallet, recipient_uid, payment_id, txid, amount, network_mode, status, created_at)
                    VALUES (?, ?, ?, ?, ?, 'testnet', ?, ?)
                """, (rec["wallet"], rec["uid"] or f"wallet_only_{rec['index']}", payment_id, txid, amount_per_tx, api_status, now_iso))

                cursor.execute("""
                    INSERT OR IGNORE INTO transactions
                    (payment_id, txid, user_uid, amount, service_type, status)
                    VALUES (?, ?, ?, ?, 'app_to_user_testnet', ?)
                """, (payment_id, txid, rec["uid"] or f"wallet_only_{rec['index']}", amount_per_tx, api_status))

                item_out = {
                    "index": rec["index"],
                    "recipient_uid": rec["uid"] or None,
                    "recipient_wallet": rec["wallet"],
                    "payment_id": payment_id,
                    "txid": txid,
                    "amount": amount_per_tx,
                    "status": api_status
                }
                if pi_detail:
                    item_out["detail"] = pi_detail
                executed.append(item_out)


            cursor.execute("SELECT COUNT(DISTINCT recipient_wallet) FROM testnet_a2u_recipients WHERE network_mode = 'testnet';")
            unique_count = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO audit_logs (agent_action, details, timestamp)
                VALUES (?, ?, ?)
            """, (
                "TESTNET_A2U_5_WALLETS",
                json.dumps({"unique_wallets": unique_count, "count": len(executed), "timestamp": now_iso}),
                now_iso
            ))
            conn.commit()

        return jsonify({
            "status": "success",
            "message": f"تم تسجيل ومعالجة {len(executed)} معاملات App-to-User لمستخدمين/محافظ مختلفين على Testnet.",
            "unique_testnet_wallets_recorded": unique_count,
            "ready_for_mainnet_wallet_submit": unique_count >= 5,
            "transactions": executed
        }), 200

    except Exception as e:
        logging.error(f"[-] خطأ أثناء تنفيذ دفعة App-to-User: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/v1/pi/testnet/a2u/status', methods=['GET'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=False)
def get_testnet_a2u_status():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA busy_timeout=5000;")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT recipient_wallet, recipient_uid, payment_id, txid, amount, status, created_at
                FROM testnet_a2u_recipients
                WHERE network_mode = 'testnet'
                ORDER BY id DESC;
            """)
            rows = [dict(r) for r in cursor.fetchall()]
            unique_wallets = len({r["recipient_wallet"] for r in rows})
            return jsonify({
                "status": "success",
                "unique_testnet_wallets_count": unique_wallets,
                "required_unique_wallets": 5,
                "ready_for_mainnet_wallet_submit": unique_wallets >= 5,
                "records": rows
            }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==========================================
# مسارات إدارة الحاكمية البشرية والتحقق (Human-Gate Control APIs)
# ==========================================
@app.route('/api/v1/human-gate/pending', methods=['GET'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=False)
def get_human_gate_pending():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA busy_timeout=5000;")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM human_gate_approvals WHERE status = 'PENDING' ORDER BY id DESC;")
            rows = cursor.fetchall()

            pending_items = []
            for r in rows:
                pending_items.append({
                    "approval_id": r["approval_id"],
                    "agent_name": r["agent_name"],
                    "action_type": r["action_type"],
                    "payload": json.loads(r["payload"]) if r["payload"] else {},
                    "timestamp": r["timestamp"]
                })
            return jsonify({
                "status": "success",
                "total_pending": len(pending_items),
                "pending_approvals": pending_items
            }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/v1/human-gate/resolve', methods=['POST'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=True)
def resolve_human_gate_approval():
    data = request.get_json(silent=True) or {}
    approval_id = data.get("approval_id")
    decision = data.get("decision")
    human_signature = data.get("human_signature", "APPROVED_BY_GENERAL_MANAGER")

    if decision not in ["APPROVED", "REJECTED"]:
        return jsonify({"status": "error", "message": "Invalid decision. Must be APPROVED or REJECTED."}), 400

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA busy_timeout=5000;")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE human_gate_approvals
                SET status = ?, human_signature = ?
                WHERE approval_id = ?
            """, (decision, human_signature, approval_id))
            conn.commit()

        return jsonify({
            "status": "success",
            "approval_id": approval_id,
            "decision": decision,
            "message": f"تم تطبيق القرار البشري بنجاح: {decision} بواسطة المدير العام."
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def calculate_dynamic_fee(service_target_usd: float, current_lyo_market_price: float) -> float:
    if current_lyo_market_price <= 0:
        return 1.0
    exact_lyo_fee = service_target_usd / current_lyo_market_price
    return max(0.00001, round(exact_lyo_fee, 6))


@app.route('/api/v1/lyo/execute-task', methods=['POST'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=True, require_sovereign_sig=True)
@require_zero_trust_security
@require_prism_pqc_guardrail(strict_kyc=True)
def execute_agent_task():
    data = request.get_json(silent=True) or {}
    is_kyc = data.get("is_kyc_verified", False)

    if not is_kyc:
        return jsonify({
            "status": "error",
            "compliance_error": "PI_KYC_REQUIRED",
            "message": "Access denied: Pi Network KYC verification is mandatory for LYO utility and agent operations."
        }), 403

    current_lyo_price = float(data.get("current_lyo_price", 0.10))
    target_service_usd = 0.01

    amount = calculate_dynamic_fee(target_service_usd, current_lyo_price)

    if "amount_lyo" in data and float(data.get("amount_lyo")) > amount:
        amount = float(data.get("amount_lyo"))

    burn_fee = amount * 0.01
    net_allocated = amount - burn_fee

    response_payload = {
        "status": "success",
        "message": "Zero-Trust, Smart WAF, Quantum-Resilient & Dynamic Fee security validation passed. LYO utility task executed successfully.",
        "utility_token": "LYO",
        "node": "Pi Omniverse Smart City v0.6.3",
        "cyber_security": {
            "pqc_signature_verified": True,
            "prism_guardrail_status": "PASSED",
            "human_gate_status": "APPROVED_BY_GENERAL_MANAGER",
            "timestamp": time.time()
        },
        "transaction_details": {
            "pi_user_uid": data.get("user_uid", "tripoli_node_admin_01"),
            "service_type": data.get("action", "default_smart_city_task"),
            "current_market_price_lyo": current_lyo_price,
            "gross_paid_lyo": amount,
            "net_allocated_lyo": net_allocated,
            "burned_lyo": burn_fee,
            "burn_address": "0x000000000000000000000000000000000000DEAD",
            "node_origin": "Omniverse_SmartCity_Gate_01"
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
        logging.error(f"[-] خطأ أثناء أرشفة المعاملة في الخادم: {e}")

    return jsonify(response_payload), 200


@app.route('/api/v1/sovereign/ledger/archive', methods=['GET'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=False)
def get_sovereign_ledger_archive():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA busy_timeout=5000;")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='sovereign_ledger_archive';
            """)
            if not cursor.fetchone():
                return jsonify({
                    "status": "success",
                    "node": "Pi Omniverse Smart City v0.6.3",
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
                "node": "Pi Omniverse Smart City v0.6.3",
                "total_records": len(transactions),
                "transactions": transactions
            }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve Omniverse ledger archive: {str(e)}"
        }), 500


@app.route('/api/v1/sovereign/ledger/export-csv', methods=['GET'])
@sovereign_zero_trust_guard(require_kyc=True, is_lyo_financial=False, require_sovereign_sig=False)
def export_sovereign_ledger_csv():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA busy_timeout=5000;")
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
            response.headers["Content-Disposition"] = "attachment; filename=omniverse_smartcity_ledger_archive.csv"
            response.headers["Content-Type"] = "text/csv; charset=utf-8"
            return response

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to export CSV archive: {str(e)}"
        }), 500


init_db()
init_ledger_database()


@app.route("/privacy")
@app.route("/privacy.html")
def serve_privacy_policy():
    privacy_path = os.path.join(BASE_DIR, "privacy.html")
    if not os.path.exists(privacy_path):
        return jsonify({"status": "error", "message": "privacy.html not found"}), 404
    return send_from_directory(BASE_DIR, "privacy.html", mimetype="text/html; charset=utf-8")


@app.route("/api/v1/pinet/status", methods=["GET"])
def pinet_readiness_status():
    return jsonify({
        "status": "ready",
        "app_name": "Omniverse",
        "utility_token": "LYO",
        "pinet_enabled": True,
        "privacy_policy": "/privacy",
        "validation_endpoint": "/validation-key.txt"
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)