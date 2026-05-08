import requests
import json
from http.server import BaseHTTPRequestHandler

# --- ELITE CONFIGURATION ---
SERPER_API_KEY = "6c182913e988a6f03588ca60e4cd657a5fb66300" 
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

def hunt_leads():
    url = "https://google.serper.dev/search"
    
    # These queries target high-intent 'I want' and 'Help me' language
    queries = [
        "site:nairaland.com 'looking for land' Lagos 'UK' OR 'USA' 2026",
        "site:x.com 'recommend' 'realtor' Lagos diaspora",
        "site:nairaland.com 'verified' land 'Epe' OR 'Ibeju Lekki' 2026",
        "site:facebook.com 'Nigeria diaspora' 'buy' 'property' Lagos",
        "site:nairaland.com 'avoid scam' land Lagos 2026",
        "site:x.com 'want to invest' Nigeria 'real estate' diaspora"
    ]
    
    total_found = 0
    seen_links = set()

    for q in queries:
        payload = json.dumps({
            "q": q,
            "tbs": "qdr:m", # Strict focus on the last 30 days
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
                    if link and link not in seen_links:
                        title = item.get("title", "High-Value Lead")
                        snippet = item.get("snippet", "No preview available.")
                        
                        # Professional Diaspora Lead Card
                        message = (
                            "🔥 **HOT INDIVIDUAL LEAD** 🔥\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            f"👤 **Source:** {title[:75]}\n"
                            f"💬 **Message:** \"{snippet[:180]}...\"\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            f"🔗 [GO TO CONVERSATION]({link})\n"
                            "━━━━━━━━━━━━━━━━━━━━\n"
                            "✅ *Action: Direct Outreach via DM/Comment*"
                        )
                        
                        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                      json={
                                          "chat_id": CHAT_ID, 
                                          "text": message, 
                                          "parse_mode": "Markdown",
                                          "disable_web_page_preview": False
                                      })
                        
                        seen_links.add(link)
                        total_found += 1
                        
                        # Stop at 15 leads to keep quality high
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
        self.wfile.write(f"Elite Scan Finished. {count} premium individuals found.".encode())
                        
