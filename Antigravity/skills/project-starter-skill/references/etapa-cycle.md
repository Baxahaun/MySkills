# El Ciclo E.T.A.P.A. — Referencia Completa

Este documento detalla cada fase del ciclo con sus reglas, procedimientos y Definitions of Done.

---

## 1️⃣ E — Estrategia (Visión y Lógica)

### Descubrimiento

Haz al usuario las 5 preguntas clave:

1. **Directriz Principal**: ¿Cuál es el resultado singular deseado?
2. **Integraciones**: ¿Qué servicios externos necesitamos? ¿Están listas las claves?
3. **Fuente de la Verdad**: ¿Dónde viven los datos primarios?
4. **Carga Útil (Payload)**: ¿Cómo y dónde debe entregarse el resultado final?
5. **Reglas de Comportamiento**: Restricciones o tono específico.

### Regla "Datos-Primero"

Antes de pasar a la siguiente fase, DEBES definir el **Esquema de Datos JSON** (Input/Output) en `genesis.md`.

Ejemplo de schema en genesis.md:

```json
{
  "input": {
    "source": "API externa",
    "schema": {
      "id": "string (UUID)",
      "timestamp": "ISO 8601",
      "data": "object"
    }
  },
  "output": {
    "destination": "webhook POST",
    "schema": {
      "processed_id": "string (UUID)",
      "result": "object",
      "status": "enum: success|error"
    }
  }
}
```

### Definition of Done — Fase E

- [ ] Las 5 preguntas de descubrimiento están respondidas.
- [ ] Esquema JSON de Input/Output definido en `genesis.md`.
- [ ] Reglas de comportamiento documentadas en `genesis.md`.
- [ ] `task_plan.md` tiene plano aprobado por el usuario.

---

## 2️⃣ T — Tests (Conectividad)

Verifica las tuberías antes de pasar el agua. El objetivo es confirmar que todos los servicios externos responden y devuelven datos con la forma esperada.

### Procedimiento

1. **Verificación de credenciales**: Lee `.env` y confirma que todas las claves necesarias existen y no están vacías.
2. **Handshake**: Construye scripts mínimos en `tools/` (ej: `test_api.py`) para verificar cada servicio.
3. **Validación de Shape**: No basta con un HTTP 200. Verifica que la respuesta coincide con el schema definido en `genesis.md`. Compara campos, tipos de datos y estructura.
4. **Bloqueo**: Si algún test falla, NO procedas a la fase de Arquitectura. Documenta el fallo en `findings.md`.

### Ejemplo de test mínimo

```python
# tools/test_api.py
import os
import requests
import json

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("API_BASE_URL")

def test_connection():
    """Verifica conexión y shape de respuesta."""
    response = requests.get(f"{BASE_URL}/health", headers={"Authorization": f"Bearer {API_KEY}"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert "id" in data, "Missing 'id' field in response"
    assert "status" in data, "Missing 'status' field in response"
    print("✅ API connection and shape validated")

if __name__ == "__main__":
    test_connection()
```

### Definition of Done — Fase T

- [ ] Todas las credenciales `.env` verificadas (existen y no están vacías).
- [ ] Scripts `test_*.py` ejecutados y pasando.
- [ ] Respuestas de APIs validadas contra el schema de `genesis.md`.
- [ ] Resultados documentados en `findings.md`.

---

## 3️⃣ A — Arquitectura (La Construcción de 3 Capas)

### Capa 1: Arquitectura (`architecture/`)

SOPs (Standard Operating Procedures) técnicos en Markdown. Cada SOP define:

- Propósito del script.
- Entradas esperadas (con referencia al schema en `genesis.md`).
- Salidas producidas.
- Casos extremos y cómo manejarlos.
- Dependencias con otras herramientas.

**Regla**: Si la lógica cambia, actualiza el SOP **antes** que el código.

### Capa 2: Navegación (Tú)

Tu capa de razonamiento como agente. Enrutas datos entre SOPs y herramientas. No ejecutas lógica de negocio directamente; delegas a los scripts.

### Capa 3: Herramientas (`tools/`)

- Scripts Python atómicos y deterministas.
- Las variables de entorno van en `.env`.
- Usa `.tmp/` para todas las operaciones intermedias.
- Cada script hace UNA cosa bien.

### Grafo de Dependencias

Cuando una herramienta produce output que consume otra, documenta el contrato en `genesis.md` bajo `## Pipeline`:

```markdown
## Pipeline

### tool_fetch.py → tool_transform.py
- Output: `.tmp/raw_data.json`
- Formato: JSON array según schema X
- Obligatorio: campo `id` presente en cada elemento

### tool_transform.py → tool_export.py
- Output: `.tmp/clean_data.json`
- Formato: JSON según schema Y
- Side-effect: false
```

### Regla de Idempotencia

Toda herramienta debe ser idempotente: ejecutarla N veces con el mismo input produce el mismo resultado sin efectos secundarios duplicados.

Las herramientas con side-effects irreversibles (envío de emails, webhooks, escritura en APIs externas) se marcan explícitamente en la cabecera del script:

```python
# META: side-effect: true
# META: idempotent: false
# META: requires-confirmation: true
```

### Definition of Done — Fase A

- [ ] SOPs escritos en `architecture/` para cada herramienta.
- [ ] Scripts implementados en `tools/`.
- [ ] Grafo de dependencias documentado en `genesis.md`.
- [ ] Tests de integración entre herramientas pasando.
- [ ] Herramientas con side-effects marcadas con META tags.

---

## 4️⃣ P — Pulido (Refinamiento)

### Templates de Output

Toda salida del sistema se valida contra una plantilla definida en `templates/`. Las plantillas se referencian desde `genesis.md` bajo `## Templates`.

```
templates/
├── report.md        # Plantilla para reportes
├── payload.json     # Estructura de entrega de datos
└── notification.md  # Formato de notificaciones
```

El pulido no es subjetivo; es verificable contra una plantilla. Si el output no coincide con el template, no pasa.

### Refinamiento de Carga Útil

Formatea todas las salidas (Markdown, HTML, JSON limpio) para entrega profesional según lo definido en `genesis.md`.

### UX/UI

Si el proyecto tiene interfaz, aplica diseños limpios e intuitivos según las especificaciones.

### Definition of Done — Fase P

- [ ] Todas las salidas validadas contra sus templates en `templates/`.
- [ ] Formatos de entrega (Markdown, HTML, JSON) verificados.
- [ ] Si hay interfaz: revisión visual completada.

---

## 5️⃣ A — Automatización (Despliegue)

### Procedimiento

1. **Limpieza**: Elimina residuos de `.tmp/`.
2. **Transferencia**: Mueve la lógica finalizada a producción/nube.
3. **Configuración**: Establece los disparadores (Cron, Webhooks).
4. **Smoke Test**: Verificación mínima en el entorno de producción.

### Definition of Done — Fase A (final)

- [ ] `.tmp/` limpio (sin archivos residuales).
- [ ] Código desplegado en destino final.
- [ ] Triggers configurados y verificados.
- [ ] Smoke test en producción pasando.
- [ ] `progress.md` actualizado con estado final.
