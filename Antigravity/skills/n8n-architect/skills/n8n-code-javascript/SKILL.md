---
name: "n8n-code-javascript"
description: "Generador de código JavaScript para nodos Code en n8n. Incluye snippets validados, patrones de transformación de datos y buenas prácticas. Consultar siempre que se necesite lógica custom."
version: "1.0"
type: "generator"
triggers:
  - "código javascript n8n"
  - "nodo code"
  - "transformar datos"
  - "script n8n"
  - "función custom"
---

# Generador de Código JavaScript para N8N

## Instrucciones de Uso

Cuando te invoquen, debes:
1. Entender exactamente qué transformación o lógica se necesita.
2. Generar código que funcione **dentro del nodo Code de n8n** (no Node.js genérico).
3. Incluir manejo de errores y comentarios explicativos.
4. Indicar el modo correcto: `runOnceForAllItems` o `runOnceForEachItem`.

---

## Contexto del Nodo Code en N8N

### Variables disponibles
```javascript
// Acceso a items de entrada
const items = $input.all();        // Todos los items (modo AllItems)
const item = $input.item;          // Item actual (modo EachItem)

// Acceso a datos de otros nodos
const data = $('Nombre Nodo').all();
const firstItem = $('Nombre Nodo').first();

// Variables de entorno
const apiKey = $env.MI_VARIABLE;

// Variables del workflow
const workflowId = $workflow.id;
const isActive = $workflow.active;

// Ejecución actual
const executionId = $execution.id;
const mode = $execution.mode;      // 'test' o 'production'
```

### Retorno obligatorio
```javascript
// Modo AllItems — devolver array de items
return items.map(item => ({
  json: { ...item.json, nuevoCampo: 'valor' }
}));

// Modo EachItem — devolver un item
return { json: { ...item.json, nuevoCampo: 'valor' } };
```

---

## Snippets Validados

### Filtrar items por condición
```javascript
// Modo: runOnceForAllItems
const items = $input.all();
const filtrados = items.filter(item => {
  return item.json.status === 'active' && item.json.amount > 100;
});

if (filtrados.length === 0) {
  throw new Error('No se encontraron items activos con amount > 100');
}

return filtrados;
```

### Agrupar por campo
```javascript
// Modo: runOnceForAllItems
const items = $input.all();
const grupos = {};

for (const item of items) {
  const key = item.json.category || 'sin_categoria';
  if (!grupos[key]) grupos[key] = [];
  grupos[key].push(item.json);
}

return Object.entries(grupos).map(([category, records]) => ({
  json: { category, count: records.length, records }
}));
```

### Llamada HTTP dentro de Code
```javascript
// Modo: runOnceForAllItems
// Usar solo cuando HTTP Request node no es suficiente
const results = [];

for (const item of $input.all()) {
  try {
    const response = await fetch(`https://api.ejemplo.com/data/${item.json.id}`, {
      headers: { 'Authorization': `Bearer ${$env.API_TOKEN}` }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    results.push({ json: { ...item.json, enriched: data } });
  } catch (error) {
    // No romper el loop — registrar error y continuar
    results.push({
      json: { ...item.json, error: error.message, enriched: null }
    });
  }
}

return results;
```

### Deduplicar items
```javascript
// Modo: runOnceForAllItems
const items = $input.all();
const seen = new Set();
const unicos = [];

for (const item of items) {
  const key = item.json.email; // campo por el que deduplicar
  if (!seen.has(key)) {
    seen.add(key);
    unicos.push(item);
  }
}

return unicos;
```

### Transformar estructura (flatten/unflatten)
```javascript
// Modo: runOnceForAllItems
// Aplanar objeto anidado
function flatten(obj, prefix = '') {
  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    const newKey = prefix ? `${prefix}_${key}` : key;
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      Object.assign(result, flatten(value, newKey));
    } else {
      result[newKey] = value;
    }
  }
  return result;
}

return $input.all().map(item => ({
  json: flatten(item.json)
}));
```

### Generar resumen/estadísticas
```javascript
// Modo: runOnceForAllItems
const items = $input.all();

const stats = {
  total: items.length,
  porStatus: {},
  montoTotal: 0,
  montoPromedio: 0
};

for (const item of items) {
  const status = item.json.status || 'unknown';
  stats.porStatus[status] = (stats.porStatus[status] || 0) + 1;
  stats.montoTotal += Number(item.json.amount) || 0;
}

stats.montoPromedio = stats.total > 0
  ? Math.round(stats.montoTotal / stats.total * 100) / 100
  : 0;

return [{ json: stats }];
```

---

## Reglas de Código

1. **Siempre** manejar errores con try/catch.
2. **Nunca** hardcodear credenciales — usar `$env.VARIABLE`.
3. **Siempre** devolver el formato correcto (`{ json: {} }`).
4. **Preferir** `runOnceForAllItems` a menos que el procesamiento sea independiente por item.
5. **Comentar** la lógica de negocio, no la sintaxis obvia.
6. **Validar inputs** — Nunca asumir que los campos existen o tienen el tipo correcto.

---

Referencia extendida de snippets en `references/`.
