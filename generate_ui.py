import os

def generate_dashboard():
    dashboard_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://sdk.minepi.com/pi-sdk.js"></script>
    <title>OMNIVERSE HUB | TRIPOLI</title>
</head>
<body class="bg-slate-950 text-slate-100 font-sans">
    <div class="max-w-5xl mx-auto p-6">
        <header class="flex justify-between items-center mb-10 border-b border-slate-800 pb-6">
            <h1 class="text-3xl font-bold text-yellow-500">OMNIVERSE <span class="text-white">HUB</span></h1>
            <button id="authBtn" onclick="connectPi()" class="bg-yellow-500 text-black px-6 py-2 rounded-full font-bold">CONNECT PI</button>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
                <h2 class="text-xl mb-4 text-slate-400">My Assets</h2>
                <div id="assetsList" class="text-sm italic">Connect to view assets...</div>
                <button onclick="registerAsset()" class="mt-4 w-full bg-slate-800 py-2 rounded-lg hover:bg-slate-700">+ Register New Asset</button>
            </div>

            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 md:col-span-2">
                <h2 class="text-xl mb-4 text-slate-400">Social Graph</h2>
                <div id="socialList" class="text-sm">Network nodes active...</div>
            </div>
        </div>
    </div>

    <script>
        async function connectPi() {
            const auth = await Pi.authenticate(['username'], (s) => console.log(s), (u) => alert("Welcome: " + u.user.username));
        }

        async function registerAsset() {
            const name = prompt("Asset Name (e.g. Tripoli Property):");
            const value = prompt("Value in PI:");
            const res = await fetch('/api/register_asset', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name, value, owner: "User"})
            });
            const data = await res.json();
            alert(data.message);
            location.reload();
        }
    </script>
</body>
</html>
    """
    os.makedirs('ui', exist_ok=True)
    with open("ui/index.html", "w", encoding="utf-8") as f:
        f.write(dashboard_code)
    print("[+] Dashboard UI generated successfully.")

if __name__ == "__main__":
    generate_dashboard()
"""