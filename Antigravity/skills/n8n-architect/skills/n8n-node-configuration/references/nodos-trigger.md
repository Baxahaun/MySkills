# Nodos Trigger — Referencia Completa

## Visión General

Los triggers son el punto de entrada de un workflow. Solo puede haber **un trigger activo** por workflow (aunque se pueden tener varios configurados y activar solo uno).

---

## Webhook Trigger

**Nodo**: `n8n-nodes-base.webhook`

Recibe peticiones HTTP externas.

```json
{
  "parameters": {
    "httpMethod": "POST",
    "path": "mi-webhook",
    "responseMode": "responseNode",
    "responseCode": 200,
    "options": {
      "rawBody": false,
      "responseContentType": "application/json"
    }
  }
}
```

### Métodos HTTP soportados
- `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`

### Modos de respuesta
- `onReceived`: Responde 200 inmediatamente, workflow continúa en background.
- `lastNode`: Espera a que termine el workflow y responde con el output del último nodo.
- `responseNode`: Usa un nodo `Respond to Webhook` — **recomendado** para control total.

### Datos disponibles
- `$json.body`: Cuerpo de la petición
- `$json.headers`: Headers de la petición
- `$json.query`: Parámetros de query string
- `$json.params`: Parámetros de ruta

---

## Schedule Trigger

**Nodo**: `n8n-nodes-base.scheduleTrigger`

Ejecuta el workflow periódicamente.

```json
{
  "parameters": {
    "rule": {
      "interval": [
        { "field": "minutes", "minutesInterval": 30 }
      ]
    }
  }
}
```

### Opciones de intervalo
- `seconds` (mínimo 10 en cloud)
- `minutes`
- `hours`
- `days`
- `weeks`
- `months`
- `cronExpression` para reglas complejas

### Ejemplo Cron
```json
{
  "rule": {
    "interval": [
      {
        "field": "cronExpression",
        "expression": "0 9 * * 1-5"
      }
    ]
  }
}
```
Esto ejecuta a las 9:00 AM de lunes a viernes.

---

## Triggers de Servicios Externos

### Telegram Trigger
```json
{
  "node": "n8n-nodes-base.telegramTrigger",
  "parameters": {
    "updates": ["message", "callback_query"],
    "additionalFields": {}
  },
  "credentials": {
    "telegramApi": { "id": "CREDENTIAL_ID" }
  }
}
```

### Slack Trigger (Event)
```json
{
  "node": "n8n-nodes-base.slackTrigger",
  "parameters": {
    "trigger": "onMessage",
    "channelId": "C01234ABCDE",
    "options": {}
  },
  "credentials": {
    "slackOAuth2Api": { "id": "CREDENTIAL_ID" }
  }
}
```

### Google Sheets Trigger
```json
{
  "node": "n8n-nodes-base.googleSheetsTrigger",
  "parameters": {
    "documentId": "SHEET_ID",
    "sheetName": "Sheet1",
    "event": "rowAdded",
    "pollTimes": {
      "item": [{ "mode": "everyMinute" }]
    }
  }
}
```

---

## Email Trigger (IMAP)
```json
{
  "node": "n8n-nodes-base.imapEmail",
  "parameters": {
    "mailbox": "INBOX",
    "options": {
      "unseen": true
    }
  },
  "credentials": {
    "imap": { "id": "CREDENTIAL_ID" }
  }
}
```

---

## Error Trigger

**Nodo**: `n8n-nodes-base.errorTrigger`

Se ejecuta cuando OTRO workflow falla y tiene este como "Error Workflow".

```json
{
  "node": "n8n-nodes-base.errorTrigger",
  "parameters": {}
}
```

No tiene parámetros configurables. Recibe automáticamente información del error y la ejecución fallida.

---

## Buenas Prácticas para Triggers

1. **Un trigger activo por workflow** — Tener múltiples puede causar ejecuciones inesperadas.
2. **Nombrar descriptivamente** — Ej: `Webhook: Recibir formulario de contacto`.
3. **Documentar la URL/frecuencia** — Añadir nota con la URL del webhook o la frecuencia del schedule.
4. **Validar inmediatamente después del trigger** — El siguiente nodo debería validar los datos.
