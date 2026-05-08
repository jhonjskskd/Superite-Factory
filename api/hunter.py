import requests
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

def hunt_leads():
    # We use ONE powerful query to test the connection first
    query = "site:nairaland.com 'invest in Lagos' 2026"
    search_url = f"https://www.google.com/search?q={query}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This looks for ANY link in the search results
        links = []
        for a in soup.find_all('a', href=True):
            url = a['href']
            if "/url?q=" in url and "google.com" not in url:
                clean_url = url.split("/url?q=")[1].split("&sa=")[0]
                links.append(clean_url)
        
        unique_links = list(set(links))[:3] # Just get 3 for the test
        
        if unique_links:
            for link in unique_links:
                msg = f"🔍 **TEST LEAD FOUND**\n{link}"
                requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                              json={"chat_id": CHAT_ID, "text": msg})
            return len(unique_links)
    except Exception as e:
        print(e)
    return 0

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        count = hunt_leads()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"Test Run Complete. Found {count} results.".encode())
        
