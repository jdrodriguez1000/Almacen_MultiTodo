# Task List — Validación de Infraestructura (`f01_02`)

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.2
**Estado:** 🟡 En Progreso
**Fecha:** 2026-03-24

> Trazabilidad: Estas tareas implementan el plan `docs/plans/f01_02_plan.md`.
> Actualiza este archivo marcando `[x]` cuando completes cada tarea.
> **Nunca borrar tareas completadas `[x]`** — son evidencia de trabajo realizado.

---

## Bloque 1 — Ambiente Python (`[REQ-01]`, `[REQ-02]` / `[ARC-02]`, `[ARC-03]`)

> Depende de: ninguno. Prerequisito de todos los demás bloques.

- [x] `[TSK-1-01]` Abrir `pipeline/.env` (o `.env` en la raíz) y verificar que las 3 variables tienen valores reales y no son placeholders literales (`"${SUPABASE_URL}"`): `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`. Si alguna es placeholder, detenerse y pedir al usuario que las complete antes de continuar.
- [x] `[TSK-1-02]` Crear el ambiente virtual Python en `pipeline/`: ejecutar `python -m venv venv` desde el directorio `pipeline/`. Confirmar que el directorio `pipeline/venv/` fue creado.
- [x] `[TSK-1-03]` Activar el venv: `source pipeline/venv/Scripts/activate` (Windows Git Bash). Verificar activación con `which python` — debe apuntar a la ruta del venv.
- [x] `[TSK-1-04]` Instalar las 8 dependencias del stack con venv activo: `pip install supabase pandas pandera python-dotenv pydantic pytz pytest pytest-dotenv`. Confirmar que no hay errores de instalación.
- [x] `[TSK-1-05]` Verificar que las 8 librerías están disponibles: ejecutar `python -c "import supabase, pandas, pandera, dotenv, pydantic, pytz, pytest; print('OK')"`. Debe imprimir `OK` sin errores (`[MET-01]`).
- [x] `[TSK-1-06]` Generar `pipeline/requirements.txt` con versiones fijadas: `pip freeze > pipeline/requirements.txt`. Abrir el archivo y confirmar que contiene al menos las 8 librerías con sus versiones exactas.
- [x] `[TSK-1-07]` Verificar que `venv/` está en `.gitignore`. Ejecutar `git status` desde la raíz — `pipeline/venv/` no debe aparecer como untracked. Si aparece, agregar `venv/` al `.gitignore`.
- [x] `[TSK-1-08]` Crear `pipeline/pytest.ini` con la configuración de `pytest-dotenv` definida en `docs/specs/f01_02_spec.md §5.2`:
  ```ini
  [pytest]
  testpaths = tests
  env_files = ../.env
  ```
  Confirmar que el archivo existe y tiene el contenido correcto.

---

## Bloque 2 — TDD: Tests primero, luego implementación (`[REQ-03]` / `[ARC-01]`, `[ARC-05]`)

> Depende de: B1 (venv activo).
> **Mandato TDD:** Escribir TODOS los tests antes de implementar una sola función. Confirmar que fallan (RED) antes de implementar.

### Sub-bloque 2A — Scaffolding de archivos

- [x] `[TSK-1-09]` Eliminar el `.gitkeep` de `pipeline/tests/` (el directorio tendrá contenido real a partir de esta tarea). Crear `pipeline/tests/__init__.py` vacío para que pytest reconozca el directorio como package Python.
- [x] `[TSK-1-10]` Eliminar el `.gitkeep` de `pipeline/src/`. Crear `pipeline/src/__init__.py` vacío.

### Sub-bloque 2B — Escribir los 12 tests (FASE RED)

