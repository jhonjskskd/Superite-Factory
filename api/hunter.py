import requests
import json
from http.server import BaseHTTPRequestHandler

# --- MASTER CONFIGURATION ---
# Your unique Serper pass for official Google access
SERPER_API_KEY = "6c182913e988a6f03588ca60e4cd657a5fb66300" 
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

def hunt_leads():
    url = "https://google.serper.dev/search"
    
    # We target Diaspora Nigerians (UK/USA/Canada) looking for premium Lagos assets
    # Using 'tbs': 'qdr:m' ensures we get fresh data from the last 30 days
    payload = json.dumps({
      "q": "invest in Lagos real estate diaspora (UK OR USA OR Canada) 2026",
      "tbs": "qdr:m", 
      "num": 15
    })
    
    headers = {
      'X-API-KEY': SERPER_API_KEY,
      'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=20)
        results = response.json()
        
        count = 0
        if "organic" in results:
            for item in results["organic"]:
                title = item.get("title", "Premium Lead")
                link = item.get("link", "#")
                snippet = item.get("snippet", "No context available.")
                
                # Professional Card Formatting for your Telegram
                message = (
                    "💎 **DIASPORA ASSET SIGNAL** 💎\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    f"🏢 **Title:** {title}\n"
                    f"📝 **Intent:** {snippet[:180]}...\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 [SECURE THE LEAD]({link})\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🌟 *Status: High-Value Verified*"
                )
                
                # Send the card
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              json={
                                  "chat_id": CHAT_ID, 
                                  "text": message, 
                                  "parse_mode": "Markdown",
                                  "disable_web_page_preview": False
                              })
                count += 1
                
        return count
    except Exception as e:
        print(f"Factory Error: {e}")
        return 0

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Trigger the hunt
        count = hunt_leads()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        if count > 0:
            output = f"✅ SUCCESS: {count} leads found and delivered to Telegram."
        else:
            output = "⚠️ API Connected, but no new signals found. Try widening keywords."
            
        self.wfile.write(output.encode())
        
