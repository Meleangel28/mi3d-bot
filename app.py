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
    return "❌ Token inválido", 403

@app.route("/webhook", methods=["POST"])
def recibir_webhook():
    data = request.get_json()
    print("📦 Datos recibidos:", data)

    # 🧪 Para pruebas desde Meta (estructura con "value")
    if "field" in data and "value" in data:
        value = data["value"]
        sender_id = value.get("sender", {}).get("id")
        message_text = value.get("message", {}).get("text")
        if sender_id and message_text:
            print(f"📩 Prueba de {sender_id}: {message_text}")
            enviar_respuesta(sender_id, "✅ Webhook de prueba recibido correctamente.")
        return "ok", 200

    # 💬 Para mensajes reales (estructura con "entry" y "messaging")
    if "entry" in data:
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                sender_id = event.get("sender", {}).get("id")
                message_text = event.get("message", {}).get("text")
                if sender_id and message_text:
                    print(f"📩 Mensaje real de {sender_id}: {message_text}")
                    enviar_respuesta(sender_id, "Hola 👋, gracias por escribir a Mi3D.")
    return "ok", 200

def enviar_respuesta(recipient_id, mensaje):
    url = "https://graph.facebook.com/v18.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": mensaje}
    }
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}

    response = requests.post(url, params=params, json=payload, headers=headers)
    print(f"📤 Enviado a {recipient_id}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
