import time, requests, os

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def avisar(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje}, timeout=10)
    except Exception as e:
        print(e)

avisar("✅ Bot conectado - Vigilando Navarra, Barcelona, Madrid - Huellas + Recogida TIE")

while True:
    time.sleep(60)
