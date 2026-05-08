import requests
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = "8673029559:AAF4zFJC80TERVUMTvZ9ieSMWM0K-2vWGTI"
CHAT_ID = "7909543900"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Test Ping to Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": "🧼 Scrubber is Online!"})
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Scrubber reached. Check Telegram.")
      
