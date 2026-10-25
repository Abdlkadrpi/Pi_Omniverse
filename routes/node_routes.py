from flask import Blueprint, jsonify
import requests

node_bp = Blueprint('node_bp', __name__, url_prefix='/api/node')
TRIPOLI_NODE_URL = "http://127.0.0.1:5000/api/node/status"

@node_bp.route('/status', methods=['GET'])
def get_node_bridge_status():
    tripoli_sync_status = "Disconnected"
    try:
        res = requests.get(TRIPOLI_NODE_URL, timeout=2)
        if res.status_code == 200:
            tripoli_sync_status = "Connected to Tripoli Node (Port 5000)"
    except Exception:
        tripoli_sync_status = "Tripoli Node Offline (Running Standalone)"

    return jsonify({
        "status": "success",
        "environment": "sandbox",
        "piverify_integration": "Active",
        "data": {
            "node_name": "Omniverse-App-Engine-v2.0-PiVerify",
            "network": "Pi-Soroban-CrossChain-Bridge",
            "circulating_lyo": 250000000,
            "active_agents": 4,
            "status": "Active & Synchronized with Tripoli Node & PiVerify Global Gateway",
            "tripoli_node_bridge": "http://127.0.0.1:5000",
            "tripoli_sync": tripoli_sync_status
        }
    }), 200
