import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import datetime

load_dotenv()
PORT = int(os.getenv("DASHBOARD_PORT", "8000"))

# Cloud Deployment Specifics
CLOUD_MODE = os.getenv("CLOUD_MODE", "false").lower() == "true"
AETHERSHELF_CLOUD_API_KEY = os.getenv("AETHERSHELF_CLOUD_API_KEY", "secure_claw_live_demo_123")
cloud_ledger_cache = []
last_heartbeat = None

app = FastAPI(title="AetherShelf API Bridge - OpenClaw 2026.4.27")

# ── CORS: allow requests from any origin (Pinggy tunnel, local LAN, etc.) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import ledger_handler
from flux_engine import calculate_days_remaining, parse_expiry, get_decay_days, TODAY
from network_check import get_local_ip, check_ngrok_status

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AetherShelf | Autonomous Pantry Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
</head>
<body class="bg-gray-900 text-white p-6 font-sans">
    <div id="app" class="max-w-7xl mx-auto space-y-6">
        <!-- Header: Heavy OpenClaw Emphasis -->
        <div class="flex flex-col md:flex-row justify-between items-center border-b border-gray-700 pb-4">
            <div>
                <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">AetherShelf: Autonomous Pantry Intelligence</h1>
                <p class="text-gray-400 font-mono text-sm mt-1">Powered by OpenClaw Framework v2026.4.27 Gateway</p>
            </div>
            <div class="flex flex-wrap gap-4 mt-4 md:mt-0 items-center">
                <button @click="copyLink" class="bg-blue-600 hover:bg-blue-500 px-5 py-2 rounded font-bold shadow-lg transition flex items-center space-x-2">
                    <span>📋 Copy Public Link</span>
                </button>
                <button @click="triggerDemo" class="bg-purple-600 hover:bg-purple-500 px-6 py-2 rounded font-bold shadow-lg shadow-purple-500/30 transition">⚡ Trigger OpenClaw Autonomous Loop</button>
            </div>
        </div>

        <!-- Network & System Status Banner -->
        <div class="flex flex-col md:flex-row space-y-3 md:space-y-0 md:space-x-4">
            <div class="flex-1 bg-gray-800 border border-gray-700 rounded p-4 flex items-center shadow-lg">
                <div class="flex items-center space-x-3">
                    <div class="w-4 h-4 rounded-full transition-all duration-500" 
                         :class="network.heartbeat_active ? 'bg-green-500 animate-pulse shadow-[0_0_12px_#22c55e]' : 'bg-red-500 shadow-[0_0_12px_#ef4444]'"></div>
                    <span class="font-bold text-gray-300 text-lg">System Status: 
                        <span :class="network.heartbeat_active ? 'text-green-400' : 'text-red-400'">
                            {{ network.heartbeat_active ? 'Connected (Local Agent Heartbeat Synchronized)' : 'Disconnected (Awaiting Cloud Sync from OpenClaw)' }}
                        </span>
                    </span>
                </div>
            </div>
        </div>

        <!-- Human in the Loop (Alerts) -->
        <div v-if="alerts.length > 0" class="bg-red-900/50 border border-red-500 rounded p-5 shadow-xl">
            <h3 class="text-xl font-bold mb-4 flex items-center text-red-200">
                <span class="mr-2">🚨</span> OpenClaw Gateway: Human-in-the-Loop Interventions
            </h3>
            <div v-for="alert in alerts" :key="alert.id" class="flex flex-col md:flex-row justify-between items-center mb-3 bg-red-950/80 p-4 rounded border border-red-800">
                <div class="font-medium text-red-100 mb-3 md:mb-0">
                    <span v-if="alert.type === 'restock'" class="bg-red-700 text-xs px-2 py-1 rounded mr-2 uppercase tracking-wide">SMS Alert</span>
                    <span v-if="alert.type === 'collision'" class="bg-orange-600 text-xs px-2 py-1 rounded mr-2 uppercase tracking-wide">CollisionDetection.skill</span>
                    <span v-if="alert.type === 'utility_gap'" class="bg-blue-600 text-xs px-2 py-1 rounded mr-2 uppercase tracking-wide">UtilityGapFinder.skill</span>
                    {{ alert.message }}
                </div>
                <button v-if="alert.type === 'restock'" @click="confirmPurchase(alert.item)" class="bg-green-600 hover:bg-green-500 text-white px-5 py-2 rounded shadow transition font-bold whitespace-nowrap">✓ Confirm Purchase</button>
            </div>
        </div>

        <!-- Graphs and Ledger -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Dynamic Flux Visualization -->
            <div class="bg-gray-800 p-5 rounded-lg shadow-xl border border-gray-700">
                <h2 class="text-xl font-semibold mb-2 text-gray-200">Dynamic Flux Visualization (Entropy Curve)</h2>
                <p class="text-sm text-gray-400 mb-4">Tracking Utility Gaps via OpenClaw FluxAlgorithm.skill</p>
                <div id="plotlyChart" class="w-full h-80"></div>
            </div>

            <!-- Live Ledger -->
            <div class="bg-gray-800 p-5 rounded-lg shadow-xl border border-gray-700 flex flex-col h-full">
                <h2 class="text-xl font-semibold mb-2 text-gray-200">Live Ledger View</h2>
                <p class="text-sm text-gray-400 mb-4">Remote Agent Synchronization (pantry_ledger.yaml)</p>
                <div class="overflow-y-auto flex-1 bg-gray-900 rounded border border-gray-700 max-h-80">
                    <table class="w-full text-left table-auto">
                        <thead class="sticky top-0 bg-gray-700 text-gray-300">
                            <tr>
                                <th class="p-3">Item</th>
                                <th class="p-3">Quantity</th>
                                <th class="p-3">Days Remaining</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in ledger" :key="item.name" class="border-b border-gray-800 hover:bg-gray-800 transition">
                                <td class="p-3 font-medium">{{ item.name }}</td>
                                <td class="p-3 font-mono text-gray-300">{{ item.quantity }}</td>
                                <td class="p-3 font-bold" :class="{'text-red-400': item.days < 3, 'text-green-400': item.days >= 3}">
                                    {{ item.days }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Agent Logs -->
        <div class="bg-gray-800 p-5 rounded-lg shadow-xl border border-gray-700 flex flex-col h-72">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold text-gray-200">OpenClaw Agent Logs (Chain of Thought)</h2>
                <span class="px-2 py-1 bg-green-900 text-green-400 text-xs rounded border border-green-700">Streaming openclaw_session.log</span>
            </div>
            <div class="flex-1 bg-black p-4 rounded border border-gray-900 font-mono text-sm overflow-y-auto whitespace-pre-wrap text-green-500 shadow-inner" id="logTerminal">{{ logs }}</div>
        </div>
    </div>

    <script>
        const { createApp, ref, onMounted } = Vue;

        createApp({
            setup() {
                const ledger = ref([]);
                const logs = ref("");
                const alerts = ref([]);
                const network = ref({ local_url: "", public_active: false, heartbeat_active: false });
                
                const drawChart = (items) => {
                    if (!items || items.length === 0) return;
                    
                    const traces = [];
                    const dates = [];
                    for (let i = 0; i < 8; i++) {
                        const d = new Date();
                        d.setDate(d.getDate() + i);
                        dates.push(d.toISOString().split('T')[0]);
                    }

                    items.forEach(item => {
                        if (item.quantity > 0) {
                            const y_values = [];
                            for(let i=0; i<8; i++) {
                                y_values.push(Math.max(0, item.days - i));
                            }
                            traces.push({
                                x: dates,
                                y: y_values,
                                mode: 'lines+markers',
                                name: item.name,
                                line: { width: 3 },
                                marker: { size: 8 }
                            });
                        }
                    });

                    const layout = {
                        paper_bgcolor: 'rgba(0,0,0,0)',
                        plot_bgcolor: 'rgba(0,0,0,0)',
                        font: { color: '#9ca3af' },
                        margin: { l: 40, r: 20, t: 20, b: 40 },
                        xaxis: { showgrid: false },
                        yaxis: { showgrid: true, gridcolor: '#374151', title: 'Freshness' },
                        shapes: [
                            {
                                type: 'line',
                                x0: dates[0], x1: dates[dates.length-1],
                                y0: 2, y1: 2,
                                line: { color: 'rgba(239, 68, 68, 0.8)', width: 2, dash: 'dash' }
                            },
                            {
                                type: 'rect',
                                xref: 'x', yref: 'y',
                                x0: dates[0], x1: dates[dates.length-1],
                                y0: 0, y1: 2,
                                fillcolor: 'rgba(239, 68, 68, 0.1)',
                                line: { width: 0 },
                                layer: 'below'
                            }
                        ]
                    };

                    Plotly.react('plotlyChart', traces, layout, {displayModeBar: false, responsive: true});
                };

                const fetchData = async () => {
                    try {
                        const res = await fetch('/api/state');
                        const data = await res.json();
                        ledger.value = data.ledger;
                        logs.value = data.logs;
                        alerts.value = data.alerts;
                        network.value = data.network;
                        
                        drawChart(data.ledger);
                        
                        const term = document.getElementById('logTerminal');
                        if (term && Math.abs(term.scrollHeight - term.scrollTop - term.clientHeight) < 50) {
                            term.scrollTop = term.scrollHeight;
                        }
                    } catch (e) {
                        console.error("Sync error:", e);
                    }
                };

                const triggerDemo = async () => {
                    try {
                        await fetch('/api/trigger-demo', { method: 'POST' });
                        alert("OpenClaw Autonomous Loop triggered! Check the Agent Logs.");
                    } catch (e) {
                        alert("Error triggering demo.");
                    }
                };

                const copyLink = async () => {
                    try {
                        const res = await fetch('/api/public-url');
                        const data = await res.json();
                        if(data.url) {
                            await navigator.clipboard.writeText(data.url);
                            alert("Copied public link to clipboard:\\n" + data.url + "\\n\\nBasic Auth: admin / secret");
                        } else {
                            alert("Public tunnel is not active yet. Please run start_public_link.py");
                        }
                    } catch (e) {
                        alert("Error copying link.");
                    }
                };

                const confirmPurchase = async (itemName) => {
                    try {
                        await fetch('/api/update-inventory', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ item_name: itemName, quantity: 1 })
                        });
                        await fetchData();
                    } catch (e) {
                        alert("Error communicating with OpenClaw Gateway.");
                    }
                };

                onMounted(() => {
                    fetchData();
                    setInterval(fetchData, 3000);
                });

                return { ledger, logs, alerts, network, triggerDemo, copyLink, confirmPurchase };
            }
        }).mount('#app');
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    return HTMLResponse(content=HTML_TEMPLATE, status_code=200)

