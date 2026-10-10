from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# عنوان محرك Ollama المحلي
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # أو النموذج المختار

@app.route('/api/ai/process', methods=['POST'])
def process_ai_request():
    data = request.json
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        result = response.json()
        return jsonify({
            "status": "success",
            "response": result.get("response", ""),
            "source": "local-open-weight"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # التشغيل محلياً على المنفذ 10000 الخاص بالتطوير
    app.run(host='127.0.0.1', port=10000, debug=True)