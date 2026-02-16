---
name: "n8n-workflow-patterns"
description: "Catálogo de patrones arquitectónicos para workflows en n8n. Contiene plantillas probadas para los casos de uso más comunes. Consultar antes de diseñar cualquier workflow nuevo."
version: "1.0"
type: "reference"
triggers:
  - "qué patrón usar"
  - "cómo estructurar"
  - "arquitectura workflow"
  - "plantilla n8n"
---

# Patrones de Workflow en N8N

## Instrucciones de Uso

Cuando el orquestador (`n8n-architect`) te invoque, debes:
1. Analizar el caso de uso del usuario.
2. Identificar qué patrón (o combinación de patrones) encaja mejor.
3. Devolver la estructura recomendada con los nodos principales.

Si ningún patrón encaja, diseña uno nuevo documentando la justificación.

---

## Catálogo de Patrones

### Patrón 1: Webhook → Procesador → Destino
**Caso de uso**: Recibir datos externos, transformarlos y enviarlos a otro sistema.
**Estructura**:
```
[Webhook] → [Code/Set] → [IF] → [HTTP Request / API Destino]
                                → [Error Handler]
```
**Ejemplos**: Formulario web → Google Sheets, Stripe webhook → CRM, GitHub webhook → Slack.
**Referencia detallada**: `references/patron-webhook-procesador.md`

---

### Patrón 2: Polling → Sync Bidireccional
**Caso de uso**: Sincronizar datos entre dos sistemas periódicamente.
**Estructura**:
```
[Schedule Trigger] → [Leer Sistema A] → [Comparar] → [Escribir Sistema B]
                                                    → [Escribir Sistema A (updates)]
```
**Ejemplos**: CRM ↔ Google Sheets, Base de datos ↔ Airtable.
**Referencia detallada**: `references/patron-polling-sync.md`

---

### Patrón 3: Error Handling Centralizado
**Caso de uso**: Capturar, registrar y notificar errores de cualquier workflow.
**Estructura**:
```
[Error Trigger] → [Code: formatear error] → [Slack/Email/Telegram]
                                           → [Google Sheets: log]
```
**Aplicar a**: Todos los workflows en producción.
**Referencia detallada**: `references/patron-error-handling.md`

---

### Patrón 4: Fan-Out / Fan-In (Procesamiento Paralelo)
**Caso de uso**: Procesar múltiples items en paralelo y consolidar resultados.
**Estructura**:
```
[Trigger] → [Split In Batches] → [Procesamiento por item]
                                → [Merge: consolidar]
                                → [Destino final]
```
**Ejemplos**: Procesar lista de URLs, envío masivo de emails personalizados.
**Referencia detallada**: `references/patron-fan-out-fan-in.md`

---

### Patrón 5: Chatbot / Agente Conversacional
**Caso de uso**: Bot en Telegram/Slack/WhatsApp que responde con lógica.
**Estructura**:
```
[Telegram/Slack Trigger] → [Switch: comando] → [Rama A: respuesta]
                                              → [Rama B: consulta API]
                                              → [Rama C: AI Agent]
                         → [Respuesta al usuario]
```

---

### Patrón 6: Pipeline de Datos ETL
**Caso de uso**: Extraer, transformar y cargar datos entre fuentes.
**Estructura**:
```
[Schedule/Webhook] → [Extract: API/DB/File] → [Transform: Code/Set]
                                             → [Load: DB/Sheets/API]
                                             → [Notify: éxito/error]
```

---

## Cómo Combinar Patrones

Los patrones se combinan frecuentemente:
- Patrón 1 + Patrón 3 = Webhook con error handling robusto
- Patrón 4 + Patrón 6 = ETL con procesamiento paralelo
- Patrón 5 + Patrón 1 = Bot que recibe webhooks y responde

Siempre recomienda **Patrón 3** como capa adicional en cualquier workflow de producción.
