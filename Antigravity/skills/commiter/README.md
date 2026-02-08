# ✨ Commiter

Skill que guía al agente para generar mensajes de commit en español siguiendo **Conventional Commits** estrictos con emojis.

## Instalación Rápida

```bash
# Solo esta skill
npx skills add https://github.com/Baxahaun/MySkills --skill commiter -a antigravity

# Con todas las skills del pack (recomendado)
npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill --skill commiter --skill changelog-updater -a antigravity

# Instalación global
npx skills add https://github.com/Baxahaun/MySkills --skill commiter -a antigravity -g
```

## ¿Qué hace?

Cuando el usuario pide hacer un commit o se completa un cambio de código, el agente sigue estas reglas:

1. **Analiza los cambios** realizados en el código.
2. **Selecciona el tipo** de commit apropiado (feat, fix, docs, refactor, etc.).
3. **Formatea el mensaje** con emoji, tipo, alcance y descripción en español.
4. **Genera un cuerpo detallado** obligatorio explicando qué, por qué y detalles técnicos.
5. **Ejecuta el commit** con el formato correcto.

## Formato

```text
<emoji> <tipo>(<alcance>): <descripción corta>

<cuerpo detallado y extenso>

<footer>
```

## Tipos y Emojis

| Emoji | Tipo | Descripción |
| :---: | :--- | :--- |
| ✨ | `feat` | Nueva característica |
| 🐛 | `fix` | Corrección de bug |
| 📚 | `docs` | Documentación |
| 💄 | `style` | Formato y estilo (sin cambio lógico) |
| ♻️ | `refactor` | Refactorización |
| ⚡ | `perf` | Mejora de rendimiento |
| ✅ | `test` | Tests |
| 📦 | `build` | Build y dependencias |
| 👷 | `ci` | Integración continua |
| 🔧 | `chore` | Mantenimiento |
| ⏪ | `revert` | Reversión |

## Ejemplo

```text
✨ feat(auth): integra login social con Google

Se ha implementado la autenticación mediante OAuth2 con Google para facilitar
el acceso a nuevos usuarios.

Cambios principales:
- Agrega configuración de estrategia de Passport.js para Google.
- Crea nuevas rutas de callback en el controlador de autenticación.
- Actualiza el modelo de Usuario para almacenar el providerId.

Motivación:
Reducir la fricción en el registro de usuarios y aumentar la conversión.
```

## Reglas

- El emoji es obligatorio al inicio.
- Todo en **español**.
- Título máximo **50 caracteres** (sin contar emoji).
- Cuerpo **obligatorio** y detallado.
- Modo **imperativo** en el asunto ("agrega", no "agregado").

## Integración

Después de un commit exitoso, el router del agente activa automáticamente la skill **changelog-updater** para registrar el cambio en `CHANGELOG.md`.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `SKILL.md` | Instrucciones completas para el agente |

Esta skill no requiere scripts — es puramente instructiva. El agente ejecuta `git commit` directamente.

## Autor

**Xavier Crespo Gríman** — [@Baxahaun](https://github.com/Baxahaun)

## Licencia

[MIT](../../LICENSE)
