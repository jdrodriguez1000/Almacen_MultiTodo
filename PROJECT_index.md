# 🗺️ PROJECT_index — Dashboard MultiTodo

> **MANDATO IA:** Lee este archivo en el Paso 2 del Protocolo de Inicio de Sesión. Úsalo para ubicar los documentos SDD activos y entender el estado macro del proyecto. Actualiza el checklist de hitos SOLO cuando el usuario apruebe el cierre de una tarea mayor.

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase 1 — Gobernanza y Cimientos`
- **Etapa Activa:** `Etapa 1.1 — Constitución del proyecto: CLAUDE.md, PROJECT_index.md, estructura de carpetas y repositorio`
- **Capa Medallón Activa:** `N/A`
- **Documentos SDD Gobernantes:** Leer obligatoriamente antes de tomar decisiones arquitectónicas:
  - PRD:    `docs/reqs/f01_01_prd.md` ⬜ Pendiente
  - SPEC:   `docs/specs/f01_01_spec.md` ⬜ Pendiente
  - Plan:   `docs/plans/f01_01_plan.md` ⬜ Pendiente
  - Tareas: `docs/tasks/f01_01_task.md` ⬜ Pendiente

---

## 🏁 2. Hitos de la Fase Actual

### Fase 1 — Gobernanza y Cimientos
- 🔄 **1.1** Constitución del proyecto: CLAUDE.md, PROJECT_index.md, estructura de carpetas y repositorio
- ⬜ **1.2** Validación de infraestructura: verificar tablas Supabase, triggers, índices, permisos y conectividad
- ⬜ **1.3** Data Contract: especificación formal del contrato de datos cliente–Triple S, validaciones y protocolo de rechazo

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Constitución del Proyecto | `CLAUDE.md` | ✅ Existe |
| Índice del Proyecto | `PROJECT_index.md` | ✅ Existe |
| Bitácora de Sesión | `PROJECT_handoff.md` | ⬜ Pendiente |
| Orquestador Pipeline | `pipeline/main.py` | ⬜ Fase 2 |
| Configuración Global | `pipeline/config.yaml` | ⬜ Fase 2 |
| Pipelines | `pipeline/pipelines/` | ⬜ Fase 2 |
| Lógica Atómica (src) | `pipeline/src/` | ⬜ Fase 2 |
| Tests Pipeline | `pipeline/tests/` | ⬜ Fase 2 |
| Dashboard Web | `web/` | ⬜ Transversal (diferido a Fase 3) |
| Requerimientos (reqs) | `docs/reqs/` | ⬜ Pendiente |
| Especificaciones (specs) | `docs/specs/` | ⬜ Pendiente |
| Planes (plans) | `docs/plans/` | ⬜ Pendiente |
| Tareas (tasks) | `docs/tasks/` | ⬜ Pendiente |
| Lecciones Aprendidas | `docs/lessons/` | ⬜ Pendiente |
| Resúmenes Ejecutivos | `docs/executives/` | ⬜ Pendiente |
| Control de Cambios | `docs/changes/` | ⬜ Pendiente |
| Schema Base de Datos | `docs/database/schema.sql` | ⬜ Pendiente |
| Skill: update-index | `.claude/skills/update-index/SKILL.md` | ✅ Existe |
| Skill: session-close | `.claude/skills/session-close/SKILL.md` | ✅ Existe |
| Skill: sdd-doc | `.claude/skills/sdd-doc/SKILL.md` | ✅ Existe |
| Skill: close-stage | `.claude/skills/close-stage/SKILL.md` | ✅ Existe |
| Skill: change-control | `.claude/skills/change-control/SKILL.md` | ✅ Existe |

---

## 📚 4. Índice de Documentos SDD

### Fase 1 — Gobernanza y Cimientos

| Documento | Ruta | Estado |
|---|---|---|
| PRD Etapa 1.1 | `docs/reqs/f01_01_prd.md` | ⬜ Pendiente |
| SPEC Etapa 1.1 | `docs/specs/f01_01_spec.md` | ⬜ Pendiente |
| Plan Etapa 1.1 | `docs/plans/f01_01_plan.md` | ⬜ Pendiente |
| Tareas Etapa 1.1 | `docs/tasks/f01_01_task.md` | ⬜ Pendiente |
| Ejecutivo Etapa 1.1 | `docs/executives/f01_01_executive.md` | ⬜ Pendiente |
| PRD Etapa 1.2 | `docs/reqs/f01_02_prd.md` | ⬜ Pendiente |
| SPEC Etapa 1.2 | `docs/specs/f01_02_spec.md` | ⬜ Pendiente |
| Plan Etapa 1.2 | `docs/plans/f01_02_plan.md` | ⬜ Pendiente |
| Tareas Etapa 1.2 | `docs/tasks/f01_02_task.md` | ⬜ Pendiente |
| Ejecutivo Etapa 1.2 | `docs/executives/f01_02_executive.md` | ⬜ Pendiente |
| PRD Etapa 1.3 | `docs/reqs/f01_03_prd.md` | ⬜ Pendiente |
| SPEC Etapa 1.3 | `docs/specs/f01_03_spec.md` | ⬜ Pendiente |
| Plan Etapa 1.3 | `docs/plans/f01_03_plan.md` | ⬜ Pendiente |
| Tareas Etapa 1.3 | `docs/tasks/f01_03_task.md` | ⬜ Pendiente |
| Ejecutivo Etapa 1.3 | `docs/executives/f01_03_executive.md` | ⬜ Pendiente |

---

## 📝 5. Notas y Decisiones Registradas

- **2026-03-23** — Proyecto iniciado. `CLAUDE.md` como constitución del proyecto y fuente de verdad de reglas globales, stack tecnológico, dominio y fases. Desarrollado por Sabbia Solutions & Services (Triple S) para Almacén MultiTodo.
- **2026-03-23** — Skills de gobernanza creados bajo `.claude/skills/` con estructura de carpetas (`/update-index`, `/session-close`, `/sdd-doc`, `/close-stage`, `/change-control`). Formato: cada skill en su propia carpeta con `SKILL.md`.
- **2026-03-23** — `PROJECT_index.md` creado como primer artefacto de gobernanza. El proyecto arranca en Fase 1 — Etapa 1.1. Ningún documento SDD existe aún.
