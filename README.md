# 🧰 MySkills

Colección de skills para agentes de código, optimizadas para **Antigravity** y compatibles con Claude Code, Codex, Cursor y [otros agentes](https://github.com/vercel-labs/skills#supported-agents).

## Instalación Rápida

### Instalar todas las skills (recomendado)

```bash
# Local (solo este proyecto)
npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill --skill commiter --skill changelog-updater -a antigravity

# Global (disponible en todos los proyectos)
npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill --skill commiter --skill changelog-updater -a antigravity -g
```

### Instalar una skill específica

```bash
npx skills add https://github.com/Baxahaun/MySkills --skill <nombre> -a antigravity
```

### Listar skills disponibles

```bash
npx skills add https://github.com/Baxahaun/MySkills --list
```

## Skills Disponibles

| Skill | Descripción | Instalación rápida |
|-------|-------------|--------------------|
| [**project-starter-skill**](skills/project-starter-skill/) | Inicializa proyectos completos con el protocolo E.T.A.P.A. v2.0. Crea estructura de directorios, infraestructura de agente, archivos de memoria y repositorio. | `npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill -a antigravity` |
| [**commiter**](skills/commiter/) | Genera mensajes de commit en español siguiendo Conventional Commits estrictos con emojis. | `npx skills add https://github.com/Baxahaun/MySkills --skill commiter -a antigravity` |
| [**changelog-updater**](skills/changelog-updater/) | Actualiza automáticamente el CHANGELOG.md del proyecto tras cada commit, categorizando cambios con emojis. | `npx skills add https://github.com/Baxahaun/MySkills --skill changelog-updater -a antigravity` |

## Alcance de Instalación

| Alcance | Flag | Descripción |
|---------|------|-------------|
| **Local** | *(por defecto)* | Se instala en `.agent/skills/` del proyecto actual. Se commitea con el proyecto y se comparte con el equipo. |
| **Global** | `-g` | Se instala en `~/.gemini/antigravity/global_skills/`. Disponible en todos los proyectos sin necesidad de reinstalar. |

## Compatibilidad

Estas skills siguen la [especificación Agent Skills](https://agentskills.io) y son compatibles con cualquier agente que soporte el estándar. Han sido diseñadas y testeadas principalmente para **Antigravity**, pero funcionan con Claude Code, Codex, Cursor y otros.

## Autor

**Xavier Crespo Gríman** — [@Baxahaun](https://github.com/Baxahaun)

## Licencia

[MIT](LICENSE) — Libre para uso, modificación y distribución, incluyendo fines comerciales, siempre que se mantenga el aviso de autoría.
