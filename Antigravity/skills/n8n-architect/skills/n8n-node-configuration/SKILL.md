---
name: "n8n-node-configuration"
description: "Referencia de configuración de nodos en n8n. Contiene parámetros exactos, versiones válidas y configuraciones recomendadas para cada tipo de nodo. Consultar en fase de Diseño."
version: "1.0"
type: "reference"
triggers:
  - "configurar nodo"
  - "parámetros nodo"
  - "qué nodo usar"
  - "versión nodo"
---

# Referencia de Configuración de Nodos

## Instrucciones de Uso

Cuando te invoquen, debes:
1. Identificar qué nodos necesita el workflow.
2. Devolver la configuración exacta con todos los parámetros requeridos.
3. Advertir sobre configuraciones que puedan causar errores.

---

## Nodos Críticos — Referencia Rápida

### Webhook
```json
{
  "node": "n8n-nodes-base.webhook",
  "parameters": {
    "httpMethod": "POST",
    "path": "mi-endpoint",
    "responseMode": "onReceived",
    "responseCode": 200
  }
}
```
**Errores comunes**: Olvidar `responseMode` (causa timeouts), path sin sanitizar.

### Code (reemplaza a Function — NO usar Function)
```json
{
  "node": "n8n-nodes-base.code",
  "parameters": {
    "language": "javaScript",
    "mode": "runOnceForAllItems"
  }
}
```
**Modos**: `runOnceForAllItems` (acceso a todos los items) vs `runOnceForEachItem` (por item).

### HTTP Request
```json
{
  "node": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://api.ejemplo.com/data",
    "authentication": "predefinedCredentialType",
    "options": {
      "timeout": 30000,
      "redirect": { "redirect": { "followRedirects": true } }
    }
  }
}
```
**Siempre**: Configurar timeout y manejo de redirects.

### IF (Condicional)
```json
{
  "node": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "options": { "caseSensitive": true },
      "combinator": "and",
      "conditions": [
        {
          "leftValue": "={{ $json.status }}",
          "rightValue": "active",
          "operator": { "type": "string", "operation": "equals" }
        }
      ]
    }
  }
}
```

### Switch
Usar cuando hay **3+ ramas**. Para 2, usar IF.

### Split In Batches
```json
{
  "parameters": {
    "batchSize": 10,
    "options": { "reset": false }
  }
}
```
**Siempre**: Usar `batchSize` razonable para evitar rate limits.

### Schedule Trigger
```json
{
  "node": "n8n-nodes-base.scheduleTrigger",
  "parameters": {
    "rule": {
      "interval": [
        { "field": "minutes", "minutesInterval": 15 }
      ]
    }
  }
}
```

### Respond to Webhook
```json
{
  "node": "n8n-nodes-base.respondToWebhook",
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ { success: true, message: 'Procesado' } }}"
  }
}
```
Usar con `responseMode: "responseNode"` en el Webhook.

### Wait
```json
{
  "node": "n8n-nodes-base.wait",
  "parameters": {
    "amount": 1,
    "unit": "seconds"
  }
}
```

### Merge
```json
{
  "node": "n8n-nodes-base.merge",
  "parameters": {
    "mode": "combine",
    "combineBy": "combineByPosition"
  }
}
```
**Modos v2**: `append` (concatenar), `combine` (por posición o campo), `chooseBranch` (elegir una rama).

---

## Nodos Obsoletos — NO USAR

| Obsoleto | Reemplazo |
|----------|-----------|
| `Function` | `Code` |
| `Function Item` | `Code` (modo `runOnceForEachItem`) |
| `Merge` (v1) | `Merge` (v2 con modos: append, combine, chooseBranch) |
| `Set` (v1) | `Set` (v2 — interfaz simplificada) |
| `Item Lists` (v1) | `Item Lists` (v2) |

---

## Reglas de Nomenclatura

Cada nodo DEBE tener un nombre descriptivo:
- ❌ `HTTP Request`  →  ✅ `Obtener datos del CRM`
- ❌ `Code`  →  ✅ `Transformar respuesta API a formato Sheets`
- ❌ `IF`  →  ✅ `¿Es cliente activo?`
- ❌ `Switch`  →  ✅ `Clasificar por tipo de evento`

---

Referencia completa por categoría en `references/`.
