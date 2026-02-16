# Patrón: Error Handling Centralizado

## Descripción

Un workflow dedicado que captura errores de TODOS los demás workflows, los formatea y los envía a canales de notificación y logs. Es la "red de seguridad" de tu instancia n8n.

## Estructura Detallada

```
[Error Trigger]
    ↓
[Code: Formatear error]
    ↓
[Switch: Severidad]
    → Crítico → [Slack: canal #alertas-criticas]
              → [Email: equipo de guardia]
    → Warning → [Slack: canal #alertas]
    → Info    → (solo log)
    ↓
[Google Sheets / DB: Registrar log]
```

## Configuración del Error Trigger

Cada workflow de producción debe tener configurado un "Error Workflow" en sus settings que apunte a este workflow centralizado.

```json
{
  "node": "n8n-nodes-base.errorTrigger",
  "parameters": {}
}
```

El Error Trigger recibe automáticamente:
- `execution.id`: ID de la ejecución fallida
- `execution.url`: URL para ver la ejecución en n8n
- `execution.error`: Objeto con mensaje y stack trace
- `workflow.id`: ID del workflow que falló
- `workflow.name`: Nombre del workflow

## Código de Formateo

```javascript
// Nodo Code — Modo: runOnceForAllItems
const error = $input.first().json;

const execution = error.execution || {};
const workflow = error.workflow || {};
const errorData = execution.error || {};

// Clasificar severidad
let severidad = 'info';
const errorMsg = (errorData.message || '').toLowerCase();

if (errorMsg.includes('timeout') || errorMsg.includes('rate limit')) {
  severidad = 'warning';
} else if (errorMsg.includes('authentication') || errorMsg.includes('unauthorized')) {
  severidad = 'critico';
} else if (errorMsg.includes('500') || errorMsg.includes('internal server')) {
  severidad = 'critico';
} else {
  severidad = 'warning';
}

const formatted = {
  severidad,
  workflow_name: workflow.name || 'Desconocido',
  workflow_id: workflow.id || 'N/A',
  execution_id: execution.id || 'N/A',
  execution_url: execution.url || 'N/A',
  error_message: errorData.message || 'Sin mensaje de error',
  error_stack: errorData.stack || 'Sin stack trace',
  timestamp: new Date().toISOString(),
  resumen: `[${severidad.toUpperCase()}] ${workflow.name}: ${errorData.message}`
};

return [{ json: formatted }];
```

## Mensaje para Slack/Telegram

Template recomendado:
```
🚨 *Error en Workflow*
*Workflow*: {{ $json.workflow_name }}
*Severidad*: {{ $json.severidad }}
*Error*: {{ $json.error_message }}
*Ejecución*: {{ $json.execution_url }}
*Timestamp*: {{ $json.timestamp }}
```

## Configuración en Workflows de Producción

Cada workflow debe tener en su configuración (Settings):
1. **Error Workflow**: Seleccionar el workflow de error handling centralizado.
2. **Timeout**: Configurar un timeout global razonable (ej. 120 segundos).
3. **Retry on Fail**: Para nodos HTTP, activar retry con backoff exponencial.

### Retry por nodo
```json
{
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 1000
}
```

## Mejoras Opcionales

1. **Dashboard de errores**: Conectar el log de Google Sheets a un Looker/Metabase para visualización.
2. **Alertas inteligentes**: No notificar el mismo error 50 veces — agregar deduplicación por ventana de tiempo.
3. **Auto-retry**: Para errores transitorios (timeouts, rate limits), reintentar automáticamente la ejecución.
