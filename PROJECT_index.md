# 🗺️ PROJECT_index — Dashboard MultiTodo

> **MANDATO IA:** Lee este archivo en el Paso 2 del Protocolo de Inicio de Sesión. Úsalo para ubicar los documentos SDD activos y entender el estado macro del proyecto. Actualiza el checklist de hitos SOLO cuando el usuario apruebe el cierre de una tarea mayor.

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase 2 — Ingeniería de Datos e Integración`
- **Etapa Activa:** `Etapa 2.1 — Pipeline de validación`
- **Capa Medallón Activa:** `N/A`
- **Documentos SDD Gobernantes:** Leer obligatoriamente antes de tomar decisiones arquitectónicas:
  - PRD:    `docs/reqs/f02_01_prd.md` ⬜ Pendiente de crear
  - SPEC:   `docs/specs/f02_01_spec.md` ⬜ Pendiente de crear
  - Plan:   `docs/plans/f02_01_plan.md` ⬜ Pendiente de crear
  - Tareas: `docs/tasks/f02_01_task.md` ⬜ Pendiente de crear

---

## 🏁 2. Hitos de la Fase Actual

### Fase 1 — Gobernanza y Cimientos
- ✅ **1.1** Constitución del proyecto: CLAUDE.md, PROJECT_index.md, estructura de carpetas y repositorio
- ✅ **1.2** Validación de infraestructura: verificar tablas Supabase, triggers, índices, permisos y conectividad
- ✅ **1.3** Data Contract: especificación formal del contrato de datos cliente–Triple S, validaciones y protocolo de rechazo

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Constitución del Proyecto | `CLAUDE.md` | ✅ Existe |
| Índice del Proyecto | `PROJECT_index.md` | ✅ Existe |
| Bitácora de Sesión | `PROJECT_handoff.md` | ✅ Existe |
| `.gitignore` | `.gitignore` | ✅ Existe |
| Skills de Gobernanza | `.claude/skills/` | ✅ Existe (6 skills) |
| Agentes Especializados | `.claude/agents/` | ✅ Existe (db-agent, python-dev, project-manager) |
| Orquestador Pipeline | `pipeline/main.py` | ✅ Stub creado |
| Configuración Global | `pipeline/config.yaml` | ✅ Existe (actualizado Etapa 1.2) |
| Conector Supabase | `pipeline/src/supabase_client.py` | ✅ Implementado (Etapa 1.2) |
| Tests de Integración | `pipeline/tests/test_supabase_client.py` | ✅ 12/12 verde (Etapa 1.2) |
| Dependencias Python | `pipeline/requirements.txt` | ✅ Existe (Etapa 1.2) |
| Ambiente Virtual | `pipeline/venv/` | ✅ Existe (no commiteado) |
| Pipelines | `pipeline/pipelines/` | ⬜ Vacío — Fase 2 |
| Lógica Atómica (src) | `pipeline/src/` | 🔄 Parcial — solo supabase_client.py |
| Tests Pipeline | `pipeline/tests/` | 🔄 Parcial — solo test_supabase_client.py |
| Dashboard Web | `web/` | ⬜ Placeholder — Fase 3 |
| Requerimientos (reqs) | `docs/reqs/` | ✅ Existe (f01_01, f01_02, f01_03) |
| Especificaciones (specs) | `docs/specs/` | ✅ Existe (f01_01, f01_02, f01_03) |
| Planes (plans) | `docs/plans/` | ✅ Existe (f01_01, f01_02, f01_03) |
| Tareas (tasks) | `docs/tasks/` | ✅ Existe (f01_01, f01_02, f01_03) |
| Lecciones Aprendidas | `docs/lessons/lessons-learned.md` | ✅ Existe |
| Resúmenes Ejecutivos | `docs/executives/` | ✅ f01_01 existe — f01_02 generado en esta sesión |
| Control de Cambios | `docs/changes/` | ✅ CC_00001 Aprobado |
| Schema Base de Datos | `docs/database/schema.sql` | ✅ Existe — 7 tablas sincronizadas (Etapa 1.2) |

---

## 📚 4. Índice de Documentos SDD

### Fase 1 — Gobernanza y Cimientos

| Documento | Ruta | Estado |
|---|---|---|
| PRD Etapa 1.1 | `docs/reqs/f01_01_prd.md` | ✅ Existe |
| SPEC Etapa 1.1 | `docs/specs/f01_01_spec.md` | ✅ Existe |
| Plan Etapa 1.1 | `docs/plans/f01_01_plan.md` | ✅ Existe |
| Tareas Etapa 1.1 | `docs/tasks/f01_01_task.md` | ✅ Existe |
| Ejecutivo Etapa 1.1 | `docs/executives/f01_01_executive.md` | ✅ Existe |
| PRD Etapa 1.2 | `docs/reqs/f01_02_prd.md` | ✅ Existe |
| SPEC Etapa 1.2 | `docs/specs/f01_02_spec.md` | ✅ Existe |
| Plan Etapa 1.2 | `docs/plans/f01_02_plan.md` | ✅ Existe |
| Tareas Etapa 1.2 | `docs/tasks/f01_02_task.md` | ✅ Existe (35/35 completadas) |
| Ejecutivo Etapa 1.2 | `docs/executives/f01_02_executive.md` | ✅ Existe |
| PRD Etapa 1.3 | `docs/reqs/f01_03_prd.md` | ✅ Existe |
| SPEC Etapa 1.3 | `docs/specs/f01_03_spec.md` | ✅ Existe |
| Plan Etapa 1.3 | `docs/plans/f01_03_plan.md` | ✅ Existe |
| Tareas Etapa 1.3 | `docs/tasks/f01_03_task.md` | ✅ Existe (12/12 completadas) |
| Ejecutivo Etapa 1.3 | `docs/executives/f01_03_executive.md` | ✅ Existe |

---

## 📝 5. Notas y Decisiones Registradas

- **2026-03-23** — Proyecto iniciado. `CLAUDE.md` como constitución del proyecto y fuente de verdad de reglas globales, stack tecnológico, dominio y fases. Desarrollado por Sabbia Solutions & Services (Triple S) para Almacén MultiTodo.
- **2026-03-23** — Skills de gobernanza creados bajo `.claude/skills/` con estructura de carpetas (`/update-index`, `/session-close`, `/sdd-doc`, `/close-stage`, `/change-control`). Formato: cada skill en su propia carpeta con `SKILL.md`.
- **2026-03-23** — `PROJECT_index.md` creado como primer artefacto de gobernanza. El proyecto arranca en Fase 1 — Etapa 1.1. Ningún documento SDD existe aún.
- **2026-03-23** — Etapa 1.1 completada. Repositorio Git inicializado, rama `main` activa, remoto conectado a `https://github.com/jdrodriguez1000/Almacen_MultiTodo.git`. 24 artefactos commiteados. Primer commit: `790e39a`. Avance global: 8.33% (1/12 etapas).
- **2026-03-23** — `contexto.md` y `temp.md` presentes en el directorio de trabajo pero excluidos del repositorio vía `.gitignore` por decisión del usuario.
- **2026-03-24** — CC_00001 aprobado y ejecutado. `CLAUDE.md §1` actualizado: Paso 6 agrega lectura obligatoria de `docs/database/schema.sql` al Protocolo de Inicio de Sesión.
- **2026-03-24** — Etapa 1.2 completada. `supabase_client.py` implementado con 7 funciones atómicas. 12/12 tests de integración en verde contra Supabase real (sin mocks). Tablas `tss_error_log`, `tss_pipeline_log`, `tss_quarantine` creadas en Supabase. `schema.sql` sincronizado con 7 tablas (4 `usr_*` + 3 `tss_*`). Rama `feat/etapa-1-2` creada con el código. Avance global: 16.67% (2/12 etapas).
- **2026-03-24** — SUPABASE_PROJECT_ID en `.env` corregido durante Etapa 1.2: apuntaba al proyecto inactivo `pbsqivxcwyomplqgoqva` (Demo_Bunuelos). El proyecto correcto es `ebqrvegxefahumxytgbj` (Demo_Dashboard, ACTIVE_HEALTHY).
- **2026-03-24** — Agentes especializados creados bajo `.claude/agents/`: `db-agent` (Supabase/PostgreSQL), `python-dev` (TDD Python), `project-manager` (gobernanza documental).
- **2026-03-24** — Etapa 1.3 en progreso. Los 4 documentos SDD creados: `f01_03_prd.md`, `f01_03_spec.md`, `f01_03_plan.md`, `f01_03_task.md` (12 tareas, 4/12 completadas). Políticas RLS habilitadas en las 3 tablas `tss_*` (`tss_error_log`, `tss_pipeline_log`, `tss_quarantine`). La etapa avanzará a ✅ cuando exista `docs/executives/f01_03_executive.md`.
- **2026-03-24** — Etapa 1.3 cerrada. Fase 1 completamente cerrada (3/3). Progreso global: 25%. Gate desbloqueado para Etapa 2.1.
