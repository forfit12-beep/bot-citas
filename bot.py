import requests, time, os
import urllib3
urllib3.disable_warnings()
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.environ.get("9123991972:AAHngHY1FGqiAeVUEvjLdU5pMEjM3VRqURg")
CHAT_ID = os.environ.get("6998750482")
LINK = "https://icp.administracionelectronica.gob.es/icpplus/index.html"

# SOLO TUS 5 PROVINCIAS
PROVINCIAS = ["Navarra", "Barcelona", "Rioja", "Castellon", "Valladolid"]
TRAMITES = ["huellas", "recogida"]

def avisar(m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m}, timeout=10)
    except:
        pass

def web():
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.end_headers(); self.wfile.write(b"Bot funcionando")
        def log_message(self, *a): pass
    HTTPServer(("0.0.0.0", 10000), H).serve_forever()
threading.Thread(target=web, daemon=True).start()

print("Bot conectado - Solo 5 provincias: Navarra, Barcelona, Rioja, Castellon, Valladolid")
avisar("Bot conectado - Solo Navarra, Barcelona, Rioja, Castellon, Valladolid - cada 3 minutos")

while True:
    for prov in PROVINCIAS:
        for tramite in TRAMITES:
            try:
                print(f"Comprobando {prov}/{tramite}...")
                r = requests.get(LINK, timeout=20, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
                print(f"{prov} Codigo:", r.status_code)
                texto = r.text.lower()
                if "no hay" not in texto and "sin citas" not in texto and "no existen" not in texto:
                    avisar(f"⚠️ HAY CITA POSIBLE en {prov} - {tramite} - Entra YA: " + LINK)
                else:
                    print(f"{prov}/{tramite} Sin citas")
            except Exception as e:
                print(f"Error {prov}:", e)
    print("Espero 3 minutos")
    time.sleep(180)
