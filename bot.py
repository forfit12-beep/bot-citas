import requests, os
import urllib3
urllib3.disable_warnings()

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
LINK = "https://icp.administracionelectronica.gob.es/icpplus/index.html"

def avisar(m):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m})

try:
    r = requests.get(LINK, timeout=20, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
    texto = r.text.lower()
    if "captcha" in texto:
        print("Pide captcha")
    elif "no hay" in texto or "sin citas" in texto or "no existen" in texto:
        print("Sin citas")
    else:
        avisar("HAY CITA POSIBLE en Navarra / Barcelona / Madrid - Entra ya: " + LINK)
        print("Aviso enviado")
except Exception as e:
    print("Error:", e)
