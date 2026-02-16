# Servidores MCP Compatibles con N8N — Referencia Detallada

## Servidores Oficiales (Model Context Protocol)

### Filesystem
**Paquete**: `@modelcontextprotocol/server-filesystem`
**Protocolo**: stdio
**Instalación**: `npx -y @modelcontextprotocol/server-filesystem /ruta/permitida`

**Herramientas disponibles**:
- `read_file`: Leer contenido de un archivo
- `write_file`: Escribir contenido a un archivo
- `list_directory`: Listar contenido de un directorio
- `create_directory`: Crear directorio
- `move_file`: Mover/renombrar archivo
- `search_files`: Buscar archivos por patrón
- `get_file_info`: Obtener metadatos de un archivo

**Seguridad**: Solo permite acceso dentro de las rutas especificadas en los argumentos. Nunca dar acceso a `/` o `~`.

---

### Brave Search
**Paquete**: `@modelcontextprotocol/server-brave-search`
**Protocolo**: stdio
**Requisito**: Variable de entorno `BRAVE_API_KEY`

**Herramientas disponibles**:
- `brave_web_search`: Búsqueda web general
- `brave_local_search`: Búsqueda de negocios locales

**Configuración en n8n**:
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-brave-search"],
  "env": {
    "BRAVE_API_KEY": "tu-api-key"
  }
}
```

---

### GitHub
**Paquete**: `@modelcontextprotocol/server-github`
**Protocolo**: stdio
**Requisito**: Variable de entorno `GITHUB_PERSONAL_ACCESS_TOKEN`

**Herramientas disponibles**:
- `create_or_update_file`: Crear/actualizar archivo en repo
- `search_repositories`: Buscar repos
- `create_repository`: Crear repo
- `get_file_contents`: Leer archivo de repo
- `push_files`: Push múltiples archivos
- `create_issue`: Crear issue
- `create_pull_request`: Crear PR
- `fork_repository`: Fork de repo
- `create_branch`: Crear branch
- `list_commits`: Listar commits
- `list_issues`: Listar issues

---

### Slack
**Paquete**: `@modelcontextprotocol/server-slack`
**Protocolo**: stdio
**Requisito**: Variable de entorno `SLACK_BOT_TOKEN`

**Herramientas disponibles**:
- `list_channels`: Listar canales
- `post_message`: Enviar mensaje a canal
- `reply_to_thread`: Responder en hilo
- `add_reaction`: Añadir reacción
- `get_channel_history`: Leer historial
- `get_thread_replies`: Leer respuestas de hilo
- `search_messages`: Buscar mensajes
- `get_users`: Listar usuarios
- `get_user_profile`: Obtener perfil de usuario

---

### PostgreSQL
**Paquete**: `@modelcontextprotocol/server-postgres`
**Protocolo**: stdio
**Requisito**: Connection string como argumento

**Herramientas disponibles**:
- `query`: Ejecutar SQL (SELECT, INSERT, UPDATE, DELETE)
- `list_tables`: Listar tablas
- `describe_table`: Describir estructura de tabla

**Configuración**:
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@host:5432/db"]
}
```

**Seguridad**: Usar un usuario de base de datos con permisos mínimos. Nunca dar acceso de superuser.

---

### Memory
**Paquete**: `@modelcontextprotocol/server-memory`
**Protocolo**: stdio

**Herramientas disponibles**:
- `create_entities`: Crear entidades en memoria
- `create_relations`: Crear relaciones entre entidades
- `add_observations`: Añadir observaciones a entidades
- `delete_entities`: Eliminar entidades
- `delete_observations`: Eliminar observaciones
- `delete_relations`: Eliminar relaciones
- `read_graph`: Leer el grafo de conocimiento
- `search_nodes`: Buscar nodos
- `open_nodes`: Abrir nodos específicos

Útil para dar al agente "memoria" entre ejecuciones.

---

### Puppeteer
**Paquete**: `@modelcontextprotocol/server-puppeteer`
**Protocolo**: stdio

**Herramientas disponibles**:
- `navigate`: Navegar a URL
- `screenshot`: Capturar pantalla
- `click`: Hacer clic en elemento
- `fill`: Rellenar campo
- `select`: Seleccionar opción
- `hover`: Hover sobre elemento
- `evaluate`: Ejecutar JavaScript en la página

Útil para scraping y automatización web cuando no hay API disponible.

---

## Criterio de Selección

| Necesidad | Servidor recomendado |
|-----------|---------------------|
| El agente necesita buscar información en la web | Brave Search |
| El agente necesita leer/escribir archivos | Filesystem |
| El agente necesita interactuar con GitHub | GitHub |
| El agente necesita enviar/leer mensajes de Slack | Slack |
| El agente necesita consultar/modificar base de datos | PostgreSQL |
| El agente necesita recordar información entre sesiones | Memory |
| El agente necesita interactuar con páginas web | Puppeteer |

## Nota sobre Servidores Custom

Si necesitas un servidor MCP que no existe, puedes crear uno custom. La especificación MCP es abierta. Sin embargo, para la mayoría de casos en n8n, los nodos nativos + HTTP Request cubren mejor la necesidad que un servidor MCP custom.
