# Snippets Comunes para Nodos Code

## Manipulación de Strings

### Limpiar y normalizar texto
```javascript
// Modo: runOnceForAllItems
return $input.all().map(item => ({
  json: {
    ...item.json,
    email: (item.json.email || '').toLowerCase().trim(),
    nombre: (item.json.nombre || '').trim().replace(/\s+/g, ' '),
    telefono: (item.json.telefono || '').replace(/[^0-9+]/g, '')
  }
}));
```

### Extraer datos con regex
```javascript
// Modo: runOnceForEachItem
const text = $input.item.json.body || '';

// Extraer email
const emailMatch = text.match(/[\w.-]+@[\w.-]+\.\w+/);
// Extraer teléfono
const phoneMatch = text.match(/\+?\d[\d\s-]{7,}/);
// Extraer URLs
const urlMatch = text.match(/https?:\/\/[^\s]+/g);

return {
  json: {
    ...item.json,
    extractedEmail: emailMatch ? emailMatch[0] : null,
    extractedPhone: phoneMatch ? phoneMatch[0].replace(/\s/g, '') : null,
    extractedUrls: urlMatch || []
  }
};
```

### Generar slug
```javascript
function slugify(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remover acentos
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

return $input.all().map(item => ({
  json: { ...item.json, slug: slugify(item.json.title || '') }
}));
```

---

## Manipulación de Fechas

### Formatear fecha
```javascript
// Modo: runOnceForAllItems
return $input.all().map(item => {
  const date = new Date(item.json.createdAt);
  return {
    json: {
      ...item.json,
      fechaFormateada: date.toLocaleDateString('es-ES', {
        year: 'numeric', month: 'long', day: 'numeric'
      }),
      horaFormateada: date.toLocaleTimeString('es-ES', {
        hour: '2-digit', minute: '2-digit'
      }),
      timestamp: date.getTime(),
      iso: date.toISOString()
    }
  };
});
```

### Calcular diferencia entre fechas
```javascript
// Modo: runOnceForEachItem
const start = new Date($input.item.json.startDate);
const end = new Date($input.item.json.endDate);
const diffMs = end - start;

return {
  json: {
    ...$input.item.json,
    diasDiferencia: Math.floor(diffMs / (1000 * 60 * 60 * 24)),
    horasDiferencia: Math.floor(diffMs / (1000 * 60 * 60)),
    esVencido: end < new Date()
  }
};
```

---

## Manipulación de Arrays

### Paginar resultados
```javascript
// Modo: runOnceForAllItems
const items = $input.all();
const page = 1; // Cambiar según necesidad
const pageSize = 50;
const start = (page - 1) * pageSize;
const end = start + pageSize;

const paginated = items.slice(start, end);

return [{
  json: {
    items: paginated.map(i => i.json),
    pagination: {
      page,
      pageSize,
      total: items.length,
      totalPages: Math.ceil(items.length / pageSize)
    }
  }
}];
```

### Agrupar items en chunks
```javascript
// Modo: runOnceForAllItems
const items = $input.all();
const chunkSize = 10;
const chunks = [];

for (let i = 0; i < items.length; i += chunkSize) {
  chunks.push({
    json: {
      chunkIndex: Math.floor(i / chunkSize),
      items: items.slice(i, i + chunkSize).map(item => item.json)
    }
  });
}

return chunks;
```

---

## Manejo de Errores

### Try/catch con logging
```javascript
// Modo: runOnceForAllItems
const results = [];
const errors = [];

for (const item of $input.all()) {
  try {
    // ... lógica de procesamiento ...
    const processed = { /* resultado */ };
    results.push({ json: { ...processed, _status: 'ok' } });
  } catch (error) {
    errors.push({
      json: {
        _status: 'error',
        _error: error.message,
        _originalData: item.json
      }
    });
  }
}

// Opcional: lanzar si hay muchos errores
if (errors.length > results.length) {
  throw new Error(`Demasiados errores: ${errors.length}/${results.length + errors.length}`);
}

return [...results, ...errors];
```

---

## Interacción con Otros Nodos

### Acceder a datos de nodos anteriores
```javascript
// Datos del nodo "Webhook"
const webhookData = $('Webhook').first().json;
const body = webhookData.body;
const headers = webhookData.headers;

// Datos del nodo "Obtener usuario"
const usuario = $('Obtener usuario').first().json;

// Todos los items de un nodo
const todosLosItems = $('Buscar en DB').all();
```

### Usar variables de ejecución
```javascript
const isTest = $execution.mode === 'test';
const executionId = $execution.id;

// Comportamiento diferente en test vs producción
const endpoint = isTest
  ? 'https://staging-api.ejemplo.com'
  : 'https://api.ejemplo.com';
```