class SyncData(BaseModel):
    ledger: list

@app.post("/api/update")
def sync_ledger(request: Request, data: SyncData):
    """Secure Webhook Endpoint for Remote Agent Sync"""
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {AETHERSHELF_CLOUD_API_KEY}":
        raise HTTPException(status_code=401, detail="SecureClaw Authentication Failed")
        
    global cloud_ledger_cache, last_heartbeat
    cloud_ledger_cache = data.ledger
    last_heartbeat = datetime.datetime.now()
    return {"status": "success", "message": "Cloud ledger synced via Webhook"}

@app.get("/api/state")
def get_state():
    global cloud_ledger_cache, last_heartbeat
    
    if CLOUD_MODE:
        items = cloud_ledger_cache
        heartbeat_active = last_heartbeat is not None and (datetime.datetime.now() - last_heartbeat).seconds < 300
    else:
        ledger_path = ROOT_DIR / "pantry_ledger.yaml"
        items = ledger_handler.load_ledger(ledger_path)
        heartbeat_active = True # Local mode always assumes direct sync is active
    
    formatted_ledger = []
    alerts = []
    
    network = {
        "local_url": f"http://{get_local_ip()}:{PORT}",
        "public_active": CLOUD_MODE, # Always true if in cloud
        "heartbeat_active": heartbeat_active
    }
    
    for item in items:
        name = item.get("name", "Unknown")
        qty = int(item.get("quantity", 0))
        expiry_date = parse_expiry(item.get("estimated_expiry"))
        
        if not expiry_date:
            decay = get_decay_days(name)
            expiry_date = TODAY + datetime.timedelta(days=decay)
            
        days = calculate_days_remaining(expiry_date)
        
        formatted_ledger.append({
            "name": name,
            "quantity": qty,
            "days": days
        })
        
        # OpenClaw Skill Logic Integrations
        if days < 3 and qty > 0:
            alerts.append({
                "id": f"{name}_restock",
                "type": "restock",
                "item": name,
                "message": f"⚠️ AetherShelf Alert: Based on your consumption flux, you will run out of {name} in {days} days. Should I add this to your list?"
            })
            
            if "spinach" in name.lower():
                alerts.append({
                    "id": f"{name}_gap",
                    "type": "utility_gap",
                    "item": name,
                    "message": f"Buy $1 of cream to make Creamed Spinach—this unlocks 80% of your current expiring inventory."
                })
            elif "milk" in name.lower() or "bread" in name.lower():
                alerts.append({
                    "id": f"{name}_collision",
                    "type": "collision",
                    "item": name,
                    "message": f"Collision detected! You already have {name} that expires in {days} days. Do you really need to buy more?"
                })
            
    # Load Logs
    log_path = ROOT_DIR / "openclaw_session.log"
    logs = "Awaiting OpenClaw logs..."
    if log_path.exists():
        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            logs = "".join(lines[-50:])
            
    # Compute entropy score (average days remaining across non-zero items)
    active_items = [i for i in formatted_ledger if i["quantity"] > 0]
    entropy_score = round(sum(i["days"] for i in active_items) / len(active_items), 1) if active_items else 0.0

    return {
        "status": "active",
        "entropy_score": entropy_score,
        "ledger": formatted_ledger,
        "logs": logs,
        "alerts": alerts,
        "network": network
    }

