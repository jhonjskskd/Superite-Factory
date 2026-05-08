import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from http.server import BaseHTTPRequestHandler

# --- PREMIUM CONFIGURATION ---
BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

# BROAD & DEEP: These queries cover the entire Google index for high-value targets
QUERIES = [
    'investing in Lagos real estate "2026"',
    'buying land in Lekki as Nigerian in UK USA',
    'best estate developers in Lagos reviews diaspora',
    'how to verify land title in Nigeria forum',
    'Epe property investment ROI diaspora',
    'site:x.com "Lagos property" "diaspora"',
    'site:nairaland.com "buy land" "Lekki" "scam"',
    'moving back to Nigeria from abroad housing'
]

def send_telegram_card(title, link, snippet):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Premium Branding for the Message
    message = (
        "🌍 **GLOBAL ASSET SCAN: LEAD DETECTED**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📑 **Topic:** {title[:80]}\n"
        f"📝 **Context:** \"{snippet[:150]}...\"\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🔗 [OPEN SOURCE]({link})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💎 *Status: Monthly High-Intent Signal*"
    )
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Professional User-Agent to avoid blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        total_leads = 0
        seen_links = set() # Avoid sending the same thing twice
        
        for query in QUERIES:
            # tbs=qdr:m tells Google to look at the last MONTH for maximum results
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbs=qdr:m"
            
            try:
                response = requests.get(search_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Target all Google result containers
                    for result in soup.find_all('div', class_='g'):
                        link_tag = result.find('a')
                        title_tag = result.find('h3')
                        snippet_tag = result.find('div', style=lambda value: value and '-webkit-line-clamp' in value)
                        
                        if link_tag and title_tag:
                            link = link_tag['href']
                            title = title_tag.text
                            snippet = snippet_tag.text if snippet_tag else "Click link to view details."
                            
                            # Filter out Google's own internal links
                            if link.startswith("http") and "google.com" not in link and link not in seen_links:
                                send_telegram_card(title, link, snippet)
                                seen_links.add(link)
                                total_leads += 1
                                if total_leads >= 15: break # Limit to 15 best leads per run
                
                time.sleep(1) # Safety gap
            except:
                continue
            
            if total_leads >= 15: break

        # Final Response to Browser
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response_message = f"Global Hunter Complete. Found {total_leads} leads from the last 30 days."
        self.wfile.write(response_message.encode())
                        
