# Nodos de Acción — Referencia Completa

## Visión General

Los nodos de acción ejecutan operaciones: enviar datos, crear registros, enviar mensajes, etc.

---

## HTTP Request

**Nodo**: `n8n-nodes-base.httpRequest`

El nodo más versátil. Conecta con cualquier API REST.

```json
{
  "parameters": {
    "method": "POST",
    "url": "https://api.ejemplo.com/endpoint",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "httpHeaderAuth",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        { "name": "Content-Type", "value": "application/json" }
      ]
    },
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        { "name": "key", "value": "={{ $json.valor }}" }
      ]
    },
    "options": {
      "timeout": 30000,
      "response": { "response": { "fullResponse": false } },
      "redirect": { "redirect": { "followRedirects": true, "maxRedirects": 5 } }
    }
  }
}
```

### Tipos de autenticación
- `none`: Sin autenticación
- `predefinedCredentialType`: Usar credencial guardada en n8n
- `genericCredentialType`: Header, Query o Basic auth genérico

### Modos de body
- `json`: Enviar JSON (más común)
- `form-urlencoded`: Para formularios
- `multipart-form-data`: Para subir archivos
- `raw`: Body crudo (XML, texto, etc.)

---

## Google Sheets

**Nodo**: `n8n-nodes-base.googleSheets`

```json
{
  "parameters": {
    "operation": "append",
    "documentId": "SPREADSHEET_ID",
    "sheetName": "Sheet1",
    "columns": {
      "mappingMode": "autoMapInputData"
    },
    "options": {}
  },
  "credentials": {
    "googleSheetsOAuth2Api": { "id": "CREDENTIAL_ID" }
  }
}
```

### Operaciones disponibles
- `append`: Añadir fila al final
- `update`: Actualizar filas existentes
- `read`: Leer filas
- `delete`: Eliminar filas
- `clear`: Limpiar rango

---

## Slack

**Nodo**: `n8n-nodes-base.slack`

```json
{
  "parameters": {
    "resource": "message",
    "operation": "post",
    "channel": "C01234ABCDE",
    "text": "={{ $json.mensaje }}",
    "otherOptions": {
      "unfurl_links": false
    }
  },
  "credentials": {
    "slackOAuth2Api": { "id": "CREDENTIAL_ID" }
  }
}
```

### Recursos y operaciones
- `message`: post, update, delete, getPermalink
- `channel`: archive, create, get, getAll, invite, join, kick, leave
- `file`: upload, getAll
- `reaction`: add, get, remove
- `user`: get, getAll, getPresence

---

## Email (Send)

**Nodo**: `n8n-nodes-base.sendEmail` (SMTP) o `n8n-nodes-base.gmail`

### Gmail
```json
{
  "parameters": {
    "resource": "message",
    "operation": "send",
    "to": "={{ $json.email }}",
    "subject": "Asunto del email",
    "message": "Contenido HTML del email",
    "options": {}
  },
  "credentials": {
    "gmailOAuth2": { "id": "CREDENTIAL_ID" }
  }
}
```

---

## Telegram

**Nodo**: `n8n-nodes-base.telegram`

```json
{
  "parameters": {
    "resource": "message",
    "operation": "sendMessage",
    "chatId": "={{ $json.chatId }}",
    "text": "={{ $json.respuesta }}",
    "additionalFields": {
      "parse_mode": "Markdown"
    }
  },
  "credentials": {
    "telegramApi": { "id": "CREDENTIAL_ID" }
  }
}
```

---

## Buenas Prácticas

1. **Siempre configurar timeout** en HTTP Request (default puede ser muy largo).
2. **Usar credenciales de n8n**, nunca valores hardcodeados.
3. **Nombrar descriptivamente** — `Enviar alerta a Slack #ops` en vez de `Slack`.
4. **Configurar `continueOnFail`** cuando sea aceptable que un nodo falle sin romper el workflow.
5. **Usar expresiones** (`={{ }}`) para datos dinámicos, nunca valores estáticos que deberían ser dinámicos.
