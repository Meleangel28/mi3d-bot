from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

@app.route("/", methods=["GET"])
def index():
    return "✅ Mi3D Bot activo en Render", 200

@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    token_enviado = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token_enviado == VERIFY_TOKEN:
        return challenge, 200
    return "❌ Token de verificación inválido", 403

@app.route("/webhook", methods=["POST"])
def recibir_evento():
    data = request.get_json()
    print("📦 Webhook recibido:", data)

    if "entry" in data:
        for entry in data["entry"]:
            if "messaging" in entry:
                for evento in entry["messaging"]:
                    if evento.get("message"):
                        sender_id = evento["sender"]["id"]
                        mensaje = evento["message"].get("text", "")
                        print(f"📩 Mensaje de {sender_id}: {mensaje}")
                        enviar_respuesta(sender_id, "Hola 👋, gracias por escribir a Mi3D. Te responderemos pronto.")

    return "ok", 200

def enviar_respuesta(recipient_id, mensaje):
    url = f"https://graph.facebook.com/v18.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": mensaje}
    }
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, params=params, json=payload, headers=headers)
    print(f"📤 Enviando respuesta a {recipient_id}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
