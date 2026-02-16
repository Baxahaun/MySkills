# Errores Comunes en Workflows N8N

## Errores Críticos (Bloqueos)

### 1. Credenciales Hardcodeadas
**Qué es**: API keys, tokens o passwords escritos directamente en el JSON del workflow o en nodos Code.
**Por qué es grave**: Cualquiera que vea el workflow tiene acceso a los servicios.
**Cómo detectar**: Buscar strings que parezcan tokens (Bearer, sk-, xoxb-, etc.) en el JSON del workflow.
**Solución**: Mover a credenciales de n8n o variables de entorno (`$env.MI_VARIABLE`).

### 2. Webhook Sin Autenticación
**Qué es**: Un webhook público que cualquiera puede llamar sin verificación.
**Por qué es grave**: Actores maliciosos pueden enviar datos falsos, desencadenar workflows, o hacer DDoS.
**Cómo detectar**: Webhook sin nodo de validación de headers/firma inmediatamente después.
**Solución**: Implementar verificación de header secret, firma HMAC, o IP whitelist.

### 3. Loop Infinito en Split In Batches
**Qué es**: `Split In Batches` con `reset: true` sin condición de salida.
**Por qué es grave**: El workflow nunca termina, consume recursos indefinidamente.
**Cómo detectar**: Verificar que el parámetro `reset` está en `false`, o que hay una condición de salida clara.
**Solución**: `reset: false` (default) o añadir un IF que detecte cuándo parar.

### 4. Sin Error Handling
**Qué es**: Workflow sin Error Trigger ni Error Workflow configurado.
**Por qué es grave**: Los errores pasan desapercibidos. El workflow falla silenciosamente.
**Cómo detectar**: Verificar en Settings del workflow si hay un Error Workflow asignado.
**Solución**: Crear un workflow de error handling centralizado y asignarlo.

### 5. Nodos Obsoletos
**Qué es**: Uso de nodos descontinuados como `Function`, `Function Item`, `Merge v1`.
**Por qué es grave**: Pueden dejar de funcionar en actualizaciones de n8n. No reciben fixes.
**Cómo detectar**: Buscar `n8n-nodes-base.function` en el JSON.
**Solución**: Migrar a `Code`, `Merge v2`, etc.

---

## Errores de Rendimiento (Advertencias)

### 6. Batch Size Excesivo
**Qué es**: `Split In Batches` con batchSize > 50 para APIs con rate limits.
**Impacto**: Errores 429 (Too Many Requests), datos perdidos.
**Solución**: Reducir batchSize y añadir Wait nodes.

### 7. Sin Timeout en HTTP Request
**Qué es**: HTTP Request sin timeout configurado.
**Impacto**: Si la API no responde, el nodo espera indefinidamente (hasta el timeout global).
**Solución**: Configurar `options.timeout` (recomendado: 30000ms).

### 8. Procesamiento Secuencial Innecesario
**Qué es**: Procesar items uno a uno cuando se podrían procesar en batch.
**Impacto**: Workflow lento para volúmenes grandes.
**Solución**: Usar APIs de batch cuando estén disponibles, o `runOnceForAllItems`.

---

## Errores de Datos (Advertencias/Bloqueos)

### 9. Sin Validación de Input
**Qué es**: Asumir que los datos de entrada siempre tienen la estructura esperada.
**Impacto**: Errores crípticos cuando falta un campo o viene con tipo incorrecto.
**Solución**: Añadir nodo Code o IF que valide la estructura antes de procesar.

### 10. Campos que Desaparecen
**Qué es**: Un nodo transforma los datos y pierde campos que se necesitan después.
**Impacto**: Nodos downstream fallan por campos undefined.
**Cómo detectar**: Seguir el flujo de datos y verificar que cada nodo pasa los campos necesarios.
**Solución**: Usar spread operator (`...item.json`) para mantener campos existentes al transformar.

### 11. Tipos Inconsistentes
**Qué es**: Un campo viene como string pero se compara como number (o viceversa).
**Impacto**: Condicionales que nunca se cumplen, datos incorrectos.
**Solución**: Convertir explícitamente con `Number()`, `String()`, `Boolean()`.

---

## Errores de Legibilidad (Advertencias)

### 12. Nodos Sin Nombre
**Qué es**: Nodos con nombres por defecto como "Code", "HTTP Request", "IF".
**Impacto**: El workflow es difícil de entender y mantener.
**Solución**: Renombrar con el propósito del nodo: "Validar payload", "Obtener usuario del CRM".

### 13. Sin Notas Explicativas
**Qué es**: Secciones complejas sin documentación.
**Impacto**: Otros (o tú mismo en 3 meses) no entienden la lógica.
**Solución**: Añadir Sticky Notes en n8n explicando la lógica de negocio.

### 14. Flujo Desordenado
**Qué es**: Nodos cruzados, conexiones que van hacia atrás, layout confuso.
**Impacto**: Difícil de seguir visualmente.
**Solución**: Reorganizar de izquierda a derecha, usar colores para secciones.

---

## Checklist Rápido Pre-Entrega

1. Buscar strings sospechosos en JSON (tokens, keys, passwords)
2. Verificar que hay Error Workflow configurado
3. Verificar que webhooks tienen validación
4. Verificar que no hay nodos obsoletos
5. Verificar que Split In Batches tiene `reset: false`
6. Verificar que HTTP Request tiene timeout
7. Verificar que todos los nodos tienen nombres descriptivos
8. Ejecutar una prueba con datos reales
