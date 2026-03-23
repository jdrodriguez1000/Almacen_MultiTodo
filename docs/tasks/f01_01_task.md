# Task List — Constitución del Proyecto (`f01_01`)

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.1
**Estado:** 🟡 En Progreso
**Fecha:** 2026-03-23

> Trazabilidad: Estas tareas implementan el plan `docs/plans/f01_01_plan.md`.
> Actualiza este archivo marcando `[x]` cuando completes cada tarea.
> **Nunca borrar tareas completadas `[x]`** — son evidencia de trabajo realizado.

---

## Bloque 1 — Inicialización Git (`[REQ-08]` / `[ARC-04]`)

> Depende de: ninguno. Es el primer paso de la ruta crítica.

- [x] `[TSK-1-01]` Verificar que el repositorio Git está inicializado en la raíz: ejecutar `git status` y confirmar que responde sin error de "not a git repository".
- [x] `[TSK-1-02]` Crear `.gitignore` en la raíz del repositorio con todas las exclusiones mínimas obligatorias definidas en `docs/specs/f01_01_spec.md §2.1` (entornos virtuales, caché Python, secretos, `.mcp.json`, `node_modules/`, build Next.js, artefactos de datos, OS, IDEs).
- [x] `[TSK-1-03]` Verificar que `.gitignore` funciona correctamente: crear un archivo `.env` de prueba → ejecutar `git status` → confirmar que aparece como "ignored" (no como "untracked") → eliminar el `.env` de prueba.

---

## Bloque 2 — Estructura de Carpetas (`[REQ-04]`, `[REQ-05]`, `[REQ-06]` / `[ARC-06]`, `[ARC-07]`, `[ARC-08]`)

> Depende de: B1 (Git inicializado).

### `docs/` — 8 subdirectorios canónicos

- [x] `[TSK-1-04]` Verificar que existen `docs/reqs/` y `docs/specs/` (ya tienen contenido de esta etapa). Si no existen, crearlos.
- [x] `[TSK-1-05]` Crear `docs/plans/` con archivo `.gitkeep` si el directorio no existe o está vacío. *(El `f01_01_plan.md` lo poblará.)*
- [x] `[TSK-1-06]` Crear `docs/tasks/` con archivo `.gitkeep` si el directorio estaba vacío antes de este archivo. *(Este archivo `f01_01_task.md` es su primer contenido.)*
- [x] `[TSK-1-07]` Crear `docs/executives/` con archivo `.gitkeep` (permanece vacío hasta cerrar la etapa con `/close-stage`).
- [x] `[TSK-1-08]` Crear `docs/lessons/` si no existe. *(Tendrá `lessons-learned.md` al completar TSK-1-16.)*
- [x] `[TSK-1-09]` Crear `docs/changes/` con archivo `.gitkeep` (permanece vacío hasta el primer Control de Cambios).
- [x] `[TSK-1-10]` Crear `docs/database/` con archivo `.gitkeep` (permanece vacío hasta Etapa 1.2 donde se creará `schema.sql`).
- [x] `[TSK-1-11]` Verificar que `ls docs/` muestra los 8 subdirectorios: `reqs/`, `specs/`, `plans/`, `tasks/`, `executives/`, `lessons/`, `changes/`, `database/`.

### `pipeline/` — Motor de datos (stub)

- [x] `[TSK-1-12]` Crear directorio `pipeline/` si no existe.
- [x] `[TSK-1-13]` Crear `pipeline/pipelines/` con archivo `.gitkeep` (vacío hasta Fase 2).
- [x] `[TSK-1-14]` Crear `pipeline/src/` con archivo `.gitkeep` (vacío hasta Fase 2).
- [x] `[TSK-1-15]` Crear `pipeline/tests/` con archivo `.gitkeep` (vacío hasta Fase 2).

### `web/` — Dashboard (placeholder)

- [x] `[TSK-1-16]` Crear `web/` con archivo `.gitkeep` y un comentario que indique que la implementación está diferida a Fase 3.

---

## Bloque 3 — Artefactos de Gobernanza (`[REQ-01]`, `[REQ-02]`, `[REQ-03]`, `[REQ-07]`, `[REQ-09]` / `[ARC-01]`, `[ARC-02]`, `[ARC-03]`, `[ARC-05]`)

> Depende de: B2 (carpetas existentes).

