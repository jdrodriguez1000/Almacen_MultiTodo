# SPEC — Validación de Infraestructura (`f01_02`)

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.2
**Estado:** ✅ Aprobado
**Fecha:** 2026-03-24

> Trazabilidad: Este documento implementa los requerimientos definidos en `docs/reqs/f01_02_prd.md`.

---

## 1. Arquitectura Lógica

Esta etapa no produce flujos de datos de negocio — produce la **capa de conectividad y verificación** que toda la Fase 2 usará como fundación.

```
.env (credenciales)
      │
      ▼
[ARC-01] pipeline/src/supabase_client.py
      │  (get_client, verify_*, create_tss_tables)
      │
      ├──► Supabase: information_schema  ──► Verificación de esquemas usr_*
      │                                          │
      │                                          ▼
      │                                   [ARC-04] docs/database/schema.sql
      │
      └──► Supabase: public schema       ──► Creación de tablas tss_*
                                                   │
                                                   ▼
                                          tss_error_log
                                          tss_pipeline_log
                                          tss_quarantine

[ARC-02] pipeline/venv/                 ──► Ambiente aislado con dependencias
[ARC-03] pipeline/requirements.txt      ──► Declaración de versiones
[ARC-05] pipeline/tests/
         test_supabase_client.py        ──► Tests de integración contra Supabase real
```

### Componentes de Arquitectura

| ID | Componente | Responsabilidad | REQ que satisface |
|---|---|---|---|
| `[ARC-01]` | `pipeline/src/supabase_client.py` | Conector Python reutilizable. Inicializa el cliente, verifica conectividad, consulta esquemas y crea tablas `tss_*` idempotentemente. Fundación de toda la Fase 2. | `[REQ-03]`, `[REQ-04]`, `[REQ-05]`, `[REQ-06]` |
| `[ARC-02]` | `pipeline/venv/` | Ambiente virtual Python aislado. Contiene todas las dependencias del stack. No se commitea (está en `.gitignore`). | `[REQ-01]` |
| `[ARC-03]` | `pipeline/requirements.txt` | Declaración de dependencias con versiones fijadas. Se commitea al repositorio. Permite reproducir el ambiente en cualquier máquina. | `[REQ-01]` |
| `[ARC-04]` | `docs/database/schema.sql` | DDL fuente de verdad técnica de la base de datos. Refleja el estado real verificado de Supabase al cierre de la etapa. Se actualiza tras cada `CREATE TABLE` o `ALTER TABLE`. | `[REQ-07]` |
| `[ARC-05]` | `pipeline/tests/test_supabase_client.py` | Suite de tests de integración contra Supabase real. Sin mocks de base de datos (mandato `CLAUDE.md §5`). Valida conectividad, esquemas y operaciones CRUD en tablas `tss_*`. | `[REQ-08]` |

---

## 2. Especificaciones de Ingeniería de Datos

### 2.1 — Ambiente Python (`[ARC-02]` y `[ARC-03]`)

**Versión de Python:** 3.12+ (mandato `CLAUDE.md §3`)

**`pipeline/requirements.txt` — versiones mínimas a fijar:**

```text
# requirements.txt — Dashboard MultiTodo Pipeline
# Generado con: pip freeze > requirements.txt (dentro del venv activo)

supabase>=2.3.0
pandas>=2.2.0
pandera>=0.18.0
python-dotenv>=1.0.0
pydantic>=2.5.0
pytz>=2024.1
pytest>=8.0.0
pytest-dotenv>=0.5.2
```

> **Nota:** Las versiones exactas se fijan al momento de la instalación con `pip freeze`. Las versiones mínimas aquí son el piso garantizado de compatibilidad.

**Procedimiento de creación del venv:**

```bash
# Ejecutar desde el directorio pipeline/
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
```

**Verificación de activación:**

```bash
python -c "import supabase, pandas, pandera, dotenv, pydantic, pytz; print('OK')"
```

---

### 2.2 — DDL de Tablas `tss_*` Operativas (implementa `[REQ-06]`)

