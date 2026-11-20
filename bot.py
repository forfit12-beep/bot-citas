import time, requests, os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib3
urllib3.disable_warnings()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
LINK = "https://icp.administracionelectronica.gob.es/icpplus/index.html"

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot funcionando")
    def log_message(self, *a):
        pass

def web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve_forever()

threading.Thread(target=web, daemon=True).start()

def avisar(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
        print("Aviso enviado")
    except Exception as e:
        print(e)

avisar("Bot conectado - Navarra, Barcelona, Madrid - Huellas + Recogida TIE")
print("Bot encendido - cada 3 minutos")

while True:
    try:
        print("Entrando en la web de Extranjeria...")
        r = requests.get(LINK, timeout=20, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        print("Codigo:", r.status_code)
        if r.status_code != 403:
            texto = r.text.lower()
            if "captcha" in texto:
                print("Pide captcha, espero")
            elif "no hay" in texto or "sin citas" in texto or "no existen" in texto:
                print("Sin citas, sigo buscando")
            else:
                print("POSIBLE CITA - AVISO")
                avisar("HAY CITA POSIBLE en Navarra / Barcelona / Madrid - Entra ya: " + LINK)
    except Exception as e:
        print("Error:", e)

    print("Espero 3 minutos")
    time.sleep(180)
