#!/usr/bin/env python3
"""
ProjectStarterSkill — init_project.py
Scaffolds a complete project structure following the E.T.A.P.A. v2.0 protocol.

Usage:
    python init_project.py <project-name> [--path <dir>] [--license MIT|Apache-2.0|GPL-3.0|Proprietary] [--visibility public|private]

Examples:
    python init_project.py mi-proyecto
    python init_project.py mi-proyecto --path /home/user/projects --license MIT --visibility private
"""

import argparse
import os
import sys
from datetime import datetime

# ─────────────────────────────────────────────
# File Templates
# ─────────────────────────────────────────────

def genesis_template(project_name: str) -> str:
    return f"""# {project_name} — Constitución del Proyecto (genesis.md)

> Este archivo es la **fuente de verdad absoluta** del proyecto.
> Si un script contradice lo que dice aquí, el script está mal.
> Modificar este archivo es **Nivel Rojo** (requiere aprobación).

## Versión 1.0 — {datetime.now().strftime("%Y-%m-%d")}

## Directriz Principal

<!-- ¿Cuál es el resultado singular deseado? -->
TODO: Definir tras el descubrimiento.

## Esquema de Datos

### Input

```json
{{
  "TODO": "Definir schema de entrada"
}}
```

### Output

```json
{{
  "TODO": "Definir schema de salida"
}}
```

## Reglas de Comportamiento

<!-- Restricciones de negocio -->
- TODO: Definir reglas.

## Invariantes Arquitectónicas

- Todas las herramientas leen credenciales de `.env`.
- Los archivos temporales van siempre en `.tmp/`.
- La comunicación entre tools es vía JSON.
- Toda herramienta debe ser idempotente salvo marcado explícito.

## Pipeline

<!-- Grafo de dependencias entre herramientas -->
TODO: Definir cuando las herramientas existan.

## Templates

<!-- Referencias a las plantillas de output en templates/ -->
TODO: Definir formatos de entrega.
"""


def task_plan_template(project_name: str) -> str:
    return f"""# {project_name} — Plan de Tareas (task_plan.md)

## Fase Actual: E — Estrategia (1/5)

---

## Fase E — Estrategia
### Objetivo
Definir la visión, schemas de datos y reglas del proyecto.

### Definition of Done
- [ ] Las 5 preguntas de descubrimiento respondidas.
- [ ] Esquema JSON de Input/Output definido en `genesis.md`.
- [ ] Reglas de comportamiento documentadas en `genesis.md`.
- [ ] Este plan aprobado por el usuario.

---

## Fase T — Tests
### Objetivo
Verificar todas las conexiones y credenciales.

### Definition of Done
- [ ] Todas las credenciales `.env` verificadas.
- [ ] Scripts `test_*.py` ejecutados y pasando.
- [ ] Respuestas de APIs validadas contra schema de `genesis.md`.
- [ ] Resultados documentados en `findings.md`.

---

## Fase A — Arquitectura
### Objetivo
Construir las 3 capas: SOPs, navegación y herramientas.

### Definition of Done
- [ ] SOPs escritos en `architecture/` para cada herramienta.
- [ ] Scripts implementados en `tools/`.
- [ ] Grafo de dependencias documentado en `genesis.md`.
- [ ] Tests de integración pasando.
- [ ] Herramientas con side-effects marcadas.

---

## Fase P — Pulido
### Objetivo
Refinar todas las salidas para entrega profesional.

### Definition of Done
- [ ] Todas las salidas validadas contra templates en `templates/`.
- [ ] Formatos de entrega verificados.
- [ ] Si hay interfaz: revisión visual completada.

---

## Fase A — Automatización
### Objetivo
Desplegar a producción y configurar triggers.

### Definition of Done
- [ ] `.tmp/` limpio.
- [ ] Código desplegado.
- [ ] Triggers configurados y verificados.
- [ ] Smoke test en producción pasando.
- [ ] `progress.md` actualizado con estado final.
"""