> Estas tablas son propiedad de Triple S. Se crean idempotentemente (`CREATE TABLE IF NOT EXISTS`) para que la función sea segura de ejecutar múltiples veces.

#### `tss_error_log` — Registro de errores del pipeline

```sql
-- tss_error_log: registro persistente de errores detectados durante la ejecución del pipeline.
-- Cada error tiene un código ERR_MTD_XXX, la tabla origen y el registro que lo causó.
CREATE TABLE IF NOT EXISTS public.tss_error_log (
  id              bigserial                    NOT NULL,
  error_code      text                         NOT NULL,  -- ERR_MTD_001 al ERR_MTD_005
  error_message   text                         NOT NULL,
  source_table    text                         NULL,      -- tabla usr_* donde se detectó el error
  source_record   jsonb                        NULL,      -- registro completo que causó el error
  pipeline_run_id text                         NULL,      -- FK lógica a tss_pipeline_log.run_id
  created_at      timestamp with time zone     NOT NULL DEFAULT now(),
  CONSTRAINT tss_error_log_pkey PRIMARY KEY (id)
);
```

#### `tss_pipeline_log` — Registro de ejecuciones del pipeline

```sql
-- tss_pipeline_log: canal 3 de la Triple Persistencia de Estado (CLAUDE.md §5).
-- Cada ejecución del pipeline (validate / etl / alerts) genera 1 registro.
CREATE TABLE IF NOT EXISTS public.tss_pipeline_log (
  id                  bigserial                    NOT NULL,
  run_id              text                         NOT NULL,  -- UUID generado al inicio de la ejecución
  mode                text                         NOT NULL,  -- 'validate' | 'etl' | 'alerts'
  status              text                         NOT NULL,  -- 'success' | 'failure' | 'partial'
  records_processed   integer                      NOT NULL DEFAULT 0,
  records_failed      integer                      NOT NULL DEFAULT 0,
  error_summary       text                         NULL,      -- resumen si status != 'success'
  started_at          timestamp with time zone     NOT NULL,
  completed_at        timestamp with time zone     NULL,      -- NULL mientras corre
  created_at          timestamp with time zone     NOT NULL DEFAULT now(),
  CONSTRAINT tss_pipeline_log_pkey           PRIMARY KEY (id),
  CONSTRAINT tss_pipeline_log_run_id_key     UNIQUE (run_id),
  CONSTRAINT tss_pipeline_log_mode_check     CHECK (mode IN ('validate', 'etl', 'alerts')),
  CONSTRAINT tss_pipeline_log_status_check   CHECK (status IN ('success', 'failure', 'partial'))
);
```

#### `tss_quarantine` — Registros rechazados por violar el Data Contract

```sql
-- tss_quarantine: destino de registros que no pasan las validaciones del Data Contract.
-- Los registros permanecen aquí hasta que el cliente corrija y reentregue los datos.
CREATE TABLE IF NOT EXISTS public.tss_quarantine (
  id              bigserial                    NOT NULL,
  source_table    text                         NOT NULL,  -- 'usr_ventas' | 'usr_inventario'
  source_record   jsonb                        NOT NULL,  -- registro raw completo
  error_code      text                         NOT NULL,  -- ERR_MTD_XXX
  error_detail    text                         NULL,      -- descripción humana del error
  pipeline_run_id text                         NULL,      -- FK lógica a tss_pipeline_log.run_id
  quarantined_at  timestamp with time zone     NOT NULL DEFAULT now(),
  resolved_at     timestamp with time zone     NULL,      -- NULL hasta que el cliente corrija
  CONSTRAINT tss_quarantine_pkey PRIMARY KEY (id)
);
```

---

### 2.3 — Esquemas Pandera

> **No aplica en esta etapa.** Los esquemas Pandera para validación de DataFrames se definen a partir de la Etapa 2.1 (Pipeline de Validación), cuando se procesen datos reales en capas Silver y Gold.

---

## 3. Diseño del Módulo `supabase_client.py` (`[ARC-01]`)

