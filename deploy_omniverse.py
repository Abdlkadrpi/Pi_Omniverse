import os

def deploy_master_ui():
    full_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://sdk.minepi.com/pi-sdk.js"></script>
    <title>OMNIVERSE HUB | TRIPOLI</title>
</head>
<body class="bg-black text-white font-sans">
    <div class="max-w-4xl mx-auto p-6">
        <header class="flex justify-between items-center py-6">
            <h1 class="text-2xl font-bold text-yellow-500">OMNIVERSE HUB</h1>
            <button id="authBtn" onclick="connectPi()" class="bg-yellow-500 text-black px-4 py-2 rounded-lg font-bold">CONNECT PI</button>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div class="bg-zinc-900 p-6 rounded-xl border border-zinc-800">
                <h2 class="text-sm text-zinc-400 mb-4 uppercase">Asset Tokenization</h2>
                <input id="assetName" placeholder="Asset Name" class="w-full bg-black p-2 mb-2 border border-zinc-700 rounded">
                <input id="assetVal" placeholder="Value (Pi)" class="w-full bg-black p-2 mb-2 border border-zinc-700 rounded">
                <button onclick="registerAsset()" class="w-full bg-blue-600 p-2 rounded">REGISTER ASSET</button>
            </div>
            <div class="bg-zinc-900 p-6 rounded-xl border border-zinc-800">
                <h2 class="text-sm text-zinc-400 mb-4 uppercase">AI Governance</h2>
                <textarea id="aiInput" class="w-full bg-black p-2 mb-2 border border-zinc-700 rounded" placeholder="Consult the Agent..."></textarea>
                <button onclick="askAI()" class="w-full bg-green-600 p-2 rounded">SEND QUERY</button>
                <div id="aiResponse" class="mt-4 text-xs text-zinc-400">Waiting for query...</div>
            </div>
        </div>
    </div>

    <script>
        async function connectPi() {
            const auth = await Pi.authenticate(['username', 'pay'], (s) => console.log(s), (u) => {
                document.getElementById('authBtn').innerText = "LINKED: " + u.user.username;
            });
        }
        async function registerAsset() {
            const name = document.getElementById('assetName').value;
            const value = document.getElementById('assetVal').value;
            const res = await fetch('/api/register_asset', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({name, value, owner: "Citizen"}) });
            const data = await res.json();
            alert(data.message);
        }
        async function askAI() {
            const message = document.getElementById('aiInput').value;
            const res = await fetch('/api/ai_chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message}) });
            const data = await res.json();
            document.getElementById('aiResponse').innerText = data.message;
        }
    </script>
</body>
</html>"""
    with open("ui/index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("[!!!] Surgical deployment complete. UI is now fully integrated with AI and Blockchain engines.")

if __name__ == "__main__":
    deploy_master_ui()