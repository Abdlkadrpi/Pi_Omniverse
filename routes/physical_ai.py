# routes/physical_ai.py
import sqlite3
import datetime
from flask import Blueprint, request, jsonify

physical_ai_bp = Blueprint('physical_ai', __name__)

DB_PATH = 'assets.db'

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# إنشاء جدول الفعاليات الفيزيائية والمستشعرات إذا لم يكن موجوداً
def init_physical_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS physical_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            payload_data TEXT NOT NULL,
            prism_audit_status TEXT NOT NULL,
            lyo_fee REAL DEFAULT 1.0,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_physical_db()

@physical_ai_bp.route('/api/v1/physical/telemetry', methods=['POST'])
def process_physical_telemetry():
    """
    استقبال البيانات الفيزيائية من المستشعرات/الأجهزة المادية،
    فحصها عبر وكيل PRISM، وتوثيقها في المنظومة مقابل LYO.
    """
    data = request.get_json()
    
    if not data or 'device_id' not in data or 'payload' not in data:
        return jsonify({
            "status": "error",
            "message": "بيانات الجهاز أو الحمولة الفيزيائية مفقودة"
        }), 400

    device_id = data.get('device_id')
    sensor_type = data.get('sensor_type', 'generic_sensor')
    payload = str(data.get('payload'))
    user_pi_uid = data.get('pi_uid', 'ANONYMOUS_PHYSICAL_NODE')

    # 1. محاكاة فحص التدقيق الحارس (PRISM Guardrail Audit) للبيانات الفيزيائية
    prism_passed = True
    audit_status = "PASSED_PRISM_PHYSICAL_AUDIT"
    
    # فحص بسيط للقيم المشبوهة أو الضوضاء في البيانات المادية
    if "override_danger" in payload.lower():
        prism_passed = False
        audit_status = "REJECTED_PRISM_SAFETY_VIOLATION"

    if not prism_passed:
        return jsonify({
            "status": "rejected",
            "reason": audit_status,
            "message": "تم رفض الإشارة الفيزيائية بواسطة وكيل PRISM لحماية المنظومة"
        }), 403

    # 2. خصم رسوم المعالجة والتوثيق المادي بعملة LYO
    lyo_fee = 1.0
    
    # 3. توثيق الحدث المادي في قاعدة البيانات assets.db
    timestamp = datetime.datetime.utcnow().isoformat()
    query_db('''
        INSERT INTO physical_events (device_id, sensor_type, payload_data, prism_audit_status, lyo_fee, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (device_id, sensor_type, payload, audit_status, lyo_fee, timestamp))

    return jsonify({
        "status": "success",
        "message": "تم استقبال وتوثيق الإشارة الفيزيائية بنجاح في عقدة طرابلس ومنصة أومني فيرس",
        "data": {
            "device_id": device_id,
            "sensor_type": sensor_type,
            "prism_audit": audit_status,
            "lyo_charged": lyo_fee,
            "timestamp": timestamp
        }
    }), 200