- [x] `[TSK-1-11]` Crear `pipeline/tests/test_supabase_client.py` con los 12 tests de integración definidos en `docs/specs/f01_02_spec.md §5.1`. La estructura del archivo debe estar completa con todos los tests escritos **antes** de crear `supabase_client.py`. Cada test debe tener el nombre exacto de la tabla en §5.1.
- [x] `[TSK-1-12]` Ejecutar `pytest pipeline/tests/test_supabase_client.py -v` con el módulo aún sin crear. Confirmar que falla con `ImportError` o `ModuleNotFoundError` — esto es el **estado RED esperado** del ciclo TDD. Si no falla, revisar la estructura del test antes de continuar.

### Sub-bloque 2C — Implementar `supabase_client.py` función por función (FASE GREEN)

- [x] `[TSK-1-13]` Crear `pipeline/src/supabase_client.py` con el esqueleto del módulo: imports, constantes `USR_TABLES` y `TSS_OPERATIONAL_TABLES`, y funciones vacías con `pass` (o `raise NotImplementedError`). Verificar que el archivo importa sin error: `python -c "from src.supabase_client import get_client"`.
- [x] `[TSK-1-14]` Implementar `get_client()`: cargar `.env` con `python-dotenv`, leer las 3 variables de entorno, lanzar `EnvironmentError` si alguna falta, retornar el cliente Supabase inicializado con `create_client()`. Ejecutar `pytest -v -k "test_get_client"` — deben pasar los 2 tests de `get_client`.
- [x] `[TSK-1-15]` Implementar `verify_connectivity()`: ejecutar una consulta mínima contra Supabase y retornar `True`/`False`. Ejecutar `pytest -v -k "test_verify_connectivity"` — debe pasar.
- [x] `[TSK-1-16]` Implementar `verify_table_exists()`: consultar `information_schema.tables` filtrando por `table_schema = 'public'` y `table_name`. Retornar `bool`. Ejecutar `pytest -v -k "test_table_exists"` (si el test existe con ese nombre).
- [x] `[TSK-1-17]` Implementar `verify_all_usr_tables()`: iterar `USR_TABLES` llamando `verify_table_exists()` para cada una. Retornar `dict[str, bool]`. Ejecutar `pytest -v -k "test_all_usr_tables_exist"` — debe pasar (requiere que las tablas existan en Supabase; si falla aquí, ver protocolo `[RSK-01]` en el Plan).
- [x] `[TSK-1-18]` Implementar `get_table_columns()`: consultar `information_schema.columns` para la tabla dada, retornar lista de dicts con `column_name`, `data_type`, `is_nullable`, `column_default`. Ordenar por `ordinal_position`.
- [x] `[TSK-1-19]` Implementar `verify_table_schema()`: comparar columnas reales (vía `get_table_columns()`) contra `expected_cols`. Retornar `{"match": bool, "missing": [...], "extra": [...], "type_mismatch": [...]}`. Ejecutar `pytest -v -k "test_usr_ventas_schema"` — debe pasar (o activar protocolo `[RSK-03]` si hay discrepancia real).
- [x] `[TSK-1-20]` Implementar `create_tss_tables()`: ejecutar los 3 `CREATE TABLE IF NOT EXISTS` del DDL definido en `docs/specs/f01_02_spec.md §2.2` usando el cliente Supabase (via `rpc` o `postgrest`). Lanzar `RuntimeError` si alguna creación falla.
- [x] `[TSK-1-21]` Ejecutar la suite completa de tests por primera vez: `pytest pipeline/tests/test_supabase_client.py -v`. Registrar cuántos pasan. Continuar implementando hasta alcanzar 12/12. No avanzar al Bloque 3 si hay tests en rojo.

---

## Bloque 3 — Verificación de tablas `usr_*` (`[REQ-04]`, `[REQ-05]` / `[DAT-01]`, `[DAT-02]`)

> Depende de: B2 (módulo implementado y todos los tests en verde).
> **⛔ BLOQUEADOR `[RSK-01]`:** Si alguna tabla `usr_*` no existe → detener y seguir el protocolo del Plan §4.
> **⛔ BLOQUEADOR `[RSK-03]`:** Si algún esquema no coincide → detener e invocar `/change-control`.

