# Patrones de Transformación de Datos

## Patrón: API Response → Formato Interno

Normalizar respuestas de APIs externas a tu formato estándar.

```javascript
// Modo: runOnceForAllItems
// Transforma respuesta de HubSpot a formato interno
const items = $input.all();

return items.map(item => {
  const contact = item.json;
  return {
    json: {
      id: contact.id,
      email: contact.properties?.email || null,
      nombre: contact.properties?.firstname || '',
      apellido: contact.properties?.lastname || '',
      nombreCompleto: `${contact.properties?.firstname || ''} ${contact.properties?.lastname || ''}`.trim(),
      empresa: contact.properties?.company || null,
      telefono: contact.properties?.phone || null,
      estado: contact.properties?.lifecyclestage || 'unknown',
      creadoEn: contact.properties?.createdate || null,
      actualizadoEn: contact.properties?.lastmodifieddate || null,
      fuente: 'hubspot'
    }
  };
});
```

---

## Patrón: CSV/Sheets → Objetos Estructurados

Cuando recibes datos tabulares con headers inconsistentes.

```javascript
// Modo: runOnceForAllItems
const items = $input.all();

// Mapeo de nombres de columna (lo que viene → lo que quiero)
const fieldMap = {
  'Nombre': 'nombre',
  'Name': 'nombre',
  'nombre': 'nombre',
  'Email': 'email',
  'Correo': 'email',
  'email': 'email',
  'Teléfono': 'telefono',
  'Phone': 'telefono',
  'Tel': 'telefono'
};

return items.map(item => {
  const normalized = {};

  for (const [key, value] of Object.entries(item.json)) {
    const normalizedKey = fieldMap[key] || key.toLowerCase().replace(/\s+/g, '_');
    normalized[normalizedKey] = typeof value === 'string' ? value.trim() : value;
  }

  return { json: normalized };
});
```

---

## Patrón: Datos Anidados → Filas Planas

Expandir arrays anidados en items individuales (útil para Google Sheets).

```javascript
// Modo: runOnceForAllItems
// Input: { order_id: 1, items: [{name: "A", qty: 2}, {name: "B", qty: 1}] }
// Output: dos items, uno por cada item del pedido

const results = [];

for (const item of $input.all()) {
  const order = item.json;
  const orderItems = order.items || [];

  for (const orderItem of orderItems) {
    results.push({
      json: {
        order_id: order.order_id,
        customer: order.customer,
        item_name: orderItem.name,
        item_qty: orderItem.qty,
        item_price: orderItem.price,
        item_total: (orderItem.qty || 0) * (orderItem.price || 0)
      }
    });
  }
}

return results;
```

---

## Patrón: Filas Planas → Objeto Agrupado

Inverso al anterior — convertir filas en objetos anidados.

```javascript
// Modo: runOnceForAllItems
// Agrupar filas por order_id
const items = $input.all();
const orders = {};

for (const item of items) {
  const row = item.json;
  const orderId = row.order_id;

  if (!orders[orderId]) {
    orders[orderId] = {
      order_id: orderId,
      customer: row.customer,
      items: [],
      total: 0
    };
  }

  orders[orderId].items.push({
    name: row.item_name,
    qty: row.item_qty,
    price: row.item_price
  });

  orders[orderId].total += (row.item_qty || 0) * (row.item_price || 0);
}

return Object.values(orders).map(order => ({ json: order }));
```

---

## Patrón: Diff / Detectar Cambios

Comparar dos listas y detectar nuevos, eliminados y modificados.

```javascript
// Modo: runOnceForAllItems
const anterior = $('Datos Anteriores').all().map(i => i.json);
const actual = $('Datos Actuales').all().map(i => i.json);

const keyField = 'id'; // campo clave para identificar registros

const anteriorMap = new Map(anterior.map(item => [item[keyField], item]));
const actualMap = new Map(actual.map(item => [item[keyField], item]));

const nuevos = [];
const eliminados = [];
const modificados = [];
const sinCambios = [];

// Detectar nuevos y modificados
for (const [id, item] of actualMap) {
  if (!anteriorMap.has(id)) {
    nuevos.push(item);
  } else {
    const prev = anteriorMap.get(id);
    if (JSON.stringify(prev) !== JSON.stringify(item)) {
      modificados.push({ anterior: prev, actual: item });
    } else {
      sinCambios.push(item);
    }
  }
}

// Detectar eliminados
for (const [id, item] of anteriorMap) {
  if (!actualMap.has(id)) {
    eliminados.push(item);
  }
}

return [{
  json: {
    resumen: {
      nuevos: nuevos.length,
      eliminados: eliminados.length,
      modificados: modificados.length,
      sinCambios: sinCambios.length
    },
    nuevos,
    eliminados,
    modificados,
    sinCambios
  }
}];
```

---

## Patrón: Rate Limiter Interno

Controlar la velocidad de procesamiento desde código.

```javascript
// Modo: runOnceForAllItems
const items = $input.all();
const DELAY_MS = 200; // 200ms entre items = ~5 req/seg
const results = [];

for (let i = 0; i < items.length; i++) {
  try {
    // Procesar item
    const response = await fetch(`https://api.ejemplo.com/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${$env.API_TOKEN}`
      },
      body: JSON.stringify(items[i].json)
    });

    const data = await response.json();
    results.push({ json: { ...items[i].json, result: data } });
  } catch (error) {
    results.push({ json: { ...items[i].json, error: error.message } });
  }

  // Esperar entre requests (excepto el último)
  if (i < items.length - 1) {
    await new Promise(resolve => setTimeout(resolve, DELAY_MS));
  }
}

return results;
```
