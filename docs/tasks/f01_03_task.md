# Task List — Data Contract (`f01_03`)

> **Trazabilidad:** Estas tareas implementan el plan `docs/plans/f01_03_plan.md`.
> Actualiza este archivo marcando `[x]` cuando completes cada tarea.
> Convención de numeración: `[TSK-1-XX]` = Fase 1, número secuencial.

---

## Bloque 1 — Documentación SDD (B1)

> Objetivo: Crear los 4 documentos gobernantes de la etapa en orden PRD → SPEC → Plan → Tasks.
> Trazabilidad: `[OBJ-01]`–`[OBJ-04]` | `[MET-02]`

- [x] `[TSK-1-01]` Crear `docs/reqs/f01_03_prd.md` con estructura canónica `/sdd-doc` Modo A: 4 objetivos `[OBJ-XX]`, 7 requerimientos `[REQ-XX]`, 6 fuentes de dato `[DAT-XX]`, 4 métricas `[MET-XX]` y matriz de trazabilidad completa.
- [x] `[TSK-1-02]` Crear `docs/specs/f01_03_spec.md` con estructura canónica `/sdd-doc` Modo B: `[ARC-01]`–`[ARC-07]`, esquemas Pandera de `usr_ventas` e `usr_inventario`, tabla de módulos §3 trazada a `[REQ-XX]`, protocolo de rechazo completo, restricciones temporales y sección `config.yaml`.
- [x] `[TSK-1-03]` Crear `docs/plans/f01_03_plan.md` con estructura canónica `/sdd-doc` Modo C: ruta crítica B1→B2→B3→B4, WBS de 12 ítems y estrategia de verificación documental.
- [x] `[TSK-1-04]` Crear `docs/tasks/f01_03_task.md` (este archivo) con estructura canónica `/sdd-doc` Modo D: tareas atómicas `[TSK-1-XX]` por cada ítem del WBS más bloque de cierre.

---

## Bloque 2 — Configuración Base (B2)

> Objetivo: Materializar en `config.yaml` los parámetros del contrato definidos en SPEC §5.
> Trazabilidad: `[REQ-03]` | `[ARC-07]` | `[CVT-15]`

- [x] `[TSK-1-05]` Agregar sección `data_contract:` a `pipeline/config.yaml` con exactamente las claves y valores especificados en SPEC §5: `client_tables`, `tss_tables`, `error_codes`, `operating_hours_utc`, `timezone`, `delivery_deadline_utc`, `pipeline_start_utc`, `failure_threshold_pct` y `error_behavior` por código. Ningún valor del contrato puede quedar hardcodeado en el código.

---

## Bloque 3 — Verificación Documental (B3)

> Objetivo: Confirmar que los 4 documentos SDD son consistentes, completos y suficientes para que Etapa 2.1 pueda implementarse sin ambigüedad.
> Trazabilidad: `[MET-02]` | `[MET-03]` | `[OBJ-04]`

- [x] `[TSK-1-06]` Verificar consistencia cruzada PRD ↔ SPEC ↔ Plan ↔ Tasks: confirmar que los 7 `[REQ-XX]` del PRD tienen componente en la tabla §3 de la SPEC, bloque en el WBS del Plan y al menos una tarea `[TSK-1-XX]` en este archivo. Resultado esperado: 7/7 cubiertos.
- [x] `[TSK-1-07]` Verificar que la sección `data_contract:` en `pipeline/config.yaml` coincide clave a clave con SPEC §5. Confirmar que no existen valores hardcodeados en ningún módulo de `pipeline/src/`. Criterio de éxito: `[CVT-15]` satisfecho.
- [x] `[TSK-1-08]` Verificar que los 5 códigos `ERR_MTD_001`–`ERR_MTD_005` están completamente definidos en SPEC §4.3 (condición de bloqueo) y §4.4 (catálogo de mensajes). Cada código debe tener: condición exacta de activación, comportamiento (`block_batch` o `quarantine_record`), y plantilla de mensaje con variables. Resultado esperado: 5/5 completos.

---

## Bloque 4 — Cierre Formal (B4)

> Objetivo: Cerrar la etapa con todos los artefactos commiteados y los documentos de gobernanza actualizados.
> Prerequisito obligatorio: B3 completado al 100%.

- [ ] `[TSK-1-09]` Crear commit atómico en rama `main` con todos los artefactos de la etapa: `docs/reqs/f01_03_prd.md`, `docs/specs/f01_03_spec.md`, `docs/plans/f01_03_plan.md`, `docs/tasks/f01_03_task.md`, `pipeline/config.yaml`. Mensaje: `docs: etapa 1.3 — Data Contract formalizado`.
- [ ] `[TSK-1-10]` Generar resumen ejecutivo `docs/executives/f01_03_executive.md` usando `/close-stage`. Este documento es el **gate obligatorio** para iniciar Etapa 2.1 — sin él, la Fase 2 no puede comenzar.
- [ ] `[TSK-1-11]` Actualizar `PROJECT_index.md`: marcar Etapa 1.3 como ✅ completada, registrar `docs/executives/f01_03_executive.md` como existente y actualizar las coordenadas actuales a Etapa 2.1. Usar `/update-index`.
- [ ] `[TSK-1-12]` Actualizar `PROJECT_handoff.md` con el estado exacto al cierre: archivos modificados en esta sesión, próxima acción inmediata (iniciar Etapa 2.1 con sus 4 documentos SDD), bloqueadores activos (ninguno esperado). Usar `/session-close`.

---

## Resumen de Progreso

| Bloque | Total | Completadas | Pendientes |
|---|---|---|---|
| B1 — Documentación SDD | 4 | 4 ✅ | 0 |
| B2 — Configuración base | 1 | 1 ✅ | 0 |
| B3 — Verificación documental | 3 | 3 ✅ | 0 |
| B4 — Cierre formal | 4 | 0 | 4 |
| **Total** | **12** | **8** | **4** |

---

*Documento generado con `/sdd-doc` (Modo D — Ejecutor). Trazabilidad vertical: cada tarea `[TSK-1-XX]` se rastrea hasta un `[REQ-XX]` vía el WBS del Plan `f01_03_plan.md`.*