**Ruta:** `pipeline/src/supabase_client.py`
**Patrón:** Módulo funcional (funciones independientes, sin estado de clase). El cliente Supabase se inicializa una vez y se pasa como argumento o se usa directamente dentro de cada función.

### 3.1 — Contrato de Funciones

| Función | Input | Output | REQ que implementa | Descripción |
|---|---|---|---|---|
| `get_client()` | — | `supabase.Client` | `[REQ-02]`, `[REQ-03]` | Carga `.env`, inicializa y retorna el cliente Supabase. Lanza `EnvironmentError` si falta alguna variable obligatoria. |
| `verify_connectivity(client)` | `supabase.Client` | `bool` | `[REQ-03]` | Ejecuta una consulta mínima (`SELECT 1`) para confirmar que la conexión es funcional. Retorna `True` si exitoso, `False` si falla. |
| `get_table_columns(client, table_name)` | `client`, `str` | `list[dict]` | `[REQ-05]` | Consulta `information_schema.columns` para la tabla dada. Retorna lista de dicts con `column_name`, `data_type`, `is_nullable`, `column_default`. |
| `verify_table_exists(client, table_name)` | `client`, `str` | `bool` | `[REQ-04]` | Verifica existencia de la tabla en `information_schema.tables` (schema `public`). Retorna `True` si existe, `False` si no. |
| `verify_all_usr_tables(client)` | `client` | `dict[str, bool]` | `[REQ-04]` | Itera sobre las 4 tablas `usr_*` y retorna un dict `{tabla: existe}`. Si alguna es `False`, el llamador debe manejar el bloqueador. |
| `verify_table_schema(client, table_name, expected_cols)` | `client`, `str`, `list[dict]` | `dict` | `[REQ-05]` | Compara columnas reales vs esperadas. Retorna `{"match": bool, "missing": [...], "extra": [...], "type_mismatch": [...]}`. |
| `create_tss_tables(client)` | `client` | `None` | `[REQ-06]` | Ejecuta los 3 `CREATE TABLE IF NOT EXISTS` de las tablas `tss_*`. Idempotente — seguro de ejecutar múltiples veces. Lanza `RuntimeError` si alguna creación falla. |

### 3.2 — Estructura del módulo (pseudocódigo de referencia)

```python
"""
supabase_client.py — Conector Python-Supabase para Dashboard MultiTodo
Fundación reutilizable para toda la Fase 2.
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client


# ── Constantes de tablas ──────────────────────────────────────────────────────
USR_TABLES = ["usr_ventas", "usr_inventario", "usr_productos", "usr_sedes"]
TSS_OPERATIONAL_TABLES = ["tss_error_log", "tss_pipeline_log", "tss_quarantine"]

# Los DDL de creación van como constantes string en este módulo
# (o importados desde un archivo .sql) para mantener la lógica atómica en src/


# ── Funciones de conexión ─────────────────────────────────────────────────────
def get_client() -> Client:
    """
    Carga credenciales desde .env e inicializa el cliente Supabase.
    Usa SUPABASE_SERVICE_ROLE_KEY (acceso completo para el pipeline).
    """
    ...

def verify_connectivity(client: Client) -> bool:
    """Prueba de conexión mínima. Retorna True si la BD responde."""
    ...


# ── Funciones de verificación de esquema ─────────────────────────────────────
def get_table_columns(client: Client, table_name: str) -> list[dict]:
    """Consulta information_schema.columns para la tabla dada."""
    ...

def verify_table_exists(client: Client, table_name: str) -> bool:
    """Verifica que la tabla existe en el schema public."""
    ...

def verify_all_usr_tables(client: Client) -> dict[str, bool]:
    """Verifica las 4 tablas usr_* de una vez. Retorna {tabla: existe}."""
    ...

def verify_table_schema(
    client: Client,
    table_name: str,
    expected_cols: list[dict]
) -> dict:
    """
    Compara esquema real vs esperado.
    Retorna: {"match": bool, "missing": [...], "extra": [...], "type_mismatch": [...]}
    """
    ...


# ── Funciones de creación de infraestructura ─────────────────────────────────
def create_tss_tables(client: Client) -> None:
    """
    Crea las 3 tablas tss_* operativas de forma idempotente.
    Idempotente: usa CREATE TABLE IF NOT EXISTS.
    """
    ...
```

