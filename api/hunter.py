import requests
import json
from http.server import BaseHTTPRequestHandler

# --- MASTER GLOBAL CONFIG ---
SERPER_API_KEY = "6c182913e988a6f03588ca60e4cd657a5fb66300" 
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

def hunt_leads():
    url = "https://google.serper.dev/search"
    
    # STRATEGY: Target "First-Person" buying intent across the whole web
    # We use "-" to block the agents and 'Property Center' corporate ads
    queries = [
        "'I want to buy land' Lagos diaspora 2026 -agent -commission -sqm",
        "site:x.com 'looking for land' Lagos diaspora -promo -ads",
        "site:nairaland.com 'anyone' 'recommend' trusted land developer Lagos",
        "'help me verify' land title Lagos Nigeria forum",
        "site:reddit.com 'invest' Lagos 'real estate' advice",
        "site:facebook.com 'Nigerians in London' OR 'USA' 'buy land' Lagos"
    ]
    
    total_found = 0
    seen_links = set()

    for q in queries:
        payload = json.dumps({
            "q": q, 
            "tbs": "qdr:m", # Fresh leads from the last 30 days
            "num": 10
        })
        headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}

        try:
            response = requests.post(url, headers=headers, data=payload, timeout=20)
            results = response.json()
            
            if "organic" in results:
                for item in results["organic"]:
                    link = item.get("link")
                    snippet = item.get("snippet", "").lower()
                    
                    # SMART FILTER: If it contains agent words, skip it.
                    # This ensures you meet 'Potential Buyers', not 'Potential Competitors'
                    agent_flags = ["commission", "mandate", "direct brief", "per plot", "call for price", "sqm"]
                    if any(word in snippet for word in agent_flags):
                        continue

                    if link and link not in seen_links:
                        message = (
                            "🌍 **GLOBAL BUYER SIGNAL** 🌍\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            f"👤 **Source:** {item.get('title')[:80]}\n"
                            f"💬 **Intent:** \"{item.get('snippet')[:180]}...\"\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            f"🔗 [VIEW DIRECT LEAD]({link})\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            "🚀 *Target: Worldwide Diaspora Intent*"
                        )
                        
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                      json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
                        
                        seen_links.add(link)
                        total_found += 1
                        
                        # Keeping it to 15 high-quality leads per run
                        if total_found >= 15: return total_found
        except:
            continue
            
    return total_found

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        count = hunt_leads()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"Global Scan Complete. Found {count} high-intent individuals.".encode())
        
