# Patrón: Webhook → Procesador → Destino

## Descripción

Este es el patrón más común en n8n. Un servicio externo envía datos a un webhook, se procesan/transforman, y se envían a un destino final.

## Estructura Detallada

```
[Webhook]
    ↓
[Code: Validar payload]
    ↓
[IF: ¿Datos válidos?]
    → Sí → [Code/Set: Transformar datos]
              ↓
           [HTTP Request / Nodo destino]
              ↓
           [Respuesta: 200 OK]
    → No → [Code: Log error]
              ↓
           [Respuesta: 400 Bad Request]
```

## Configuración del Webhook

```json
{
  "node": "n8n-nodes-base.webhook",
  "parameters": {
    "httpMethod": "POST",
    "path": "mi-endpoint-descriptivo",
    "responseMode": "responseNode",
    "options": {
      "rawBody": false
    }
  }
}
```

### Opciones de `responseMode`
- `onReceived`: Responde inmediatamente con 200 (fire-and-forget).
- `lastNode`: Responde cuando termina todo el workflow.
- `responseNode`: Usa un nodo `Respond to Webhook` para controlar la respuesta.

**Recomendación**: Usar `responseNode` para control total de la respuesta.

## Validación del Payload

Siempre validar antes de procesar:

```javascript
// Nodo Code — Modo: runOnceForAllItems
const items = $input.all();
const validated = [];

for (const item of items) {
  const { email, name, action } = item.json.body || {};

  if (!email || !name) {
    throw new Error(`Payload inválido: faltan campos requeridos. Recibido: ${JSON.stringify(item.json.body)}`);
  }

  validated.push({
    json: {
      email: email.toLowerCase().trim(),
      name: name.trim(),
      action: action || 'default',
      receivedAt: new Date().toISOString()
    }
  });
}

return validated;
```

## Seguridad del Webhook

### Opción 1: Verificar Header Secret
```javascript
const headers = $input.first().json.headers;
const expectedSecret = $env.WEBHOOK_SECRET;

if (headers['x-webhook-secret'] !== expectedSecret) {
  throw new Error('Unauthorized: Invalid webhook secret');
}
```

### Opción 2: Verificar firma HMAC (ej. Stripe, GitHub)
```javascript
const crypto = require('crypto');
const payload = JSON.stringify($input.first().json.body);
const signature = $input.first().json.headers['x-hub-signature-256'];
const secret = $env.WEBHOOK_SECRET;

const expected = 'sha256=' + crypto.createHmac('sha256', secret).update(payload).digest('hex');

if (signature !== expected) {
  throw new Error('Unauthorized: Invalid signature');
}
```

## Casos de Uso Comunes

| Origen | Transformación | Destino |
|--------|---------------|---------|
| Formulario web (Typeform, Tally) | Mapear campos | Google Sheets, CRM |
| Stripe (pagos) | Extraer datos de pago | Base de datos, email |
| GitHub (push, PR) | Formatear notificación | Slack, Discord |
| Calendly (reservas) | Enriquecer con CRM | Google Calendar, email |
| Custom API | Validar + transformar | Cualquier destino |

## Errores Comunes

1. **Olvidar `responseMode`**: El webhook hace timeout si no se configura la respuesta.
2. **No validar el payload**: Datos inesperados rompen nodos downstream.
3. **Webhook público sin autenticación**: Cualquiera puede enviar datos maliciosos.
4. **No manejar duplicados**: Muchos servicios reenvían webhooks si no reciben 200.
