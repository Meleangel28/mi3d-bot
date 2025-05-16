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
def recibir_evento():
    data = request.get_json()
    print("📦 Webhook recibido:", data)

    # 🔧 Para pruebas manuales (sin entry[])
    if data.get("field") == "messages":
        value = data.get("value", {})
        sender_id = value.get("sender", {}).get("id")
        mensaje = value.get("message", {}).get("text", "")
        if sender_id and mensaje:
            print(f"🧪 [PRUEBA] Mensaje de {sender_id}: {mensaje}")
            enviar_respuesta(sender_id, "✅ Webhook de prueba recibido correctamente.")

    # 🔧 Para producción (con entry[] y changes[])
    elif "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                field = change.get("field")
                value = change.get("value", {})

                sender_id = value.get("sender", {}).get("id")

                # 💬 Mensajes
                if field == "messages" and "message" in value:
                    mensaje = value["message"].get("text", "")
                    print(f"📩 [INSTAGRAM] Mensaje de {sender_id}: {mensaje}")
                    enviar_respuesta(sender_id, "Hola 👋, gracias por escribir a Mi3D.")

                # ❤️ Reacciones
                elif field == "message_reactions" and "reaction" in value:
                    emoji = value["reaction"].get("emoji", "")
                    print(f"💖 Reacción de {sender_id}: {emoji}")

                # ⬇️ Postbacks
                elif field == "messaging_postbacks" and "postback" in value:
                    payload = value["postback"].get("payload", "")
                    print(f"📦 Postback de {sender_id}: {payload}")
                    enviar_respuesta(sender_id, f"Recibido: {payload}")

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