> **TDD obligatorio:** Antes de implementar cada función, se escribe su test en `pipeline/tests/test_supabase_client.py`. Mandato `CLAUDE.md §5`.

---

## 4. Contratos de Datos entre Capas

> **No aplica en esta etapa.** Esta etapa no mueve datos entre capas Medallion (Bronze → Silver → Gold). Los contratos entre capas se definen a partir de la Etapa 2.2 (ETL Bronze → Silver).

---

## 5. Especificación de Tests de Integración (`[ARC-05]`)

**Archivo:** `pipeline/tests/test_supabase_client.py`
**Runner:** `pytest`
**Prerequisito de ejecución:** `.env` con credenciales reales disponible en la raíz del repositorio.
**Mandato:** Sin mocks de base de datos. Tests de integración contra Supabase real (`CLAUDE.md §5`).

### 5.1 — Suite de tests obligatoria

| Test | Función que testea | Criterio de éxito | Tipo |
|---|---|---|---|
| `test_get_client_returns_client` | `get_client()` | Retorna una instancia de `supabase.Client` sin lanzar excepción. | Integración |
| `test_get_client_fails_without_env` | `get_client()` | Lanza `EnvironmentError` si `SUPABASE_URL` no está definida. | Unitaria* |
| `test_verify_connectivity_true` | `verify_connectivity()` | Retorna `True` con cliente válido. | Integración |
| `test_all_usr_tables_exist` | `verify_all_usr_tables()` | Las 4 tablas `usr_*` retornan `True`. | Integración |
| `test_usr_ventas_schema_matches` | `verify_table_schema()` | 0 discrepancias vs DDL de `CLAUDE.md §8` para `usr_ventas`. | Integración |
| `test_usr_inventario_schema_matches` | `verify_table_schema()` | 0 discrepancias vs DDL de `CLAUDE.md §8` para `usr_inventario`. | Integración |
| `test_usr_productos_schema_matches` | `verify_table_schema()` | 0 discrepancias vs DDL de `CLAUDE.md §8` para `usr_productos`. | Integración |
| `test_usr_sedes_schema_matches` | `verify_table_schema()` | 0 discrepancias vs DDL de `CLAUDE.md §8` para `usr_sedes`. | Integración |
| `test_create_tss_tables_idempotent` | `create_tss_tables()` | Se puede llamar dos veces sin error (idempotencia). | Integración |
| `test_tss_error_log_crud` | `create_tss_tables()` + Supabase | INSERT y SELECT en `tss_error_log` sin error. | Integración |
| `test_tss_pipeline_log_crud` | `create_tss_tables()` + Supabase | INSERT y SELECT en `tss_pipeline_log` sin error. Constraint de `mode` y `status` funciona. | Integración |
| `test_tss_quarantine_crud` | `create_tss_tables()` + Supabase | INSERT y SELECT en `tss_quarantine` sin error. | Integración |

> *`test_get_client_fails_without_env` es la única prueba sin conexión real: usa `monkeypatch` de pytest para eliminar la variable de entorno temporalmente. No es un mock de BD.

### 5.2 — Configuración de pytest

**`pipeline/pytest.ini`** (o sección en `pyproject.toml`):

```ini
[pytest]
testpaths = tests
env_files = ../.env
```

> Se usa `pytest-dotenv` para cargar automáticamente el `.env` durante la ejecución de tests.

---

## 6. Configuración (`config.yaml`)

Adiciones al `pipeline/config.yaml` existente para esta etapa:

```yaml
# Agregar bajo la sección `tables:` existente:
tables:
  # ... (claves existentes se mantienen sin cambio)

  # Tablas operativas creadas en Etapa 1.2
  error_log: "tss_error_log"
  pipeline_log: "tss_pipeline_log"
  quarantine: "tss_quarantine"

# Agregar nueva sección al final del archivo:
infrastructure:
  # Lista de tablas del cliente a verificar en Etapa 1.2
  usr_tables_to_verify:
    - "usr_ventas"
    - "usr_inventario"
    - "usr_productos"
    - "usr_sedes"
  # Lista de tablas tss_* operativas a crear en Etapa 1.2
  tss_operational_tables:
    - "tss_error_log"
    - "tss_pipeline_log"
    - "tss_quarantine"
```

---

## 7. Contenido de `docs/database/schema.sql` (`[ARC-04]`)

El archivo se crea al cierre de esta etapa con el siguiente esquema. Representa el estado real verificado de Supabase:

```sql
-- =============================================================================
-- schema.sql — Dashboard MultiTodo
-- Fuente de verdad técnica del esquema de Supabase.
-- Actualizar este archivo inmediatamente después de cada CREATE TABLE,
-- ALTER TABLE o nuevo trigger en Supabase.
-- =============================================================================
-- Última sincronización: 2026-03-24 (Etapa 1.2 — Validación de Infraestructura)
-- Tablas incluidas: 4 usr_* (cliente) + 3 tss_* operativas (Triple S)
-- =============================================================================

-- ─── TABLAS DEL CLIENTE (usr_*) ──────────────────────────────────────────────
-- Propiedad: Almacén MultiTodo
-- Acceso Triple S: SOLO LECTURA
-- No alterar DDL sin CC aprobado.

-- [DDL copiado de CLAUDE.md §8 — 4 tablas usr_*]
-- usr_sedes, usr_productos, usr_ventas, usr_inventario
-- (en ese orden por dependencias de FK)

-- ─── TABLAS OPERATIVAS DE TRIPLE S (tss_*) ───────────────────────────────────
-- Propiedad: Sabbia Solutions & Services (Triple S)
-- Acceso: Lectura/Escritura exclusiva del pipeline

-- [DDL de tss_error_log, tss_pipeline_log, tss_quarantine — ver SPEC §2.2]
```

> El contenido completo de `schema.sql` se popula al ejecutar las tareas de la etapa. La estructura de secciones es fija; el DDL es el que se verifica/crea durante la implementación.

---

## 8. Matriz de Diseño vs PRD

| REQ | Componente que lo implementa | Archivo | Notas |
|---|---|---|---|
| `[REQ-01]` | `venv` + `requirements.txt` | `pipeline/venv/` (no commiteado) + `pipeline/requirements.txt` | Se crea con `python -m venv venv` y se puebla con `pip install`. |
| `[REQ-02]` | `get_client()` — validación de variables de entorno | `pipeline/src/supabase_client.py` | Carga con `python-dotenv`. Lanza `EnvironmentError` si falta alguna variable. |
| `[REQ-03]` | `get_client()` + `verify_connectivity()` | `pipeline/src/supabase_client.py` | Módulo completo como fundación reutilizable de la Fase 2. |
| `[REQ-04]` | `verify_table_exists()` + `verify_all_usr_tables()` | `pipeline/src/supabase_client.py` | Consulta `information_schema.tables`. Si una tabla no existe → bloqueador informado al usuario. |
| `[REQ-05]` | `get_table_columns()` + `verify_table_schema()` | `pipeline/src/supabase_client.py` | Consulta `information_schema.columns`. Discrepancia → activar `/change-control` (`[RSK-03]`). |
| `[REQ-06]` | `create_tss_tables()` | `pipeline/src/supabase_client.py` | DDL de las 3 tablas en §2.2. Idempotente con `CREATE TABLE IF NOT EXISTS`. |
| `[REQ-07]` | `docs/database/schema.sql` | `docs/database/schema.sql` | Se popula al cierre de la etapa con el DDL verificado. Estructura definida en §7. |
| `[REQ-08]` | `test_supabase_client.py` — 12 tests de integración | `pipeline/tests/test_supabase_client.py` | Sin mocks de BD (mandato `CLAUDE.md §5`). Requiere `.env` con credenciales reales. |