@app.get("/api/public-url")
def get_public_url():
    url_file = ROOT_DIR / "public_url.txt"
    if url_file.exists():
        with open(url_file, "r") as f:
            url = f.read().strip()
            return {"url": url}
    return {"url": None}

class InventoryUpdate(BaseModel):
    item_name: str
    quantity: int

@app.post("/api/update-inventory")
def update_inventory(update: InventoryUpdate):
    skill_main = ROOT_DIR / "pantry_intel.skill" / "main.py"
    if skill_main.exists():
        spec = importlib.util.spec_from_file_location("pantry_intel_skill", str(skill_main))
        pantry_intel = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pantry_intel)
        skill = pantry_intel.PantryIntelSkill()
        result = skill.update_inventory(update.item_name, update.quantity)
    else:
        result = ledger_handler.add_item(update.item_name, update.quantity, None, ROOT_DIR / "pantry_ledger.yaml")
    return {"status": "success", "result": result}

@app.post("/api/trigger-demo")
def trigger_demo():
    demo_script = ROOT_DIR / "demo_mode.sh"
    if demo_script.exists():
        subprocess.Popen(["bash", str(demo_script)])
        return {"status": "Demo triggered successfully"}
    
    demo_script_py = ROOT_DIR / "agent_internal_reasoning.py"
    if demo_script_py.exists():
        subprocess.Popen([sys.executable, str(demo_script_py)])
        return {"status": "Python CoT Demo triggered successfully"}
        
    raise HTTPException(status_code=404, detail="Demo scripts not found")

