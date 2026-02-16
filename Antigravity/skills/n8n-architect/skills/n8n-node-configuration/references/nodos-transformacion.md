# Nodos de Transformación — Referencia Completa

## Visión General

Los nodos de transformación modifican, filtran, agregan o reestructuran datos sin interactuar con servicios externos.

---

## Code

**Nodo**: `n8n-nodes-base.code`

Reemplaza a los obsoletos `Function` y `Function Item`.

```json
{
  "parameters": {
    "language": "javaScript",
    "mode": "runOnceForAllItems",
    "jsCode": "// tu código aquí"
  }
}
```

### Modos
- `runOnceForAllItems`: Se ejecuta una vez con acceso a todos los items. Retorna array.
- `runOnceForEachItem`: Se ejecuta una vez por cada item. Retorna un item.

### Lenguajes
- `javaScript` (recomendado)
- `python` (disponible en versiones recientes)

Ver skill `n8n-code-javascript` para snippets y buenas prácticas completas.

---

## Set

**Nodo**: `n8n-nodes-base.set` (v2)

Define o modifica campos de los items.

```json
{
  "parameters": {
    "mode": "manual",
    "duplicateItem": false,
    "assignments": {
      "assignments": [
        {
          "id": "field1",
          "name": "nombre_completo",
          "value": "={{ $json.firstName }} {{ $json.lastName }}",
          "type": "string"
        },
        {
          "id": "field2",
          "name": "es_premium",
          "value": "={{ $json.plan === 'premium' }}",
          "type": "boolean"
        }
      ]
    },
    "options": {
      "includeBinary": false
    }
  }
}
```

### Modos
- `manual`: Definir campos uno a uno
- `raw`: Pasar un objeto JSON completo

### Opciones importantes
- `duplicateItem`: Si true, crea una copia del item con los nuevos campos.
- `includeBinary`: Si el item tiene datos binarios, incluirlos o no.

---

## Item Lists

**Nodo**: `n8n-nodes-base.itemLists` (v2)

Operaciones sobre la lista de items.

### Concatenar items
```json
{
  "parameters": {
    "operation": "concatenateItems",
    "aggregate": "aggregateAllItemData",
    "options": {}
  }
}
```

### Dividir items
```json
{
  "parameters": {
    "operation": "splitOutItems",
    "fieldToSplitOut": "data.items",
    "options": {}
  }
}
```
Toma un campo que es array y crea un item por cada elemento.

### Ordenar items
```json
{
  "parameters": {
    "operation": "sort",
    "sortFieldsUi": {
      "sortField": [
        { "fieldName": "createdAt", "order": "descending" }
      ]
    }
  }
}
```

### Eliminar duplicados
```json
{
  "parameters": {
    "operation": "removeDuplicates",
    "compare": "selectedFields",
    "fieldsToCompare": {
      "fields": [
        { "fieldName": "email" }
      ]
    }
  }
}
```

### Limitar items
```json
{
  "parameters": {
    "operation": "limit",
    "maxItems": 100
  }
}
```

---

## Date & Time

**Nodo**: `n8n-nodes-base.dateTime`

Manipulación de fechas.

```json
{
  "parameters": {
    "operation": "formatDate",
    "date": "={{ $json.createdAt }}",
    "format": "yyyy-MM-dd HH:mm:ss",
    "options": {
      "timezone": "America/Mexico_City"
    }
  }
}
```

### Operaciones
- `formatDate`: Convertir formato
- `calculateDate`: Sumar/restar tiempo
- `getTimeBetweenDates`: Diferencia entre fechas

---

## Crypto

**Nodo**: `n8n-nodes-base.crypto`

Hashing y encoding.

```json
{
  "parameters": {
    "action": "hash",
    "type": "SHA256",
    "value": "={{ $json.password }}",
    "dataPropertyName": "hashedPassword"
  }
}
```

---

## Rename Keys

**Nodo**: `n8n-nodes-base.renameKeys`

Renombrar campos de los items.

```json
{
  "parameters": {
    "keys": {
      "key": [
        { "currentKey": "first_name", "newKey": "firstName" },
        { "currentKey": "last_name", "newKey": "lastName" }
      ]
    }
  }
}
```

---

## Buenas Prácticas

1. **Set para transformaciones simples, Code para complejas** — No usar Code si un Set basta.
2. **Item Lists para operaciones de lista** — Ordenar, filtrar, deduplicar sin código.
3. **Expresiones en Set** — Aprovechar `={{ }}` para transformaciones inline.
4. **Nombrar descriptivamente** — `Renombrar campos API → formato interno` en vez de `Set`.
5. **Validar tipos** — Usar Code para validar que los datos tienen el tipo esperado antes de enviarlos.
