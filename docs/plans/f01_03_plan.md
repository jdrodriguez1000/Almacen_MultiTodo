# Plan de Implementación — Data Contract (`f01_03`)

> **Trazabilidad:** Este plan ejecuta los requerimientos de `docs/reqs/f01_03_prd.md` según el diseño de `docs/specs/f01_03_spec.md`.

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.3
**Fecha:** 2026-03-24
**Estado:** ✅ Aprobado
**Documentos relacionados:** `docs/reqs/f01_03_prd.md` | `docs/specs/f01_03_spec.md` | `docs/tasks/f01_03_task.md`

---

## 1. Resumen del Plan

La Etapa 1.3 es una etapa de **gobernanza pura**: su entregable principal son los documentos SDD que formalizan el Contrato de Datos, más la sección `data_contract` en `config.yaml` que el pipeline de Etapa 2.1 leerá. No se implementa código de validación — eso es Etapa 2.1.

**Estrategia:** Construcción documental en cascada (`PRD → SPEC → Plan → Tasks`) con una única pieza de configuración ejecutable (`config.yaml`). El cierre de la etapa requiere que los 4 documentos SDD sean internamente consistentes, rastreables entre sí y suficientes para que Etapa 2.1 pueda implementarse sin ambigüedad.

---

## 2. Ruta Crítica

```
B1 → B2 → B3 → B4
```

1. **B1 — Documentación SDD** → depende de: ninguno (punto de partida)
2. **B2 — Configuración base** → depende de: B1 (la sección `data_contract` se deriva de la SPEC)
3. **B3 — Verificación documental** → depende de: B1 y B2 (no se puede verificar sin todos los artefactos)
4. **B4 — Cierre formal** → depende de: B3 (el resumen ejecutivo requiere verificación aprobada)

---

## 3. Backlog de Trabajo (WBS)

| Bloque | Descripción | REQ / ARC relacionado | Entregable |
|---|---|---|---|
| **B1.1** | Crear `docs/reqs/f01_03_prd.md` con los 4 objetivos, 7 requerimientos funcionales, 6 fuentes de dato, 4 métricas y matriz de trazabilidad completa | `[OBJ-01]`–`[OBJ-04]`, `[REQ-01]`–`[REQ-07]` | `docs/reqs/f01_03_prd.md` |
| **B1.2** | Crear `docs/specs/f01_03_spec.md` con arquitectura `[ARC-01]`–`[ARC-07]`, esquemas Pandera, protocolo de rechazo, restricciones temporales y `config.yaml` | `[REQ-01]`–`[REQ-07]`, `[ARC-01]`–`[ARC-07]` | `docs/specs/f01_03_spec.md` |
| **B1.3** | Crear `docs/plans/f01_03_plan.md` (este documento) con ruta crítica, WBS, estrategia de pruebas y DoD | Todos los `[REQ-XX]` vía SPEC | `docs/plans/f01_03_plan.md` |
| **B1.4** | Crear `docs/tasks/f01_03_task.md` con la lista atómica de tareas ejecutables derivadas de este plan | `[TSK-1-XX]` por cada tarea | `docs/tasks/f01_03_task.md` |
| **B2.1** | Agregar sección `data_contract:` a `pipeline/config.yaml` exactamente como se especifica en SPEC §5 | `[ARC-07]`, `[REQ-03]` | `pipeline/config.yaml` actualizado |
| **B3.1** | Verificar consistencia cruzada: PRD ↔ SPEC ↔ Plan ↔ Tasks — todos los `[REQ-XX]` del PRD tienen implementación en la SPEC, tarea en el Task file y están cubiertos en el Plan | `[MET-02]`, `[MET-03]` | Checklist de consistencia completado |
| **B3.2** | Verificar que la sección `data_contract` en `config.yaml` coincide exactamente con los parámetros de SPEC §5 | `[ARC-07]`, `[CVT-15]` | `config.yaml` validado |
| **B3.3** | Verificar que los 5 códigos `ERR_MTD_001`–`ERR_MTD_005` están definidos en SPEC con condición exacta, mensaje en catálogo y comportamiento de bloqueo documentado | `[MET-03]`, `[REQ-03]` | 5/5 códigos verificados |
| **B4.1** | Crear commit atómico de la etapa en rama `main` con todos los artefactos documentales y la actualización de `config.yaml` | — | Commit `docs: etapa 1.3 — Data Contract formalizado` |
| **B4.2** | Generar resumen ejecutivo `docs/executives/f01_03_executive.md` | `[MET-02]` | Gate de avance a Etapa 2.1 desbloqueado |
| **B4.3** | Actualizar `PROJECT_index.md` — marcar Etapa 1.3 como completada y registrar Etapa 2.1 como siguiente | — | `PROJECT_index.md` actualizado |
| **B4.4** | Actualizar `PROJECT_handoff.md` con el estado exacto al cierre de sesión | — | `PROJECT_handoff.md` actualizado |

