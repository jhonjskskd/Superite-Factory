import requests
import json
from http.server import BaseHTTPRequestHandler

# --- ELITE CONFIGURATION ---
SERPER_API_KEY = "6c182913e988a6f03588ca60e4cd657a5fb66300" 
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

def hunt_leads():
    url = "https://google.serper.dev/search"
    
    # These queries are 'Hardened' to find individuals while blocking tech/news junk
    queries = [
        "site:nairaland.com 'anyone' 'recommend' land Lagos diaspora -software -AI",
        "site:nairaland.com 'help' 'verify' land title Lagos -coding -tech",
        "site:nairaland.com 'looking for' property Ibeju Lekki OR Epe 2026",
        "site:x.com 'want to buy' Lagos land diaspora -AI -developer",
        "site:nairaland.com 'scammed' 'property' Lagos help -visa",
        "site:facebook.com 'Nigerians in' 'USA' OR 'UK' 'buying land' Lagos"
    ]
    
    total_found = 0
    seen_links = set()

    for q in queries:
        payload = json.dumps({
            "q": q,
            "tbs": "qdr:m", # Strictly the last 30 days for fresh conversations
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
                        title = item.get("title", "Individual Buyer Signal")
                        snippet = item.get("snippet", "Checking post content...")
                        
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
                        
                        # Quality over quantity: limit to 15 per run
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
                        
