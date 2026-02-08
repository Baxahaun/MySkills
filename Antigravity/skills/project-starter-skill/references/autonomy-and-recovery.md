# Gobernanza, Autonomía y Recuperación

Este documento define los niveles de permiso, el protocolo de auto-reparación y el sistema de rollback para el proyecto.

---

## 🚦 Matriz de Autonomía (Semáforo)

### 🔴 NIVEL ROJO — Detente y Pide Permiso

Estas acciones requieren aprobación explícita del usuario antes de ejecutarse:

- Modificar la estructura de datos o reglas en `genesis.md`.
- Eliminar datos persistentes o archivos fuera de `.tmp/`.
- Despliegue final a producción (Fase de Automatización).
- Envío de comunicaciones reales a terceros (emails, webhooks con side-effects).
- Creación de repositorios o recursos en servicios externos (GitHub, cloud).
- Modificar configuraciones de acceso o seguridad.

### 🟡 NIVEL AMARILLO — Avanza con Precaución

Estas acciones se pueden ejecutar pero requieren documentación inmediata:

- Instalación de dependencias nuevas.
- Modificaciones a la estructura de directorios.
- Cambios en el pipeline documentado en `genesis.md`.

### 🟢 NIVEL VERDE — Avanza con Confianza

Estas acciones no requieren permiso:

- Creación, edición y corrección de scripts en `tools/`.
- Lectura de archivos y documentación.
- Ejecución de pruebas (Tests).
- Actualización de `progress.md`, `findings.md` y `task_plan.md`.
- Instalación de skills del ecosistema.
- Escritura y limpieza de archivos en `.tmp/`.
- Auto-Reparación (con límite de reintentos).

---

## 🛠️ Principio de Auto-Templado (Self-Annealing)

Cuando una herramienta falla o ocurre un error en Nivel Verde, sigue este protocolo:

### Procedimiento

1. **Analizar**: Lee el stack trace completo. No adivines la causa.
2. **Parchear**: Arregla el script en `tools/`.
3. **Probar**: Verifica que el arreglo funciona ejecutando el script.
4. **Actualizar Memoria**: Documenta el aprendizaje en `findings.md` o en el SOP correspondiente en `architecture/` para que el error nunca se repita.

### Límite de Reintentos

**Máximo 3 intentos de auto-reparación por error.** Si al tercer intento el error persiste:

1. **Escalar a Nivel Rojo** — Pide intervención humana.
2. **Documentar el bloqueo** en `findings.md` con:

```markdown
## Bloqueo: [nombre del error]
### Fecha: [YYYY-MM-DD]
### Script: [tools/nombre.py]

### Stack Trace
[pegar stack trace completo]

### Intentos de Reparación
1. **Intento 1**: [qué se intentó] → [resultado]
2. **Intento 2**: [qué se intentó] → [resultado]
3. **Intento 3**: [qué se intentó] → [resultado]

### Hipótesis del Problema Raíz
[análisis de por qué crees que falla]

### Acción Requerida
[qué necesitas del usuario para desbloquear]
```

### Lo que NO es Auto-Templado

- No es reintentar ciegamente el mismo comando esperando un resultado diferente.
- No es ignorar el error y continuar.
- No es cambiar el schema en `genesis.md` para que el error "desaparezca".

---

## 🔄 Protocolo de Rollback

Si una fase posterior invalida una decisión de una fase anterior (por ejemplo, el schema definido en la Fase E resulta incorrecto durante la Fase A), NO modifiques `genesis.md` directamente.

### Procedimiento

1. **Documentar** en `changelog.md` qué cambio se necesita y por qué.
2. **Solicitar aprobación** (Nivel Rojo).
3. **Una vez aprobado**, actualizar `genesis.md` con nueva versión:

```markdown
## Versión 1.1 — [fecha]

### Cambio
- [descripción precisa del cambio]

### Motivo
- [por qué la versión anterior era incorrecta o insuficiente]

### Impacto
- [qué scripts/SOPs necesitan actualizarse como consecuencia]
```

4. **Propagar el cambio**: Actualizar todos los scripts y SOPs afectados por la modificación.
5. **Re-ejecutar tests**: Verificar que los cambios no rompen nada.
6. **Actualizar `progress.md`** con el rollback documentado.

### Regla de Oro

El historial de decisiones nunca se borra. Cada versión de `genesis.md` queda registrada en `changelog.md`. Esto permite entender por qué se tomó una decisión y por qué se cambió, evitando ciclos de decisiones contradictorias.
