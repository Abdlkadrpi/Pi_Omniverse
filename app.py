import os
import sqlite3
from flask import Flask, jsonify, render_template

from routes.lyo_routes import lyo_bp
from routes.node_routes import node_bp
from routes.agent_routes import agent_bp

app = Flask(__name__)

# تسجيل جميع المسارات المعيارية (Blueprints)
app.register_blueprint(lyo_bp)
app.register_blueprint(node_bp)
app.register_blueprint(agent_bp)

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
    return jsonify({"status": "healthy", "architecture": "Flask Blueprints Modular - Zero Error"}), 200

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)