---

## 4. Estrategia de Pruebas

La Etapa 1.3 no produce código Python ejecutable — los módulos `validators/` se implementan en Etapa 2.1. La verificación de esta etapa es **documental**: confirmar que los 4 documentos SDD son consistentes, completos y accionables.

| Tipo | Qué se verifica | Cómo | Criterio de éxito |
|---|---|---|---|
| Consistencia PRD → SPEC | Cada `[REQ-XX]` del PRD tiene al menos un componente en la tabla §3 de la SPEC | Revisión cruzada de matrices de trazabilidad | 7/7 `[REQ-XX]` cubiertos |
| Consistencia SPEC → Plan | Cada módulo de `[ARC-06]` listado en la SPEC aparece en el WBS del Plan | Cruce de tablas SPEC §3 vs Plan §3 | 11/11 módulos planificados |
| Consistencia Plan → Tasks | Cada bloque del Plan tiene al menos una tarea `[TSK-1-XX]` en el Task file | Conteo de tareas por bloque | Todos los bloques cubiertos |
| Completitud de códigos ERR | Los 5 `ERR_MTD_XXX` tienen condición, mensaje en catálogo y comportamiento (`block_batch` / `quarantine_record`) | Lectura de SPEC §4.3 y §4.4 | 5/5 códigos completos |
| Configuración `config.yaml` | La sección `data_contract:` existe con todas las claves de SPEC §5 | Leer `pipeline/config.yaml` y comparar con SPEC §5 | Coincidencia exacta de claves y valores |
| Suficiencia para Etapa 2.1 | La SPEC es suficiente para que un desarrollador implemente `pipeline/src/validators/` sin preguntas adicionales | Revisión de SPEC §3 (diseño de módulos) y §4 (contratos de datos) | Sin ambigüedades en interfaces ni condiciones de validación |

---

## 5. Definición de "Hecho" (DoD)

La Etapa 1.3 se considera completada cuando se cumplen **todas** las condiciones siguientes:

- [ ] `docs/reqs/f01_03_prd.md` existe con 4 objetivos `[OBJ-XX]`, 7 requerimientos `[REQ-XX]`, 6 fuentes de dato `[DAT-XX]`, 4 métricas `[MET-XX]` y matriz de trazabilidad completa.
- [ ] `docs/specs/f01_03_spec.md` existe con `[ARC-01]`–`[ARC-07]` tageados, tabla de módulos §3 trazada a `[REQ-XX]`, protocolo de rechazo completo, restricciones temporales especificadas y sección `config.yaml` definida.
- [ ] `docs/plans/f01_03_plan.md` existe (este documento) con ruta crítica, WBS de 12 ítems y estrategia de verificación documental.
- [ ] `docs/tasks/f01_03_task.md` existe con tareas `[TSK-1-XX]` atómicas, todas en estado pendiente `[ ]`, con bloque de cierre de etapa incluido.
- [ ] `pipeline/config.yaml` contiene la sección `data_contract:` completa según SPEC §5, sin valores hardcodeados en el código.
- [ ] Verificación cruzada completada: 7/7 `[REQ-XX]` cubiertos en SPEC, Plan y Tasks.
- [ ] Los 5 códigos `ERR_MTD_001`–`ERR_MTD_005` están completamente definidos en SPEC §4.3 y §4.4.
- [ ] `docs/executives/f01_03_executive.md` existe — gate obligatorio de avance a Etapa 2.1.
- [ ] `PROJECT_index.md` actualizado con Etapa 1.3 marcada como completada.
- [ ] Commit atómico creado en rama `main` con todos los artefactos de la etapa.

---

*Documento generado con `/sdd-doc` (Modo C — Orquestador). Para lista de tareas atómicas, ver `docs/tasks/f01_03_task.md`.*
