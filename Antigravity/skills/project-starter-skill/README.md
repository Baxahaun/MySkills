# 🚀 ProjectStarterSkill

Skill global para inicializar proyectos completos usando el protocolo **E.T.A.P.A. v2.0** (Estrategia, Tests, Arquitectura, Pulido, Automatización).

## Instalación Rápida

```bash
# Instalar esta skill + commiter + changelog-updater (recomendado)
npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill --skill commiter --skill changelog-updater -a antigravity

# Solo esta skill
npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill -a antigravity

# Instalación global (disponible en todos los proyectos)
npx skills add https://github.com/Baxahaun/MySkills --skill project-starter-skill --skill commiter --skill changelog-updater -a antigravity -g
```

## ¿Qué hace?

Al activarse, ejecuta un protocolo completo de inicialización de proyecto:

1. **Descubrimiento** — Hace 5 preguntas clave al usuario para definir el alcance, integraciones, fuente de datos, entrega y restricciones.
2. **Scaffolding** — Ejecuta `init_project.py` que crea automáticamente toda la estructura de directorios y archivos base.
3. **genesis.md** — Guía la creación de la "constitución" del proyecto: schemas de datos, reglas de negocio e invariantes técnicas.
4. **Plan de tareas** — Genera `task_plan.md` con Definition of Done por cada fase del ciclo E.T.A.P.A.
5. **Skills base** — Instala las skills obligatorias (commiter, changelog-updater) y busca skills adicionales relevantes usando `npx skills find`.
6. **Repositorio** — Crea el repo en GitHub con README, LICENSE, CHANGELOG y .gitignore.

## Estructura que genera

```
proyecto/
├── .agent/
│   ├── hub/
│   │   ├── agent.md              # Instrucciones del agente
│   │   └── router.md             # Enrutamiento a skills
│   ├── skills/
│   │   ├── _registry.md          # Índice de skills instaladas
│   │   ├── commiter/
│   │   └── changelog-updater/
│   └── config/
│       └── skill-search.md       # Búsqueda de skills con npx skills
├── genesis.md                     # Constitución del proyecto
├── task_plan.md                   # Plan de fases con Definition of Done
├── progress.md                    # Diario con dashboard de estado
├── findings.md                    # Hallazgos e investigación
├── changelog.md                   # Historial de cambios en genesis.md
├── architecture/                  # SOPs técnicos
├── tools/                         # Scripts de ejecución
├── templates/                     # Plantillas de output
├── .tmp/                          # Archivos temporales
├── .env                           # Variables de entorno
├── README.md
├── LICENSE
├── CHANGELOG.md
└── .gitignore
```

## El Ciclo E.T.A.P.A.

Una vez inicializado, el proyecto avanza por 5 fases, cada una con un Definition of Done verificable:

| Fase | Nombre | Foco |
|------|--------|------|
| **E** | Estrategia | Schemas de datos y reglas en genesis.md |
| **T** | Tests | Verificar conexiones API y credenciales |
| **A** | Arquitectura | SOPs + scripts + tests de integración |
| **P** | Pulido | Outputs validados contra templates |
| **A** | Automatización | Despliegue + triggers + smoke test |

## Matriz de Autonomía

El agente opera con un sistema de semáforo:

- 🔴 **Rojo** — Pide permiso: modificar genesis.md, eliminar datos, desplegar, enviar comunicaciones externas.
- 🟢 **Verde** — Avanza solo: crear/editar scripts, ejecutar tests, actualizar logs, auto-reparar (máx. 3 intentos).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `SKILL.md` | Instrucciones para el agente |
| `scripts/init_project.py` | Script de scaffolding que genera toda la estructura |
| `references/etapa-cycle.md` | Detalle completo de las 5 fases con Definitions of Done |
| `references/autonomy-and-recovery.md` | Semáforo, auto-reparación y protocolo de rollback |

## Requisitos

- Python 3.8+
- Node.js (para `npx skills`)
- Git

## Autor

**Xavier Crespo Gríman** — [@Baxahaun](https://github.com/Baxahaun)

## Licencia

[MIT](../../LICENSE)
