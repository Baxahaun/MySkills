# Patrón: Fan-Out / Fan-In (Procesamiento Paralelo)

## Descripción

Divide una lista de items en lotes, procesa cada lote independientemente, y consolida los resultados al final. Ideal para operaciones masivas que deben respetar rate limits.

## Estructura Detallada

```
[Trigger]
    ↓
[Obtener lista de items]
    ↓
[Split In Batches: tamaño N]
    ↓  (loop)
[Procesar item/batch]
    ↓
[Wait: respetar rate limit]
    ↓
[Split In Batches: done?]
    → No → volver a procesar
    → Sí → [Code: consolidar resultados]
              ↓
           [Destino final / Notificación]
```

## Configuración de Split In Batches

```json
{
  "node": "n8n-nodes-base.splitInBatches",
  "parameters": {
    "batchSize": 10,
    "options": {
      "reset": false
    }
  }
}
```

### Tamaños de batch recomendados

| API / Servicio | Batch size recomendado | Rate limit típico |
|----------------|----------------------|-------------------|
| Google Sheets | 50 | 60 req/min |
| Slack | 10 | 1 req/seg (Tier 3) |
| HubSpot | 10 | 100 req/10seg |
| Airtable | 10 | 5 req/seg |
| Stripe | 25 | 100 req/seg |
| OpenAI | 5 | Varía por modelo |
| General (conservador) | 10 | - |

## Consolidación de Resultados

```javascript
// Nodo Code después del loop — Modo: runOnceForAllItems
const items = $input.all();

const exitosos = items.filter(i => !i.json.error);
const fallidos = items.filter(i => i.json.error);

return [{
  json: {
    total_procesados: items.length,
    exitosos: exitosos.length,
    fallidos: fallidos.length,
    errores: fallidos.map(i => ({
      id: i.json.id,
      error: i.json.error
    })),
    timestamp: new Date().toISOString()
  }
}];
```

## Wait Node para Rate Limits

```json
{
  "node": "n8n-nodes-base.wait",
  "parameters": {
    "amount": 1,
    "unit": "seconds"
  }
}
```

Insertar el Wait **dentro del loop**, después de cada batch, para respetar rate limits.

## Variante: Procesamiento con Reintentos

Para items que fallan, guardarlos y reintentarlos al final:

```javascript
// Dentro del loop de procesamiento
const item = $input.item;
try {
  // ... lógica de procesamiento ...
  return { json: { ...item.json, status: 'ok' } };
} catch (error) {
  return {
    json: {
      ...item.json,
      status: 'error',
      error: error.message,
      retryCount: (item.json.retryCount || 0) + 1
    }
  };
}
```

## Errores Comunes

1. **Batch size demasiado grande**: Sobrepasa rate limits y causa errores 429.
2. **Sin Wait node**: Procesamiento demasiado rápido para la API destino.
3. **`reset: true` accidental**: Reinicia el loop infinitamente.
4. **Sin consolidación**: Los resultados parciales se pierden.
5. **Sin manejo de errores por item**: Un item fallido rompe todo el batch.
