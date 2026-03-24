# Plan de Implementación — Validación de Infraestructura (`f01_02`)

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.2
**Estado:** ✅ Aprobado
**Fecha:** 2026-03-24

> Trazabilidad: Este plan ejecuta los requerimientos de `docs/reqs/f01_02_prd.md` según el diseño de `docs/specs/f01_02_spec.md`.

---

## 1. Resumen del Plan

El objetivo de esta etapa es confirmar que Python puede hablar con Supabase, que las tablas del cliente existen con el esquema correcto, y dejar las tablas operativas de Triple S creadas y documentadas. La estrategia es de afuera hacia adentro: primero el ambiente (sin él nada funciona), luego el conector en ciclo TDD (tests primero, código después), luego las verificaciones contra Supabase real, y finalmente la documentación del estado verificado.

**Nota de ramas (Git Flow `CLAUDE.md §6`):**
- Los documentos SDD (PRD, SPEC, Plan, Tasks, schema.sql) se commitean en `main` — son gobernanza.
- El código Python (`supabase_client.py`, `requirements.txt`, `pytest.ini`, tests) va en rama `feat/etapa-1-2` → PR a `dev` al cerrar la etapa.

---

## 2. Ruta Crítica

```
B1 (Ambiente) → B2 (TDD + Conector) → B3 (Verificar usr_*) → B4 (Crear tss_*) → B5 (schema.sql + Cierre)
                                              │                      │
                                              └──────────────────────┘
                                               Ambos deben completar antes de B5
```

1. **B1 — Ambiente Python** → depende de: ninguno
2. **B2 — Módulo conector (TDD)** → depende de: B1 (venv activo para importar `supabase`)
3. **B3 — Verificación tablas `usr_*`** → depende de: B2 (módulo disponible)
4. **B4 — Creación tablas `tss_*`** → depende de: B2 (módulo disponible)
5. **B5 — Documentar `schema.sql` y cierre** → depende de: B3 + B4 (esquema real confirmado)

> **Bifurcación B3/B4:** Los bloques 3 y 4 son independientes entre sí. Se ejecutan en secuencia (B3 → B4) pero podrían paralelizarse si hubiera múltiples desarrolladores.

---

## 3. Backlog de Trabajo (WBS)

| Bloque | Descripción | REQ / ARC relacionado | Entregable |
|---|---|---|---|
| B1 | Verificar que `.env` tiene credenciales reales. Crear `venv`, instalar dependencias del stack, generar `requirements.txt` con versiones fijadas. | `[REQ-01]`, `[REQ-02]` / `[ARC-02]`, `[ARC-03]` | `pipeline/venv/` activo. `pipeline/requirements.txt` commitable. Verificación `import` exitosa. |
| B2 | **TDD:** escribir `test_supabase_client.py` completo (12 tests) ANTES de implementar el módulo. Luego implementar `supabase_client.py` función por función hasta que todos los tests pasen. | `[REQ-03]` / `[ARC-01]`, `[ARC-05]` | `pipeline/src/supabase_client.py` con 7 funciones. `pipeline/tests/test_supabase_client.py` con 12 tests en verde. |
| B3 | Ejecutar `verify_all_usr_tables()` y `verify_table_schema()` para cada una de las 4 tablas `usr_*`. Comparar resultado contra DDL de `CLAUDE.md §8`. | `[REQ-04]`, `[REQ-05]` / `[ARC-01]` | Reporte de verificación: 4/4 tablas existentes, 0 discrepancias de esquema. O protocolo de bloqueador activado si falla. |
| B4 | Ejecutar `create_tss_tables()` para crear `tss_error_log`, `tss_pipeline_log`, `tss_quarantine`. Verificar existencia y ejecutar tests CRUD. | `[REQ-06]` / `[ARC-01]` | 3/3 tablas `tss_*` accesibles en Supabase. Tests CRUD en verde. |
| B5 | Poblar `docs/database/schema.sql` con el DDL real verificado (4 tablas `usr_*` + 3 tablas `tss_*`). Crear rama `feat/etapa-1-2`, commit del código. Commit de gobernanza en `main`. | `[REQ-07]` / `[ARC-04]` | `schema.sql` con 7 tablas documentadas. Commit en `feat/etapa-1-2`. PR hacia `dev`. |

---

## 4. Protocolo de Bloqueadores

Esta etapa tiene 2 riesgos que pueden detener la ejecución. El protocolo es explícito para no improvisar.

### Bloqueador `[RSK-01]` — Tablas `usr_*` no existen