- [x] `[TSK-1-22]` Ejecutar `verify_all_usr_tables()` desde un script Python de verificación o desde el test. Confirmar que las 4 tablas retornan `True`: `usr_ventas ✅`, `usr_inventario ✅`, `usr_productos ✅`, `usr_sedes ✅`. Si alguna retorna `False` → **DETENER** y seguir protocolo `[RSK-01]` del Plan §4.
- [x] `[TSK-1-23]` Ejecutar `verify_table_schema()` para `usr_sedes` contra el DDL de `CLAUDE.md §8`. Confirmar `"match": True` y `"missing": []`, `"extra": []`, `"type_mismatch": []`. Si hay discrepancia → **DETENER** e invocar `/change-control` (`[RSK-03]`).
- [x] `[TSK-1-24]` Ejecutar `verify_table_schema()` para `usr_productos` contra el DDL de `CLAUDE.md §8`. Confirmar `"match": True`. Si hay discrepancia → **DETENER** e invocar `/change-control` (`[RSK-03]`).
- [x] `[TSK-1-25]` Ejecutar `verify_table_schema()` para `usr_ventas` contra el DDL de `CLAUDE.md §8`. Confirmar `"match": True` (incluir verificación de constraints: `cantidad > 0`, `precio > 0`, `costo > 0`). Si hay discrepancia → **DETENER** e invocar `/change-control` (`[RSK-03]`).
- [x] `[TSK-1-26]` Ejecutar `verify_table_schema()` para `usr_inventario` contra el DDL de `CLAUDE.md §8`. Confirmar `"match": True`. Si hay discrepancia → **DETENER** e invocar `/change-control` (`[RSK-03]`).
- [x] `[TSK-1-27]` Confirmar que los 4 tests de esquema del archivo `test_supabase_client.py` pasan en verde: `test_usr_ventas_schema_matches`, `test_usr_inventario_schema_matches`, `test_usr_productos_schema_matches`, `test_usr_sedes_schema_matches` (`[MET-03]`).

---

## Bloque 4 — Creación de tablas `tss_*` (`[REQ-06]` / `[ARC-01]`)

> Depende de: B2 (módulo implementado).

- [x] `[TSK-1-28]` Ejecutar `create_tss_tables()` por primera vez. Confirmar que las 3 tablas fueron creadas: `tss_error_log ✅`, `tss_pipeline_log ✅`, `tss_quarantine ✅`. Si alguna falla, revisar el DDL en `docs/specs/f01_02_spec.md §2.2` y el mensaje de error exacto.
- [x] `[TSK-1-29]` Ejecutar `create_tss_tables()` por segunda vez. Confirmar idempotencia: la función termina sin error (`CREATE TABLE IF NOT EXISTS` no lanza excepción aunque las tablas ya existan). Este paso verifica el test `test_create_tss_tables_idempotent`.
- [x] `[TSK-1-30]` Confirmar que los 3 tests CRUD pasan en verde: `test_tss_error_log_crud`, `test_tss_pipeline_log_crud`, `test_tss_quarantine_crud`. Verificar específicamente que el constraint de `mode` en `tss_pipeline_log` rechaza valores inválidos (`[MET-04]`).
- [x] `[TSK-1-31]` Verificar que un INSERT con `mode = 'invalido'` en `tss_pipeline_log` lanza error de constraint. Este comportamiento es el guardián de integridad del log — si no falla, revisar el DDL del constraint en Supabase.

---

## Bloque 5 — Actualizar `config.yaml` y poblar `schema.sql` (`[REQ-07]` / `[ARC-04]`)

> Depende de: B3 + B4 (esquema real confirmado y tablas `tss_*` creadas).

