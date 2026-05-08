import requests
import json
from http.server import BaseHTTPRequestHandler

# --- ELITE CONFIGURATION ---
SERPER_API_KEY = "6c182913e988a6f03588ca60e4cd657a5fb66300" 
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

def hunt_leads():
    url = "https://google.serper.dev/search"
    
    # These queries are 'Hardened' to find individuals in the Diaspora
    # We use quotes for exact phrases and the minus sign (-) to remove junk
    queries = [
        "site:nairaland.com 'looking for land' Lagos 'UK' OR 'USA' -politics -visa",
        "site:nairaland.com 'want to buy' Epe OR 'Lekki' 2026 -news -protest",
        "site:nairaland.com 'recommend' 'trusted' developer Lagos",
        "site:x.com 'buy property' Lagos diaspora -politics -visa",
        "site:nairaland.com 'verify' 'Governor Consent' help Lagos",
        "site:facebook.com 'Nigerians in Canada' 'invest' Lagos land"
    ]
    
    total_found = 0
    seen_links = set()

    for q in queries:
        payload = json.dumps({
            "q": q,
            "tbs": "qdr:m", # Strictly the last 30 days for fresh buyers
            "num": 10
        })
        
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload, timeout=20)
            results = response.json()
            
            if "organic" in results:
                for item in results["organic"]:
                    link = item.get("link")
                    # Deduplication: Don't send the same lead twice
                    if link and link not in seen_links:
                        title = item.get("title", "Direct Buyer Signal")
                        snippet = item.get("snippet", "No preview.")
                        
                        # The Premium "Lead Card" for your Telegram
                        message = (
                            "🎯 **ELITE BUYER SIGNAL** 🎯\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            f"👤 **Source:** {title[:75]}\n"
                            f"💬 **Intent:** \"{snippet[:180]}...\"\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            f"🔗 [ENGAGE BUYER]({link})\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            "⭐ *Action: Direct Outreach (Nairaland/X)*"
                        )
                        
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                      json={
                                          "chat_id": CHAT_ID, 
                                          "text": message, 
                                          "parse_mode": "Markdown"
                                      })
                        
                        seen_links.add(link)
                        total_found += 1
                        
                        # 15 leads is the sweet spot for quality control
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
        self.wfile.write(f"Elite Buyer Scan Finished. {count} individuals delivered.".encode())
                    