- [x] `[TSK-1-17]` Verificar que `CLAUDE.md` existe en la raíz y contiene las 11 secciones §1–§11 completas (`[MET-01]`). Confirmar que §1 (Reglas), §2 (Identidad), §3 (Stack), §4 (Arquitectura), §5 (Estándares), §6 (Workflow), §7 (Dominio), §8 (Data Contract), §9 (Alertas), §10 (Fases) y §11 (Gobernanza) están presentes.
- [x] `[TSK-1-18]` Verificar que `PROJECT_index.md` existe en la raíz con las 5 secciones canónicas: `Coordenadas Actuales`, `Hitos de la Fase Actual`, `Mapa de Arquitectura (Rutas Clave)`, `Índice de Documentos SDD` y `Notas` (`[MET-02]`).
- [x] `[TSK-1-19]` Crear `PROJECT_handoff.md` en la raíz con las 5 secciones canónicas del skill `/session-close`: `Punto de Guardado`, `Archivos en el Escritorio (Working Set)`, `Contexto Inmediato`, `Bloqueador / Último Error` y `Próxima Acción Inmediata` (`[MET-02]`).
- [x] `[TSK-1-20]` Verificar que los 5 skills están correctamente instalados en `.claude/skills/[nombre]/SKILL.md`: `update-index/`, `session-close/`, `sdd-doc/`, `close-stage/`, `change-control/`. Ejecutar `ls .claude/skills/` (`[MET-04]`).
- [x] `[TSK-1-21]` Crear `docs/lessons/lessons-learned.md` con la estructura base definida en `docs/specs/f01_01_spec.md §2.4`: secciones por fase (Fase 1 con subsecciones de etapas 1.1, 1.2, 1.3; Fases 2, 3 y 4 como pendientes).

---

## Bloque 4 — Pipeline Base (`[REQ-05]`, `[REQ-10]` / `[ARC-06]`)

> Depende de: B2 (carpeta `pipeline/` existente).

- [x] `[TSK-1-22]` Crear `pipeline/config.yaml` con la estructura completa de claves placeholder definida en `docs/specs/f01_01_spec.md §2.2`. Verificar que no contiene URLs reales de Supabase, API keys ni ningún valor sensible (`[MET-06]`).
- [x] `[TSK-1-23]` Crear `pipeline/main.py` con el stub de argparse definido en `docs/specs/f01_01_spec.md §2.3`: módulo con `VALID_MODES = ["validate", "etl", "alerts"]`, función `main()` con argparse, y mensaje de stub por modo.
- [x] `[TSK-1-24]` Verificar que `pipeline/main.py` es ejecutable: correr `python pipeline/main.py --mode validate` y confirmar que imprime el mensaje stub sin error ni excepción.
- [x] `[TSK-1-25]` Verificar que `pipeline/main.py` rechaza modos inválidos: correr `python pipeline/main.py --mode invalido` y confirmar que argparse devuelve error con código de salida distinto de 0.

---

## Bloque 5 — Verificación Final y Primer Commit (`[MET-01]` a `[MET-06]`)

> Depende de: B3 + B4 (todos los artefactos creados).

- [x] `[TSK-1-26]` Ejecutar `ls docs/` y confirmar los 8 subdirectorios: `reqs/`, `specs/`, `plans/`, `tasks/`, `executives/`, `lessons/`, `changes/`, `database/`.
- [x] `[TSK-1-27]` Ejecutar `ls pipeline/` y confirmar: `main.py`, `config.yaml`, `pipelines/`, `src/`, `tests/`.
- [x] `[TSK-1-28]` Ejecutar `ls` en la raíz y confirmar artefactos de gobernanza: `CLAUDE.md`, `PROJECT_index.md`, `PROJECT_handoff.md`, `.gitignore`.
- [x] `[TSK-1-29]` Revisar `pipeline/config.yaml` visualmente: confirmar que no contiene URLs reales de Supabase ni API keys. Solo variables de entorno con formato `"${VAR}"` (`[MET-06]`).
- [x] `[TSK-1-30]` Ejecutar `git status` y revisar los archivos untracked para confirmar que ningún archivo sensible (`.env`, credenciales) está expuesto antes del commit.
- [x] `[TSK-1-31]` Crear el primer commit atómico en rama `main` con el mensaje exacto: `docs: constitución inicial del proyecto — etapa 1.1`. Stagear todos los artefactos de gobernanza producidos en esta etapa.
- [x] `[TSK-1-32]` Ejecutar `git log --oneline` y confirmar que el historial muestra el commit creado en `[TSK-1-31]`.
- [x] `[TSK-1-33]` Ejecutar `git status` después del commit y confirmar: "nothing to commit, working tree clean" (`[MET-05]`).

---

## Cierre de Etapa

> Prerrequisito: todos los bloques B1–B5 completados (32 tareas `[x]`).

- [x] `[TSK-1-34]` Invocar `/update-index` para actualizar `PROJECT_index.md` con los hitos de la Etapa 1.1 marcados como completados y las coordenadas actuales apuntando a Etapa 1.2.
- [x] `[TSK-1-35]` Invocar `/close-stage` para generar el Resumen Ejecutivo `docs/executives/f01_01_executive.md`. **Este documento es el gate obligatorio para avanzar a Etapa 1.2.**
- [x] `[TSK-1-36]` Invocar `/session-close` para reescribir `PROJECT_handoff.md` con el estado táctico exacto al cierre: etapa 1.1 completada, próxima acción es iniciar Etapa 1.2 (Validación de Infraestructura).