**Trigger:** `verify_all_usr_tables()` retorna `False` para una o más tablas.

**Protocolo:**
1. Registrar las tablas faltantes en el chat al usuario.
2. Proveer el DDL de `CLAUDE.md §8` listo para ejecutar en el SQL Editor de Supabase.
3. **Detener la etapa.** No avanzar a B4 ni B5.
4. Reanudar desde B3 una vez el usuario confirme que las tablas fueron creadas.

> La etapa 1.2 no puede cerrarse sin las 4 tablas `usr_*` verificadas.

### Bloqueador `[RSK-03]` — Esquema real ≠ DDL contractual

**Trigger:** `verify_table_schema()` retorna `{"match": False, ...}` para alguna tabla.

**Protocolo:**
1. Documentar la discrepancia exacta: tabla, columna, tipo esperado vs tipo real.
2. Informar al usuario con el detalle completo.
3. **Detener la implementación.** Invocar `/change-control` antes de decidir si se actualiza el contrato o se solicita al cliente corregir.
4. No poblar `schema.sql` con un esquema discrepante — esperar resolución del CC.

---

## 5. Estrategia de Pruebas

| Tipo | Qué se prueba | Archivo de test | Criterio de éxito |
|---|---|---|---|
| Integración | Conectividad Python → Supabase | `tests/test_supabase_client.py` | `verify_connectivity()` retorna `True` |
| Integración | Existencia de las 4 tablas `usr_*` | `tests/test_supabase_client.py` | `verify_all_usr_tables()` retorna 4 × `True` |
| Integración | Esquema de cada tabla `usr_*` | `tests/test_supabase_client.py` | 4 tests de `verify_table_schema()` con `"match": True` |
| Integración | Idempotencia de `create_tss_tables()` | `tests/test_supabase_client.py` | Ejecución doble sin error |
| Integración | CRUD en `tss_error_log` | `tests/test_supabase_client.py` | INSERT + SELECT sin error |
| Integración | CRUD en `tss_pipeline_log` (+ constraints) | `tests/test_supabase_client.py` | INSERT válido OK; INSERT con `mode` inválido lanza error |
| Integración | CRUD en `tss_quarantine` | `tests/test_supabase_client.py` | INSERT + SELECT sin error |
| Unitaria* | `get_client()` sin variables de entorno | `tests/test_supabase_client.py` | `EnvironmentError` lanzado (`monkeypatch`, sin conexión real) |

> **Total:** 12 tests. Todos deben pasar antes de cerrar la etapa. Sin mocks de BD (mandato `CLAUDE.md §5`).

**Comando de ejecución:**
```bash
# Desde pipeline/ con venv activo
pytest tests/test_supabase_client.py -v
```

---

## 6. Definición de "Hecho" (DoD)

> DoD adaptado para etapa de infraestructura: sin Pandera (aplica desde Etapa 2.1). La Triple Persistencia de Estado se verifica parcialmente — `tss_pipeline_log` se crea en esta etapa y el test CRUD confirma su operatividad.

- [ ] `pipeline/venv/` activo con 8 dependencias instaladas (`[MET-01]`)
- [ ] `.env` tiene credenciales reales — `get_client()` no lanza excepción (`[MET-02]`)
- [ ] `pipeline/requirements.txt` existe con versiones fijadas (`pip freeze`)
- [ ] `pipeline/src/supabase_client.py` implementado con 7 funciones (`[ARC-01]`)
- [ ] 12 tests en `pipeline/tests/test_supabase_client.py` pasan al 100% (`pytest -v`) (`[MET-02]`)
- [ ] Las 4 tablas `usr_*` existen en Supabase y coinciden con el DDL contractual (`[MET-03]`)
- [ ] Las 3 tablas `tss_*` existen en Supabase y responden a operaciones CRUD (`[MET-04]`)
- [ ] `docs/database/schema.sql` poblado con DDL de 7 tablas (`[MET-05]`)
- [ ] `config.yaml` actualizado con sección `infrastructure` y 3 claves `tss_*` en `tables` (SPEC §6)
- [ ] `pipeline/pytest.ini` creado con configuración de `pytest-dotenv`
- [ ] Rama `feat/etapa-1-2` creada con commit atómico del código: `feat: etapa 1.2 — conector Supabase e infraestructura verificada`
- [ ] PR abierto de `feat/etapa-1-2` → `dev`
- [ ] Documentos SDD commiteados en `main`: `f01_02_plan.md`, `f01_02_task.md`, `docs/database/schema.sql`
