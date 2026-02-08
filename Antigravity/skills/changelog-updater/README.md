# 📋 Changelog Updater

Skill que actualiza automáticamente el archivo `CHANGELOG.md` del proyecto basándose en el último commit realizado, categorizando cambios con emojis según Conventional Commits.

## Instalación Rápida

```bash
# Solo esta skill
npx skills add https://github.com/Baxahaun/MySkills --skill changelog-updater -a antigravity

# Con todas las skills del pack (recomendado)
npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill --skill commiter --skill changelog-updater -a antigravity

# Instalación global
npx skills add https://github.com/Baxahaun/MySkills --skill changelog-updater -a antigravity -g
```

## ¿Qué hace?

Ejecuta un script Python que:

1. **Lee el último commit** del repositorio via `git log`.
2. **Analiza el mensaje** buscando el patrón de Conventional Commits (con soporte para emojis al inicio).
3. **Formatea una entrada** con el emoji correspondiente, scope, descripción y hash corto del commit.
4. **Inserta la entrada** en la sección de la fecha actual (`YYYY-MM-DD`) del `CHANGELOG.md`.
5. **Crea el archivo** si no existe.

## Uso

```bash
python .agent/skills/changelog-updater/scripts/update_changelog.py
```

### Opciones

```bash
# Usar un archivo diferente
python scripts/update_changelog.py --file HISTORIAL.md

# Generar links a commits en GitHub
python scripts/update_changelog.py --repo-url https://github.com/Baxahaun/mi-proyecto
```

## Flujo de Trabajo

1. Haz cambios en el código.
2. Haz commit usando la skill **commiter** para formatear el mensaje.
3. El router activa esta skill automáticamente tras el commit.
4. El `CHANGELOG.md` se actualiza con la nueva entrada.

Opcionalmente, para incluir el cambio en el CHANGELOG dentro del mismo commit:

```bash
git add CHANGELOG.md
git commit --amend --no-edit
```

## Ejemplo de Output

Dado el commit:

```text
✨ feat(core): inicializa el proyecto
```

Se genera en `CHANGELOG.md`:

```markdown
## [2026-02-08]

- ✨ **(core)** inicializa el proyecto (`bf37c3a`)
```

Si se usa `--repo-url`:

```markdown
- ✨ **(core)** inicializa el proyecto [`bf37c3a`](https://github.com/Baxahaun/mi-proyecto/commit/bf37c3a...)
```

## Mapeo de Emojis

| Tipo | Emoji | Descripción |
| :--- | :---: | :--- |
| `feat` | ✨ | Nueva característica |
| `fix` | 🐛 | Corrección de errores |
| `docs` | 📚 | Documentación |
| `style` | 💄 | Estilos y formato |
| `refactor` | ♻️ | Refactorización |
| `perf` | ⚡ | Rendimiento |
| `test` | ✅ | Tests |
| `build` | 📦 | Build y dependencias |
| `ci` | 👷 | Integración continua |
| `chore` | 🔧 | Mantenimiento |
| `revert` | ⏪ | Reversión |

Commits que no siguen Conventional Commits se registran con el emoji 📝 (Misc).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `SKILL.md` | Instrucciones para el agente |
| `scripts/update_changelog.py` | Script ejecutable de actualización |

## Requisitos

- Python 3.8+
- Repositorio git inicializado con al menos un commit.

## Autor

**Xavier Crespo Gríman** — [@Baxahaun](https://github.com/Baxahaun)

## Licencia

[MIT](../../LICENSE)
