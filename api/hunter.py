import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from http.server import BaseHTTPRequestHandler

# --- PREMIUM CONFIGURATION ---
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

# High-intent Diaspora keywords for Lagos Real Estate
QUERIES = [
    'site:x.com "investing" "Lagos" "real estate" (UK OR USA OR Canada)',
    'site:x.com "buying" "property" "Nigeria" (diaspora OR abroad)',
    'site:facebook.com "Lekki" "land" (London OR Houston OR Toronto)',
    'site:nairaland.com "Diaspora" "real estate" "2026"'
]

def send_telegram_card(name, location, text, link):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = (
        "💎 **PREMIUM DIASPORA LEAD**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Name:** {name}\n"
        f"📍 **Location:** {location}\n"
        f"📝 **Signal:** \"{text[:140]}...\"\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [VIEW POST]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 *Action: Ready for Scrubber phase.*"
    )
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        total_leads = 0
        
        for query in QUERIES:
            # We use a slight delay to prevent Google from blocking the Vercel IP
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            try:
                response = requests.get(search_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Searching for Google result blocks
                    for result in soup.select('.tF2Cxc'):
                        title_element = result.select_one('.DKV0Md')
                        link_element = result.select_one('.yuRUbf a')
                        snippet_element = result.select_one('.VwiC3b')
                        
                        if title_element and link_element:
                            title = title_element.text
                            link = link_element['href']
                            snippet = snippet_element.text if snippet_element else "No description available."
                            
                            # Clean up the name from the title
                            name = title.split('(@')[0].split('|')[0].strip()
                            
                            send_telegram_card(name, "International/Diaspora", snippet, link)
                            total_leads += 1
                            time.sleep(2) # Safe interval
                else:
                    print(f"Google Search blocked or failed with status: {response.status_code}")
            except Exception as e:
                print(f"Search Error: {e}")
                continue

        # Vercel Response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response_message = f"Hunter Process Complete. Found {total_leads} leads and sent to Telegram."
        self.wfile.write(response_message.encode())
      
