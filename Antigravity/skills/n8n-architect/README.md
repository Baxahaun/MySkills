# N8N-Architect

Agente global para Antigravity especializado en diseño, auditoría y reparación de workflows en n8n.

## Skills incluidas

| Skill | Tipo | Descripción |
|-------|------|-------------|
| `n8n-workflow-patterns` | reference | Catálogo de patrones arquitectónicos |
| `n8n-node-configuration` | reference | Referencia de nodos y configuraciones |
| `n8n-code-javascript` | generator | Generador de código para nodos Code |
| `n8n-mcp-tools-expert` | reference | Integración con herramientas vía MCP |
| `n8n-validation-expert` | auditor | Auditor de workflows pre-entrega |

## Estructura

```
n8n-architect/
├── SKILL.md                              # Orquestador principal
├── README.md                             # Este archivo
├── skills/
│   ├── n8n-workflow-patterns/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── patron-webhook-procesador.md
│   │       ├── patron-polling-sync.md
│   │       ├── patron-error-handling.md
│   │       └── patron-fan-out-fan-in.md
│   ├── n8n-node-configuration/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── nodos-trigger.md
│   │       ├── nodos-accion.md
│   │       ├── nodos-flujo.md
│   │       └── nodos-transformacion.md
│   ├── n8n-code-javascript/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── snippets-comunes.md
│   │       └── patrones-transformacion.md
│   ├── n8n-mcp-tools-expert/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── mcp-servers-compatibles.md
│   └── n8n-validation-expert/
│       ├── SKILL.md
│       └── references/
│           └── errores-comunes.md
```

## Protocolo de uso

El agente sigue un protocolo de 4 fases obligatorias:

1. **Análisis**: Identifica el caso de uso y busca patrones existentes.
2. **Diseño**: Configura nodos con parámetros exactos.
3. **Lógica**: Genera código custom cuando es necesario.
4. **Validación**: Audita el workflow antes de entregarlo.

## Requisitos

- Variable de entorno `N8N_API_KEY` configurada.
- URL de la instancia n8n accesible.

## Instalación

```bash
npx skills add <repo-url> --skill n8n-architect -a antigravity -g
```

## Autor

**Xavier Crespo Griman** — @Baxahaun