def progress_template(project_name: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""# {project_name} — Diario de Progreso (progress.md)

## Estado Actual
- Fase: Estrategia (1/5)
- Bloqueadores: Ninguno
- Último test: ⏳ Pendiente
- Próximo paso: Completar descubrimiento y poblar genesis.md

---

## Log de Ejecución

### [{today}] — Inicialización
- ✅ Estructura de proyecto creada con ProjectStarterSkill.
- ✅ Infraestructura de agente (`.agent/`) inicializada.
- ⏳ Pendiente: Descubrimiento y genesis.md.
"""


def findings_template(project_name: str) -> str:
    return f"""# {project_name} — Biblioteca de Hallazgos (findings.md)

> Investigación, descubrimientos, restricciones y aprendizajes.
> Actualiza este archivo cada vez que descubras algo relevante.

## Investigación Inicial

TODO: Documentar hallazgos tras el descubrimiento.

## Restricciones Conocidas

TODO: Documentar limitaciones técnicas o de negocio.

## Aprendizajes de Auto-Reparación

<!-- Se llena automáticamente cuando el Self-Annealing actúa -->
"""


def changelog_template(project_name: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""# {project_name} — Historial de Cambios (changelog.md)

> Registro versionado de cambios en `genesis.md`.
> Cada modificación a la constitución se documenta aquí.

## [{today}] — v1.0 Inicialización

### Cambio
- Creación inicial de `genesis.md` con estructura base.

### Motivo
- Inicialización del proyecto con ProjectStarterSkill (E.T.A.P.A. v2.0).
"""


def agent_template(project_name: str) -> str:
    return f"""# Agente del Proyecto: {project_name}

## Identidad
Eres el agente principal del proyecto **{project_name}**. Operas bajo el protocolo E.T.A.P.A. v2.0.

## Fuente de Verdad
Tu fuente de verdad es `genesis.md`. Antes de tomar cualquier decisión, consulta este archivo.

## Comportamiento
- Sigue las reglas de comportamiento definidas en `genesis.md`.
- Respeta la Matriz de Autonomía (Semáforo) para determinar qué acciones puedes tomar.
- Documenta tu progreso en `progress.md`.
- Registra hallazgos en `findings.md`.

## Skills Disponibles
Consulta `.agent/skills/_registry.md` para ver las skills instaladas.
También puedes buscar nuevas skills con `npx skills find <keyword>`.

## Ciclo de Trabajo
1. Lee `task_plan.md` para saber en qué fase estás.
2. Consulta `genesis.md` para entender los datos y reglas.
3. Usa el router (`.agent/hub/router.md`) para saber qué skill aplicar.
4. Ejecuta y documenta.
"""


def router_template() -> str:
    return """# Router de Skills

## Propósito
Este archivo define las reglas de enrutamiento entre el agente principal y las skills disponibles. Cuando el agente detecta un contexto específico, consulta estas reglas para decidir qué skill invocar.

## Reglas de Enrutamiento

### Contexto: Commit de código
- **Trigger**: El usuario pide hacer un commit o se completa un cambio de código.
- **Skill**: `commiter`
- **Acción**: Consulta la skill para formatear el mensaje de commit.

### Contexto: Post-commit
- **Trigger**: Se acaba de realizar un commit exitoso.
- **Skill**: `changelog-updater`
- **Acción**: Ejecuta `scripts/update_changelog.py` para registrar el cambio.

### Contexto: Inicialización de proyecto
- **Trigger**: El usuario quiere crear un nuevo proyecto.
- **Skill**: `ProjectStarterSkill` (global)
- **Acción**: Ejecutar el protocolo de inicialización completo.

## Cómo Añadir Nuevas Reglas

Cada regla sigue este formato:

```markdown
### Contexto: [descripción]
- **Trigger**: [qué activa la regla]
- **Skill**: [nombre de la skill]
- **Acción**: [qué debe hacer el agente]
```

Al instalar una nueva skill, añade su regla de enrutamiento aquí.
"""


def registry_template() -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""# Registro de Skills

> Índice de todas las skills instaladas en el proyecto.
> Actualiza este archivo cada vez que se instale o desinstale una skill.

## Skills Instaladas

| Skill | Versión | Fecha | Descripción |
|-------|---------|-------|-------------|
| `commiter` | 1.0 | {today} | Guía para mensajes de commit en español con Conventional Commits y emojis. |
| `changelog-updater` | 1.0 | {today} | Actualización automática de CHANGELOG.md tras cada commit. |

## Skills Recomendadas (Pendientes de Instalación)

<!-- Aquí el agente registra skills recomendadas tras analizar genesis.md -->

| Skill | Motivo | Prioridad |
|-------|--------|-----------|
| TODO | Analizar `genesis.md` para recomendar | — |
"""


def skill_search_template() -> str:
    return """# Configuración del Buscador de Skills

## Propósito
Define los criterios y herramientas que el agente usa para buscar y recomendar skills relevantes basándose en la definición del proyecto en `genesis.md`.

## Herramienta de Búsqueda

Usa el CLI del ecosistema de skills:

```bash
# Buscar skills por keyword
npx skills find <keyword>

# Listar skills disponibles en un repositorio
npx skills add <repo-url> --list

# Instalar una skill específica (local, solo este proyecto)
npx skills add <repo-url> --skill <nombre> -a antigravity

# Instalar una skill globalmente (todos los proyectos)
npx skills add <repo-url> --skill <nombre> -a antigravity -g
```

## Criterios de Búsqueda

El agente analiza `genesis.md` buscando:

1. **Stack tecnológico**: Lenguajes, frameworks, herramientas mencionadas.
2. **Integraciones**: APIs, servicios externos, bases de datos.
3. **Tipo de output**: Web, API, CLI, reportes, notificaciones.
4. **Dominio**: Finanzas, educación, e-commerce, etc.

## Fuentes de Skills

1. Ecosistema abierto: `npx skills find` (busca en skills.sh).
2. Repositorios de la comunidad en GitHub/GitLab.
3. Skills locales del usuario (custom).

## Proceso de Recomendación

1. Leer `genesis.md` completo.
2. Extraer keywords del stack, integraciones y dominio.
3. Ejecutar `npx skills find <keyword>` para cada keyword relevante.
4. Registrar recomendaciones en `_registry.md` bajo "Skills Recomendadas".
5. Presentar al usuario para aprobación (Nivel Rojo — no instalar sin permiso).
"""


def readme_template(project_name: str) -> str:
    return f"""# {project_name}

> Proyecto inicializado con [ProjectStarterSkill](https://github.com) — E.T.A.P.A. v2.0

## Descripción

TODO: Completar con la directriz principal definida en `genesis.md`.

## Estructura del Proyecto

```
├── .agent/           # Infraestructura de agente (hub, skills, config)
├── architecture/     # SOPs técnicos
├── tools/            # Scripts de ejecución
├── templates/        # Plantillas de output
├── genesis.md        # Constitución del proyecto
├── task_plan.md      # Plan de fases
├── progress.md       # Diario de ejecución
├── findings.md       # Hallazgos e investigación
└── changelog.md      # Historial de cambios en genesis.md
```

## Protocolo E.T.A.P.A.

Este proyecto sigue el protocolo **E.T.A.P.A.** (Estrategia, Tests, Arquitectura, Pulido, Automatización) para construcción determinista y autorreparable.

## Licencia

Ver archivo [LICENSE](LICENSE).
"""


def gitignore_template() -> str:
    return """# Entorno
.env
.env.local
.env.*.local

# Temporales del proyecto (E.T.A.P.A.)
.tmp/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Node
node_modules/
npm-debug.log*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""


# License templates
LICENSES = {
    "MIT": lambda name: f"""MIT License

Copyright (c) {datetime.now().year} {name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    "Apache-2.0": lambda name: f"""Copyright {datetime.now().year} {name}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
""",
    "GPL-3.0": lambda name: f"""{name}
Copyright (C) {datetime.now().year} {name}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
""",
    "Proprietary": lambda name: f"""Copyright (c) {datetime.now().year} {name}. All rights reserved.

This software and associated documentation files are proprietary and confidential.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited.
""",
}


# ─────────────────────────────────────────────
# Scaffolding Logic
# ─────────────────────────────────────────────

def create_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def write_file(path: str, content: str):
    """Write content to a file, creating parent dirs if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {os.path.relpath(path)}")


def scaffold_project(
    project_name: str,
    base_path: str = ".",
    license_type: str = "MIT",
    visibility: str = "private",
):
    """Scaffold the complete project structure."""
    
    root = os.path.join(base_path, project_name)
    
    if os.path.exists(root):
        print(f"  ❌ Error: El directorio '{root}' ya existe.")
        sys.exit(1)
    
    print(f"\n🚀 Inicializando proyecto: {project_name}")
    print(f"   Ubicación: {os.path.abspath(root)}")
    print(f"   Licencia: {license_type}")
    print(f"   Visibilidad: {visibility}")
    print()
    
    # ── Directories ──
    dirs = [
        ".agent/hub",
        ".agent/skills/commiter",
        ".agent/skills/changelog-updater/scripts",
        ".agent/config",
        "architecture",
        "tools",
        "templates",
        ".tmp",
    ]
    
    print("📂 Creando estructura de directorios...")
    for d in dirs:
        create_dir(os.path.join(root, d))
        print(f"  📁 {d}/")
    print()
    
    # ── Memory Files ──
    print("📜 Creando archivos de memoria...")
    write_file(os.path.join(root, "genesis.md"), genesis_template(project_name))
    write_file(os.path.join(root, "task_plan.md"), task_plan_template(project_name))
    write_file(os.path.join(root, "progress.md"), progress_template(project_name))
    write_file(os.path.join(root, "findings.md"), findings_template(project_name))
    write_file(os.path.join(root, "changelog.md"), changelog_template(project_name))
    print()
    
    # ── Agent Infrastructure ──
    print("🤖 Creando infraestructura de agente...")
    write_file(os.path.join(root, ".agent/hub/agent.md"), agent_template(project_name))
    write_file(os.path.join(root, ".agent/hub/router.md"), router_template())
    write_file(os.path.join(root, ".agent/skills/_registry.md"), registry_template())
    write_file(os.path.join(root, ".agent/config/skill-search.md"), skill_search_template())
    print()
    
    # ── Repository Files ──
    print("📦 Creando archivos de repositorio...")
    write_file(os.path.join(root, "README.md"), readme_template(project_name))
    write_file(os.path.join(root, ".gitignore"), gitignore_template())
    
    # License
    license_fn = LICENSES.get(license_type)
    if license_fn:
        write_file(os.path.join(root, "LICENSE"), license_fn(project_name))
    
    # CHANGELOG.md (git-level, separate from changelog.md which tracks genesis.md)
    today = datetime.now().strftime("%Y-%m-%d")
    write_file(
        os.path.join(root, "CHANGELOG.md"),
        f"# Changelog\n\n## [{today}]\n\n- 🎉 Inicialización del proyecto con ProjectStarterSkill (E.T.A.P.A. v2.0)\n",
    )
    
    # .env placeholder
    write_file(
        os.path.join(root, ".env"),
        "# Credenciales y variables de entorno\n# Nunca commitear este archivo\n\n",
    )
    
    # .tmp/.gitkeep
    write_file(os.path.join(root, ".tmp/.gitkeep"), "")
    print()
    
    # ── Summary ──
    print("=" * 50)
    print(f"✅ Proyecto '{project_name}' inicializado correctamente.")
    print()
    print("📋 Próximos pasos:")
    print("  1. Responde las preguntas de descubrimiento.")
    print("  2. Puebla genesis.md con schemas y reglas.")
    print("  3. Instala las skills base (commiter, changelog-updater).")
    print("  4. Crea el repositorio en GitHub.")
    print("  5. Realiza el primer commit.")
    print()
    
    return root


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ProjectStarterSkill — Inicializa un proyecto E.T.A.P.A. v2.0"
    )
    parser.add_argument("name", help="Nombre del proyecto")
    parser.add_argument("--path", default=".", help="Directorio base (default: actual)")
    parser.add_argument(
        "--license",
        default="MIT",
        choices=["MIT", "Apache-2.0", "GPL-3.0", "Proprietary"],
        help="Tipo de licencia (default: MIT)",
    )
    parser.add_argument(
        "--visibility",
        default="private",
        choices=["public", "private"],
        help="Visibilidad del repositorio (default: private)",
    )
    
    args = parser.parse_args()
    scaffold_project(args.name, args.path, args.license, args.visibility)


if __name__ == "__main__":
    main()
