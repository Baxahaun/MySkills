# Patrón: Polling → Sync Bidireccional

## Descripción

Sincronización periódica entre dos sistemas. Un Schedule Trigger ejecuta el workflow cada X minutos/horas, lee cambios de ambos sistemas y los sincroniza.

## Estructura Detallada

```
[Schedule Trigger: cada 15 min]
    ↓
[Leer Sistema A: últimos cambios]
    ↓
[Leer Sistema B: últimos cambios]
    ↓
[Code: Comparar y detectar diferencias]
    ↓
[IF: ¿Hay cambios en A?]
    → Sí → [Escribir en Sistema B]
[IF: ¿Hay cambios en B?]
    → Sí → [Escribir en Sistema A]
    ↓
[Code: Log de sincronización]
```

## Configuración del Schedule Trigger

```json
{
  "node": "n8n-nodes-base.scheduleTrigger",
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "minutes",
          "minutesInterval": 15
        }
      ]
    }
  }
}
```

### Frecuencias recomendadas
- **Datos críticos** (pagos, inventario): cada 1-5 minutos
- **Datos operativos** (contactos, tareas): cada 15-30 minutos
- **Datos informativos** (reportes, logs): cada 1-6 horas

## Lógica de Comparación

```javascript
// Nodo Code — Modo: runOnceForAllItems
const sistemaA = $('Leer Sistema A').all().map(i => i.json);
const sistemaB = $('Leer Sistema B').all().map(i => i.json);

// Indexar por campo clave (ej: email)
const indexB = new Map(sistemaB.map(item => [item.email, item]));
const indexA = new Map(sistemaA.map(item => [item.email, item]));

const actualizarEnB = [];
const actualizarEnA = [];
const nuevosEnB = [];

for (const itemA of sistemaA) {
  const itemB = indexB.get(itemA.email);

  if (!itemB) {
    // Existe en A pero no en B → crear en B
    nuevosEnB.push({ json: itemA });
  } else if (new Date(itemA.updatedAt) > new Date(itemB.updatedAt)) {
    // A es más reciente → actualizar B
    actualizarEnB.push({ json: { ...itemA, targetId: itemB.id } });
  } else if (new Date(itemB.updatedAt) > new Date(itemA.updatedAt)) {
    // B es más reciente → actualizar A
    actualizarEnA.push({ json: { ...itemB, targetId: itemA.id } });
  }
}

return [
  { json: { actualizarEnB, actualizarEnA, nuevosEnB, resumen: {
    totalA: sistemaA.length,
    totalB: sistemaB.length,
    actualizarEnB: actualizarEnB.length,
    actualizarEnA: actualizarEnA.length,
    nuevos: nuevosEnB.length
  }}}
];
```

## Consideraciones Importantes

1. **Campo de timestamp**: Ambos sistemas necesitan un campo `updatedAt` o equivalente para detectar qué registro es más reciente.
2. **Campo clave única**: Necesitas un identificador común entre ambos sistemas (email, ID externo, etc.).
3. **Conflictos**: Si ambos cambian el mismo registro simultáneamente, define una regla: "Sistema A gana" o "el más reciente gana".
4. **Paginación**: Si hay muchos registros, usa paginación para no sobrecargar las APIs.
5. **Rate limits**: Respeta los límites de las APIs. Usa `Wait` nodes si es necesario.

## Errores Comunes

1. **Sin campo de timestamp**: No hay forma de saber qué cambió.
2. **Sincronización circular**: A actualiza B, B detecta cambio y actualiza A, loop infinito. Solución: usar un campo `syncedAt` para marcar registros ya sincronizados.
3. **Sin manejo de errores parciales**: Si falla la escritura en un sistema, el otro queda desincronizado.
4. **Frecuencia demasiado alta**: Consume cuota de API innecesariamente.
