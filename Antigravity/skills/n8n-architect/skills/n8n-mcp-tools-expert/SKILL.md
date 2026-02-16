---
name: "n8n-mcp-tools-expert"
description: "Guía de integración de herramientas externas vía MCP (Model Context Protocol) con n8n. Cubre configuración de servidores MCP, nodos AI Agent, y conexión con servicios externos."
version: "1.0"
type: "reference"
triggers:
  - "mcp"
  - "ai agent n8n"
  - "herramienta externa"
  - "model context protocol"
  - "conectar servicio externo"
---

# Integración MCP con N8N

## Instrucciones de Uso

Cuando te invoquen, debes:
1. Identificar si el caso de uso requiere MCP o si basta con nodos nativos.
2. Si requiere MCP, configurar la conexión correctamente.
3. Validar que el servidor MCP es compatible con n8n.

---

## Cuándo Usar MCP vs Nodos Nativos

| Situación | Usar |
|-----------|------|
| El servicio tiene nodo nativo en n8n | **Nodo nativo** (siempre preferir) |
| El servicio no tiene nodo pero sí API REST | **HTTP Request** |
| Necesitas que un AI Agent use herramientas dinámicamente | **MCP** |
| Necesitas interacción con filesystem, browser o DB local | **MCP** |

MCP solo es necesario cuando un agente de IA dentro del workflow necesita **decidir dinámicamente** qué herramienta usar.

---

## Arquitectura MCP en N8N

```
[Trigger] → [AI Agent Node]
                ↓
            [LLM: OpenAI/Anthropic]
                ↓
            [Tools: MCP Client]
                ↓
            [MCP Server: herramientas]
```

El nodo AI Agent es el orquestador. Se conecta a:
1. Un **LLM** (OpenAI, Anthropic, Ollama, etc.) que razona.
2. **Tools** que el LLM puede invocar — aquí entra MCP.

---

## Configuración del Nodo AI Agent

### Estructura básica
```json
{
  "node": "@n8n/n8n-nodes-langchain.agent",
  "parameters": {
    "agent": "toolsAgent",
    "promptType": "define",
    "text": "={{ $json.userMessage }}",
    "options": {
      "systemMessage": "Eres un asistente que ayuda a gestionar tareas. Usa las herramientas disponibles para completar lo que el usuario pide.",
      "maxIterations": 10,
      "returnIntermediateSteps": false
    }
  }
}
```

### Parámetros importantes
- `maxIterations`: Límite de pasos del agente. **Siempre configurar** para evitar bucles.
- `systemMessage`: Define el comportamiento del agente. Debe ser específico.
- `returnIntermediateSteps`: Si true, incluye los pasos intermedios en el output (útil para debug).

---

## Conectar un Servidor MCP

### Paso 1: Crear credencial MCP Client

En n8n, ve a **Credentials → New → MCP Client** y configura:

**Para servidores SSE (remotos)**:
```json
{
  "sseEndpoint": "https://mi-servidor-mcp.com/sse"
}
```

**Para servidores Stdio (locales)**:
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/ruta/permitida"]
}
```

### Paso 2: Añadir como Tool al AI Agent

En el nodo AI Agent, añadir un sub-nodo **MCP Client Tool** y asociarle la credencial creada.

---

## Servidores MCP Compatibles

| Servidor | Protocolo | Uso típico |
|----------|-----------|------------|
| `@modelcontextprotocol/server-filesystem` | stdio | Lectura/escritura de archivos |
| `@modelcontextprotocol/server-brave-search` | stdio | Búsqueda web |
| `@modelcontextprotocol/server-github` | stdio | Operaciones en GitHub |
| `@modelcontextprotocol/server-slack` | stdio | Mensajes en Slack |
| `@modelcontextprotocol/server-postgres` | stdio | Consultas a PostgreSQL |
| `@modelcontextprotocol/server-memory` | stdio | Memoria persistente para el agente |
| `@modelcontextprotocol/server-puppeteer` | stdio | Automatización web (scraping) |
| `@modelcontextprotocol/server-google-maps` | stdio | Geolocalización y mapas |

Referencia detallada en `references/mcp-servers-compatibles.md`.

---

## Ejemplo Completo: Agente con Herramientas

### Caso: Bot de Telegram que busca en web y responde

```
[Telegram Trigger]
    ↓
[AI Agent]
    ├── LLM: OpenAI GPT-4
    ├── Tool: MCP Client (Brave Search)
    └── Tool: Calculator
    ↓
[Telegram: enviar respuesta]
```

El AI Agent recibe el mensaje del usuario, decide si necesita buscar en la web (usa Brave Search vía MCP), calcula si es necesario, y devuelve la respuesta.

---

## Errores Comunes

1. **Usar MCP cuando basta un HTTP Request** — Sobrecomplica el workflow. Si sabes qué endpoint llamar, usa HTTP Request directamente.
2. **No limitar `maxIterations`** — El agente puede entrar en bucle gastando tokens infinitamente.
3. **No configurar `systemMessage`** — El agente no sabe qué hacer y responde de forma genérica.
4. **Timeout del servidor MCP** — Configurar timeout adecuado en la credencial.
5. **Permisos excesivos** — Si usas server-filesystem, limitar la ruta permitida al mínimo necesario.
6. **No manejar errores del agente** — Si el LLM o una tool falla, el workflow debe tener fallback.

---

## Cuándo NO usar AI Agent + MCP

- **Flujos predecibles**: Si siempre haces A → B → C, no necesitas un agente que "decida". Usa nodos normales.
- **Alto volumen**: Los agentes son lentos y costosos (múltiples llamadas al LLM). Para procesamiento masivo, usa nodos nativos.
- **Datos sensibles**: El LLM ve los datos que procesan las tools. Cuidado con información confidencial.
