# 🗺️ PROJECT_index — Dashboard MultiTodo

> **MANDATO IA:** Lee este archivo en el Paso 2 del Protocolo de Inicio de Sesión. Úsalo para ubicar los documentos SDD activos y entender el estado macro del proyecto. Actualiza el checklist de hitos SOLO cuando el usuario apruebe el cierre de una tarea mayor.

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase 1 — Gobernanza y Cimientos`
- **Etapa Activa:** `Etapa 1.2 — Validación de infraestructura: verificar tablas Supabase, triggers, índices, permisos y conectividad`
- **Capa Medallón Activa:** `N/A`
- **Documentos SDD Gobernantes:** Leer obligatoriamente antes de tomar decisiones arquitectónicas:
  - PRD:    `docs/reqs/f01_02_prd.md` ⬜ Pendiente de crear
  - SPEC:   `docs/specs/f01_02_spec.md` ⬜ Pendiente de crear
  - Plan:   `docs/plans/f01_02_plan.md` ⬜ Pendiente de crear
  - Tareas: `docs/tasks/f01_02_task.md` ⬜ Pendiente de crear

---

## 🏁 2. Hitos de la Fase Actual

### Fase 1 — Gobernanza y Cimientos
- ✅ **1.1** Constitución del proyecto: CLAUDE.md, PROJECT_index.md, estructura de carpetas y repositorio
- 🔄 **1.2** Validación de infraestructura: verificar tablas Supabase, triggers, índices, permisos y conectividad
- ⬜ **1.3** Data Contract: especificación formal del contrato de datos cliente–Triple S, validaciones y protocolo de rechazo

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Constitución del Proyecto | `CLAUDE.md` | ✅ Existe |
| Índice del Proyecto | `PROJECT_index.md` | ✅ Existe |
| Bitácora de Sesión | `PROJECT_handoff.md` | ✅ Existe |
| `.gitignore` | `.gitignore` | ✅ Existe |
| Skills de Gobernanza | `.claude/skills/` | ✅ Existe (5 skills) |
| Orquestador Pipeline | `pipeline/main.py` | ✅ Stub creado |
| Configuración Global | `pipeline/config.yaml` | ✅ Stub creado |
| Pipelines | `pipeline/pipelines/` | ⬜ Vacío — Fase 2 |
| Lógica Atómica (src) | `pipeline/src/` | ⬜ Vacío — Fase 2 |
| Tests Pipeline | `pipeline/tests/` | ⬜ Vacío — Fase 2 |
| Dashboard Web | `web/` | ⬜ Placeholder — Fase 3 |
| Requerimientos (reqs) | `docs/reqs/` | ✅ Existe (f01_01) |
| Especificaciones (specs) | `docs/specs/` | ✅ Existe (f01_01) |
| Planes (plans) | `docs/plans/` | ✅ Existe (f01_01) |
| Tareas (tasks) | `docs/tasks/` | ✅ Existe (f01_01) |
| Lecciones Aprendidas | `docs/lessons/lessons-learned.md` | ✅ Existe |
| Resúmenes Ejecutivos | `docs/executives/` | ⬜ Pendiente (gate de etapa 1.1) |
| Control de Cambios | `docs/changes/` | ⬜ Sin CCs activos |
| Schema Base de Datos | `docs/database/schema.sql` | ⬜ Pendiente — Etapa 1.2 |

---

## 📚 4. Índice de Documentos SDD

### Fase 1 — Gobernanza y Cimientos

| Documento | Ruta | Estado |
|---|---|---|
| PRD Etapa 1.1 | `docs/reqs/f01_01_prd.md` | ✅ Existe |
| SPEC Etapa 1.1 | `docs/specs/f01_01_spec.md` | ✅ Existe |
| Plan Etapa 1.1 | `docs/plans/f01_01_plan.md` | ✅ Existe |
| Tareas Etapa 1.1 | `docs/tasks/f01_01_task.md` | ✅ Existe |
| Ejecutivo Etapa 1.1 | `docs/executives/f01_01_executive.md` | ⬜ Pendiente (gate de avance) |
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
- **2026-03-23** — Etapa 1.1 completada. Repositorio Git inicializado, rama `main` activa, remoto conectado a `https://github.com/jdrodriguez1000/Almacen_MultiTodo.git`. 24 artefactos commiteados. Primer commit: `790e39a`. Avance global: 8.33% (1/12 etapas).
- **2026-03-23** — `contexto.md` y `temp.md` presentes en el directorio de trabajo pero excluidos del repositorio vía `.gitignore` por decisión del usuario.