# ── Push Notification Stubs (for PWA frontend compatibility) ─────────────
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "")
push_subscribers: list = []

@app.get("/api/push/vapid-public-key")
def get_vapid_key():
    return {"vapid_public_key": VAPID_PUBLIC_KEY}

class PushSubscription(BaseModel):
    endpoint: str
    keys: dict

@app.post("/api/push/subscribe")
def push_subscribe(sub: PushSubscription):
    global push_subscribers
    # Deduplicate by endpoint
    push_subscribers = [s for s in push_subscribers if s["endpoint"] != sub.endpoint]
    push_subscribers.append({"endpoint": sub.endpoint, "keys": sub.keys})
    return {"status": "subscribed", "total": len(push_subscribers)}

@app.post("/api/push/test")
def push_test():
    return {"status": "sent", "subscribers": len(push_subscribers)}

# ── Serve PWA static files from /public ──────────────────────────────────
PUBLIC_DIR = ROOT_DIR / "public"
if PUBLIC_DIR.exists():
    app.mount("/public", StaticFiles(directory=str(PUBLIC_DIR)), name="public")
    # Redirect root to the PWA frontend (better UX than the raw HTML template)
    @app.get("/pwa", response_class=HTMLResponse)
    def get_pwa():
        return FileResponse(str(PUBLIC_DIR / "index.html"))

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  AetherShelf Sentinel — Starting...")
    print(f"  Local:   http://localhost:{PORT}")
    print(f"  Network: http://0.0.0.0:{PORT}")
    print(f"  PWA UI:  http://localhost:{PORT}/pwa")
    print(f"{'='*60}\n")
    uvicorn.run("api_bridge:app", host="0.0.0.0", port=PORT, reload=False)
