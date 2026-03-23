# Plan de Implementación — Constitución del Proyecto (`f01_01`)

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.1
**Estado:** ✅ Aprobado
**Fecha:** 2026-03-23

> Trazabilidad: Este plan ejecuta los requerimientos de `docs/reqs/f01_01_prd.md` según el diseño de `docs/specs/f01_01_spec.md`.

---

## 1. Resumen del Plan

El objetivo de esta etapa es dejar el repositorio en **estado canónico de arranque**: todos los artefactos de gobernanza creados, la estructura de carpetas completa y el repositorio Git limpio con su primer commit. No se produce código de negocio.

La estrategia es secuencial y de afuera hacia adentro: primero el control de versiones (Git), luego la estructura de carpetas, luego los artefactos de contenido, y finalmente la verificación y commit. Cada bloque depende del anterior porque los artefactos de contenido necesitan las carpetas, y Git necesita que todo esté en su lugar antes del commit inicial.

---

## 2. Ruta Crítica

```
B1 (Git) → B2 (Carpetas) → B3 (Artefactos de gobernanza) → B4 (Pipeline base) → B5 (Verificación y commit)
```

1. **B1 — Inicialización Git** → depende de: ninguno
2. **B2 — Estructura de carpetas** → depende de: B1
3. **B3 — Artefactos de gobernanza** → depende de: B2
4. **B4 — Pipeline base** → depende de: B2
5. **B5 — Verificación y primer commit** → depende de: B3 + B4

---

## 3. Backlog de Trabajo (WBS)

| Bloque | Descripción | REQ / ARC relacionado | Entregable |
|---|---|---|---|
| B1 | Inicializar repositorio Git y crear `.gitignore` con exclusiones mínimas obligatorias (ver SPEC §2.1) | `[REQ-08]` / `[ARC-04]` | `.gitignore` válido. `git status` sin errores. |
| B2 | Crear los 8 subdirectorios de `docs/` con `.gitkeep` donde corresponda (ver SPEC §4) | `[REQ-04]` / `[ARC-08]` | `docs/plans/`, `docs/tasks/`, `docs/executives/`, `docs/changes/`, `docs/database/` con `.gitkeep`. |
| B2 | Crear la estructura de `pipeline/` con sus 3 subdirectorios y `.gitkeep` | `[REQ-05]` / `[ARC-06]` | `pipeline/pipelines/`, `pipeline/src/`, `pipeline/tests/` con `.gitkeep`. |
| B2 | Crear `web/` con `.gitkeep` | `[REQ-06]` / `[ARC-07]` | `web/.gitkeep` |
| B3 | Crear `PROJECT_handoff.md` con la plantilla canónica del skill `/session-close` | `[REQ-03]` / `[ARC-03]` | `PROJECT_handoff.md` en raíz con las 5 secciones. |
| B3 | Crear `docs/lessons/lessons-learned.md` con la estructura base (ver SPEC §2.4) | `[REQ-09]` / `[ARC-08]` | `docs/lessons/lessons-learned.md` con secciones por fase. |
| B4 | Crear `pipeline/config.yaml` con claves placeholder y sin secretos (ver SPEC §2.2) | `[REQ-10]` / `[ARC-06]` | `pipeline/config.yaml` con estructura completa. Sin valores sensibles. |
| B4 | Crear `pipeline/main.py` stub con argparse y los 3 modos (ver SPEC §2.3) | `[REQ-05]` / `[ARC-06]` | `pipeline/main.py` ejecutable. `python pipeline/main.py --mode validate` imprime mensaje stub. |
| B5 | Verificar completitud: todos los artefactos existen, `.gitignore` excluye correctamente, `git status` limpio | `[MET-01]` a `[MET-06]` | Checklist de verificación completado (ver §4). |
| B5 | Crear primer commit atómico en rama `main` | `[REQ-08]` | `git log` muestra 1 commit con mensaje `docs: constitución inicial del proyecto — etapa 1.1`. |

---

## 4. Estrategia de Verificación

> *Esta etapa no tiene código Python de negocio para testear con `pytest`. La verificación es estructural: confirmar que todos los artefactos existen y tienen el contenido mínimo especificado.*

| Tipo | Qué se verifica | Comando / Método | Criterio de éxito |
|---|---|---|---|
| Estructural | 8 subdirectorios en `docs/` | `ls docs/` | Aparecen: `reqs/`, `specs/`, `plans/`, `tasks/`, `executives/`, `lessons/`, `changes/`, `database/` |
| Estructural | Estructura de `pipeline/` | `ls pipeline/` | Aparecen: `main.py`, `config.yaml`, `pipelines/`, `src/`, `tests/` |
| Estructural | Skills operativos | `ls .claude/skills/` | 5 carpetas: `update-index/`, `session-close/`, `sdd-doc/`, `close-stage/`, `change-control/` |
| Estructural | Artefactos raíz | `ls` en raíz | Aparecen: `CLAUDE.md`, `PROJECT_index.md`, `PROJECT_handoff.md`, `.gitignore` |
| Funcional | `.gitignore` excluye `.env` | Crear `.env` de prueba → `git status` | `.env` aparece como "ignored", no como "untracked" |
| Funcional | `main.py` stub ejecutable | `python pipeline/main.py --mode validate` | Imprime mensaje stub sin error |
| Funcional | Repositorio Git limpio | `git status` | Muestra "nothing to commit, working tree clean" tras el primer commit |
| Contenido | `config.yaml` sin secretos | Revisar el archivo | No contiene URLs reales de Supabase ni API keys |
| Contenido | `PROJECT_handoff.md` completo | Revisar el archivo | Tiene las 5 secciones: Punto de Guardado, Working Set, Contexto, Bloqueador, Próxima Acción |

---

## 5. Definición de "Hecho" (DoD)

> *DoD adaptado para etapa de gobernanza pura: sin Pandera, sin Supabase, sin tss_pipeline_log.*

- [ ] `CLAUDE.md` existe en raíz con 11 secciones completas (`[MET-01]`)
- [ ] `PROJECT_index.md` existe con 5 secciones canónicas (`[MET-02]`)
- [ ] `PROJECT_handoff.md` existe con 5 secciones canónicas (`[MET-02]`)
- [ ] Los 8 subdirectorios de `docs/` existen (`[MET-03]`)
- [ ] `pipeline/` existe con `main.py`, `config.yaml` y 3 subcarpetas (`[MET-03]`)
- [ ] `web/` existe con `.gitkeep` (`[MET-03]`)
- [ ] Los 5 skills están en `.claude/skills/[nombre]/SKILL.md` (`[MET-04]`)
- [ ] `.gitignore` operativo — `.env` ignorado correctamente (`[MET-05]`, `[MET-06]`)
- [ ] `python pipeline/main.py --mode validate` se ejecuta sin error
- [ ] `git status` muestra árbol limpio tras el primer commit (`[MET-05]`)
- [ ] Primer commit creado: `docs: constitución inicial del proyecto — etapa 1.1`