- [x] `[TSK-1-32]` Abrir `pipeline/config.yaml` y agregar las adiciones de la SPEC §6: (1) las 3 claves `tss_*` bajo la sección `tables:` existente (`error_log`, `pipeline_log`, `quarantine`), y (2) la nueva sección `infrastructure:` con `usr_tables_to_verify` y `tss_operational_tables`. No modificar ni borrar ninguna clave existente.
- [x] `[TSK-1-33]` Verificar que `pipeline/config.yaml` no tiene valores sensibles tras la edición: ejecutar `git diff pipeline/config.yaml` y confirmar que no hay URLs de Supabase ni API keys en el diff.
- [x] `[TSK-1-34]` Abrir `docs/database/schema.sql` (actualmente vacío). Eliminar el `.gitkeep` de `docs/database/` si aún existe. Poblar `schema.sql` con la estructura de encabezado definida en `docs/specs/f01_02_spec.md §7`, seguida del DDL completo de las 7 tablas activas en este orden (por dependencias de FK): `usr_sedes` → `usr_productos` → `usr_ventas` → `usr_inventario` → `tss_error_log` → `tss_pipeline_log` → `tss_quarantine`.
- [x] `[TSK-1-35]` Verificar que `docs/database/schema.sql` no está vacío y contiene los 7 bloques `CREATE TABLE`. Confirmar que el comentario de cabecera incluye la fecha de sincronización: `2026-03-24 (Etapa 1.2)` (`[MET-05]`).

---

## Cierre de Etapa

> Prerrequisito: Bloques B1–B5 completados. Verificación final antes de commits y PR.

- [ ] `[TSK-1-36]` Ejecutar la suite completa de tests: `pytest pipeline/tests/test_supabase_client.py -v`. Confirmar **12/12 tests en verde**. Si hay fallos, resolverlos antes de continuar. No avanzar con ningún test en rojo.
- [ ] `[TSK-1-37]` Verificar Triple Persistencia de Estado (mandato `CLAUDE.md §5`): (1) salida local de `pytest` en terminal, (2) confirmar que el test CRUD insertó al menos 1 registro en `tss_pipeline_log` en Supabase y es consultable, (3) confirmar que `tss_error_log` y `tss_quarantine` son accesibles. Los 3 canales deben responder sin error.
- [ ] `[TSK-1-38]` Ejecutar `git status` desde la raíz. Confirmar que `pipeline/venv/` no aparece como untracked (excluido por `.gitignore`). Confirmar que `.env` no aparece como untracked.
- [ ] `[TSK-1-39]` Crear rama de código: `git checkout -b feat/etapa-1-2`. Stagear los archivos de código: `pipeline/src/supabase_client.py`, `pipeline/src/__init__.py`, `pipeline/tests/test_supabase_client.py`, `pipeline/tests/__init__.py`, `pipeline/requirements.txt`, `pipeline/pytest.ini`. Crear commit atómico: `feat: etapa 1.2 — conector Supabase e infraestructura verificada`.
- [ ] `[TSK-1-40]` Volver a `main`: `git checkout main`. Stagear los documentos de gobernanza: `docs/plans/f01_02_plan.md`, `docs/tasks/f01_02_task.md`, `docs/database/schema.sql`, `pipeline/config.yaml` (actualizado). Crear commit atómico: `docs: etapa 1.2 — plan, tareas y schema.sql`.
- [ ] `[TSK-1-41]` Invocar `/update-index` para actualizar `PROJECT_index.md`: marcar hito 1.2 como completado (🔄 → ✅), actualizar documentos SDD de f01_02 de "Pendiente" a "✅ Existe", confirmar que el schema.sql aparece como "✅ Existe" en el Mapa de Arquitectura.
- [ ] `[TSK-1-42]` Invocar `/close-stage` para generar el Resumen Ejecutivo `docs/executives/f01_02_executive.md`. **Este documento es el gate obligatorio para avanzar a Etapa 1.3.**
- [ ] `[TSK-1-43]` Invocar `/session-close` para reescribir `PROJECT_handoff.md` con el estado exacto al cierre: etapa 1.2 completada, rama `feat/etapa-1-2` creada, próxima acción es iniciar Etapa 1.3 (Data Contract).
