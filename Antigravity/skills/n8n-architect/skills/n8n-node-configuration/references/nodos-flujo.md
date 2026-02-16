# Nodos de Flujo — Referencia Completa

## Visión General

Los nodos de flujo controlan la dirección y lógica del workflow: condicionales, loops, merges, waits.

---

## IF (Condicional)

**Nodo**: `n8n-nodes-base.if`

Divide el flujo en dos ramas (true/false).

```json
{
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

### Combinadores
- `and`: Todas las condiciones deben cumplirse
- `or`: Al menos una condición debe cumplirse

### Tipos de operador

**String**: `equals`, `notEquals`, `contains`, `notContains`, `startsWith`, `endsWith`, `regex`, `isEmpty`, `isNotEmpty`

**Number**: `equals`, `notEquals`, `gt`, `lt`, `gte`, `lte`

**Boolean**: `true`, `false`

**Datetime**: `after`, `before`

---

## Switch

**Nodo**: `n8n-nodes-base.switch`

Para 3+ ramas. Cada rama tiene su propia condición.

```json
{
  "parameters": {
    "mode": "rules",
    "rules": {
      "rules": [
        {
          "output": 0,
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.type }}",
                "rightValue": "order",
                "operator": { "type": "string", "operation": "equals" }
              }
            ]
          }
        },
        {
          "output": 1,
          "conditions": {
            "conditions": [
              {
                "leftValue": "={{ $json.type }}",
                "rightValue": "refund",
                "operator": { "type": "string", "operation": "equals" }
              }
            ]
          }
        }
      ],
      "fallbackOutput": 2
    }
  }
}
```

**Siempre** configurar `fallbackOutput` para items que no coincidan con ninguna regla.

---

## Merge

**Nodo**: `n8n-nodes-base.merge` (v2)

Combina datos de dos entradas.

### Modo Append (concatenar)
```json
{
  "parameters": {
    "mode": "append"
  }
}
```
Une todos los items de ambas entradas en una sola lista.

### Modo Combine por posición
```json
{
  "parameters": {
    "mode": "combine",
    "combineBy": "combineByPosition",
    "options": {}
  }
}
```
Combina item 1 de entrada A con item 1 de entrada B.

### Modo Combine por campo
```json
{
  "parameters": {
    "mode": "combine",
    "combineBy": "combineByFields",
    "mergeByFields": {
      "values": [
        { "field1": "email", "field2": "email" }
      ]
    }
  }
}
```
Hace "join" por un campo común.

### Modo Choose Branch
```json
{
  "parameters": {
    "mode": "chooseBranch",
    "output": "input1"
  }
}
```
Espera a que ambas entradas tengan datos, pero solo pasa los de una.

---

## Split In Batches

**Nodo**: `n8n-nodes-base.splitInBatches`

Procesa items en lotes dentro de un loop.

```json
{
  "parameters": {
    "batchSize": 10,
    "options": {
      "reset": false
    }
  }
}
```

**ADVERTENCIA**: `reset: true` reinicia el contador y puede causar loops infinitos.

### Cómo funciona el loop
- Output 1 (arriba): Items del batch actual → conectar al procesamiento
- Output 2 (abajo): Se ejecuta cuando terminan todos los batches → conectar al siguiente paso

---

## Wait

**Nodo**: `n8n-nodes-base.wait`

Pausa la ejecución.

```json
{
  "parameters": {
    "resume": "timeInterval",
    "amount": 2,
    "unit": "seconds"
  }
}
```

### Modos
- `timeInterval`: Espera un tiempo fijo
- `specificTime`: Espera hasta una hora específica
- `webhook`: Espera hasta recibir un webhook callback
- `formSubmission`: Espera hasta que se complete un formulario

---

## No Operation (NoOp)

**Nodo**: `n8n-nodes-base.noOp`

No hace nada. Útil para:
- Ramas del IF que no necesitan acción
- Placeholder durante desarrollo
- Punto de merge visual

---

## Buenas Prácticas

1. **IF para 2 ramas, Switch para 3+** — No encadenar IFs cuando un Switch es más claro.
2. **Siempre usar fallback en Switch** — Items sin match se pierden silenciosamente.
3. **Nombrar las ramas** — `¿Es cliente VIP?` es mejor que `IF`.
4. **Wait dentro de loops** — Siempre poner Wait en loops que llaman APIs para respetar rate limits.
5. **Merge: elegir modo correcto** — `append` no es lo mismo que `combine`.
