---
name: "changelog-updater"
description: "Herramienta automatizada para actualizar el archivo CHANGELOG.md basándose en el último commit realizado. Usa esta skill inmediatamente después de confirmar un commit para mantener el historial de cambios al día. Se activa con 'actualizar changelog', 'registrar cambio', 'update changelog', o automáticamente tras un commit exitoso cuando el router lo indique."
metadata:
  version: "1.0"
  type: "project"
  triggers:
    - "actualizar changelog"
    - "registrar cambio"
    - "update changelog"
    - "post-commit"
---

# Actualizador de Changelog

Esta skill mantiene actualizado el archivo `CHANGELOG.md` del proyecto de forma automática, leyendo la información directamente desde el historial de git.

## Cuándo Usar

Usa esta skill **inmediatamente después de realizar un commit** exitoso. El router debería activarla automáticamente tras detectar un commit, pero también puede invocarse manualmente.

## Cómo Usar

Ejecuta el script de actualización:

```bash
python .agent/skills/changelog-updater/scripts/update_changelog.py
```

## Qué Hace el Script

1. Obtiene el último commit del repositorio via `git log`.
2. Analiza el mensaje buscando el patrón de **Conventional Commits** (con soporte para emojis al inicio).
3. Formatea una nueva entrada para `CHANGELOG.md` incluyendo:
   - Emoji correspondiente al tipo de cambio.
   - Ámbito (scope) si existe.
   - Descripción del cambio.
   - Hash corto del commit (7 caracteres).
4. Inserta la entrada en la sección correspondiente a la fecha actual (`YYYY-MM-DD`).
5. Si no existe `CHANGELOG.md`, lo crea con la estructura base.

## Mapeo de Emojis

El script reconoce estos tipos de commit y asigna sus emojis:

| Tipo | Emoji | Descripción |
| :--- | :---: | :--- |
| `feat` | ✨ | Nueva característica |
| `fix` | 🐛 | Corrección de errores |
| `docs` | 📚 | Documentación |
| `style` | 💄 | Estilos y formato |
| `refactor` | ♻️ | Refactorización de código |
| `perf` | ⚡ | Mejoras de rendimiento |
| `test` | ✅ | Tests |
| `build` | 📦 | Build y dependencias |
| `ci` | 👷 | Integración continua |
| `chore` | 🔧 | Tareas de mantenimiento |
| `revert` | ⏪ | Reversión de cambios |

Commits que no sigan el formato Conventional Commits se registran como "Misc".

## Flujo de Trabajo Recomendado

1. Realiza tus cambios en el código.
2. Haz el commit siguiendo las convenciones (usa la skill `commiter`).
3. Ejecuta el script de esta skill.
4. (Opcional) Si deseas que el cambio en `CHANGELOG.md` forme parte del mismo commit:
   ```bash
   git add CHANGELOG.md
   git commit --amend --no-edit
   ```

## Requisitos

- Python 3 instalado.
- Repositorio git inicializado con al menos un commit.
- El script se ejecuta desde la raíz del proyecto.

## Manejo de Errores

- Si no hay commits en el repo, el script muestra un mensaje informativo y no modifica nada.
- Si `git` no está disponible, el script reporta el error y termina.
- Si el `CHANGELOG.md` tiene una estructura inesperada, añade la entrada al final como fallback.
