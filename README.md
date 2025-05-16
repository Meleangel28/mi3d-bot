
# 🤖 Mi3D Instagram Bot

Este es un bot desarrollado en Python usando Flask que se conecta con la API de Meta (Facebook/Instagram) para responder automáticamente a mensajes directos recibidos en la cuenta @mi3d.ve.

---

## 🚀 ¿Qué puede hacer este bot?

- ✅ Responde automáticamente a mensajes que llegan por Instagram
- ✅ Detecta y muestra reacciones a mensajes (❤️, 👍, etc.)
- ✅ Maneja botones o postbacks enviados por el usuario
- ✅ Es compatible con pruebas desde Meta Developers
- ✅ Funciona tanto con **Facebook Messenger** como **Instagram Direct**

---

## 📦 Estructura del Webhook

El bot escucha peticiones `POST` enviadas por Meta a la ruta `/webhook`.

### Formato real de producción (Instagram)
```json
{
  "entry": [
    {
      "changes": [
        {
          "field": "messages",
          "value": {
            "sender": { "id": "123456" },
            "message": { "text": "Hola" }
          }
        }
      ]
    }
  ]
}
```

### Formato de prueba manual desde Meta Developers
```json
{
  "field": "messages",
  "value": {
    "sender": { "id": "123456" },
    "message": { "text": "Hola" }
  }
}
```

Ambos están soportados por el servidor.

---

## 🌐 Cómo hacer que funcione

### 1. Configurar variables de entorno

Asegúrate de definir estas variables en Render (o en un archivo `.env` si es local):

```
VERIFY_TOKEN=mi3d_verify_token
PAGE_ACCESS_TOKEN=EAAXXXXX...ZCZD
```

Estas credenciales vienen de la App que creaste en [Meta for Developers](https://developers.facebook.com/).

---

### 2. Requisitos

Instala los paquetes necesarios con:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` incluye:

```
flask
requests
```

---

### 3. Ejecutar localmente

```bash
python app.py
```

Tu servidor quedará activo en:  
`http://localhost:5000`

Puedes usar [ngrok](https://ngrok.com) para exponerlo temporalmente si estás en desarrollo:

```bash
ngrok http 5000
```

---

## ⚙️ Configurar el Webhook en Meta

1. Ve a [developers.facebook.com](https://developers.facebook.com/)
2. En tu app → Productos → Webhooks
3. Selecciona el objeto `instagram`
4. En “URL de devolución de llamada”, coloca:

```
https://mi3d-bot.onrender.com/webhook
```

5. En “Token de verificación”, coloca exactamente lo mismo que pusiste en la variable `VERIFY_TOKEN`:

```
mi3d_verify_token
```

6. Haz clic en “Verificar y guardar”

7. Luego suscribe estos campos:

- `messages`
- `message_reactions`
- `messaging_postbacks`

---

## 🧪 Pruebas y Debugging

Puedes enviar mensajes reales desde otra cuenta de Instagram a @mi3d.ve o usar el botón "Enviar a servidor" en Meta Developers.

Para ver la actividad, abre la pestaña “Logs” en tu servicio Render.

---

## ✨ Respuesta automática

Cuando el bot detecta un mensaje, envía esta respuesta:

```
Hola 👋, gracias por escribir a Mi3D. Te responderemos pronto.
```

Esto se puede personalizar fácilmente en la función `enviar_respuesta()` dentro de `app.py`.

---

## 💡 ¿Qué puedo hacer después?

- Conectarlo a **ChatGPT** para generar respuestas más inteligentes.
- Leer productos desde un **Google Sheets**.
- Construir flujos automáticos según palabras clave.

---

## 📬 Contacto

Este bot fue desarrollado por [Mi3D.ve](https://www.instagram.com/mi3d.ve)  
Si deseas adaptarlo o integrarlo con IA, contáctame para ayudarte.

---
