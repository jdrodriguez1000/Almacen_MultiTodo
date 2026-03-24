"""
supabase_client.py — Conector Python-Supabase para Dashboard MultiTodo
Fundación reutilizable para toda la Fase 2.

Patrón: módulo funcional (funciones independientes, sin estado de clase).
El cliente Supabase se inicializa una vez y se pasa como argumento a cada función.

Estrategia de introspección de esquema:
  - Las columnas se obtienen vía la OpenAPI spec expuesta por PostgREST en /rest/v1/
  - No se usa information_schema (no expuesta por PostgREST en este proyecto)
  - Para crear tablas tss_* se usa la Management API de Supabase con SUPABASE_PERSONAL_ACCESS_TOKEN
"""
import os
import httpx
from dotenv import load_dotenv
from supabase import create_client, Client
from postgrest.exceptions import APIError


# ── Constantes de tablas ──────────────────────────────────────────────────────

# Tablas del cliente (usr_*) — solo lectura para Triple S
USR_TABLES = ["usr_ventas", "usr_inventario", "usr_productos", "usr_sedes"]

# Tablas operativas de Triple S (tss_*) — creadas en Etapa 1.2
TSS_OPERATIONAL_TABLES = ["tss_error_log", "tss_pipeline_log", "tss_quarantine"]

# Código de error PostgREST cuando la tabla no existe en el schema cache
_PGRST_TABLE_NOT_FOUND = "PGRST205"


# ── DDL de tablas tss_* operativas (SPEC f01_02 §2.2) ─────────────────────────

DDL_TSS_ERROR_LOG = """
CREATE TABLE IF NOT EXISTS public.tss_error_log (
  id              bigserial                    NOT NULL,
  error_code      text                         NOT NULL,
  error_message   text                         NOT NULL,
  source_table    text                         NULL,
  source_record   jsonb                        NULL,
  pipeline_run_id text                         NULL,
  created_at      timestamp with time zone     NOT NULL DEFAULT now(),
  CONSTRAINT tss_error_log_pkey PRIMARY KEY (id)
);
"""

DDL_TSS_PIPELINE_LOG = """
CREATE TABLE IF NOT EXISTS public.tss_pipeline_log (
  id                  bigserial                    NOT NULL,
  run_id              text                         NOT NULL,
  mode                text                         NOT NULL,
  status              text                         NOT NULL,
  records_processed   integer                      NOT NULL DEFAULT 0,
  records_failed      integer                      NOT NULL DEFAULT 0,
  error_summary       text                         NULL,
  started_at          timestamp with time zone     NOT NULL,
  completed_at        timestamp with time zone     NULL,
  created_at          timestamp with time zone     NOT NULL DEFAULT now(),
  CONSTRAINT tss_pipeline_log_pkey           PRIMARY KEY (id),
  CONSTRAINT tss_pipeline_log_run_id_key     UNIQUE (run_id),
  CONSTRAINT tss_pipeline_log_mode_check     CHECK (mode IN ('validate', 'etl', 'alerts')),
  CONSTRAINT tss_pipeline_log_status_check   CHECK (status IN ('success', 'failure', 'partial'))
);
"""

DDL_TSS_QUARANTINE = """
CREATE TABLE IF NOT EXISTS public.tss_quarantine (
  id              bigserial                    NOT NULL,
  source_table    text                         NOT NULL,
  source_record   jsonb                        NOT NULL,
  error_code      text                         NOT NULL,
  error_detail    text                         NULL,
  pipeline_run_id text                         NULL,
  quarantined_at  timestamp with time zone     NOT NULL DEFAULT now(),
  resolved_at     timestamp with time zone     NULL,
  CONSTRAINT tss_quarantine_pkey PRIMARY KEY (id)
);
"""

# DDL agrupado para iterar en create_tss_tables()
_TSS_DDL_MAP = {
    "tss_error_log": DDL_TSS_ERROR_LOG,
    "tss_pipeline_log": DDL_TSS_PIPELINE_LOG,
    "tss_quarantine": DDL_TSS_QUARANTINE,
}


# ── Funciones de conexión ─────────────────────────────────────────────────────

def get_client() -> Client:
    """
    Carga credenciales desde .env e inicializa el cliente Supabase.
    Usa SUPABASE_SERVICE_ROLE_KEY para acceso completo del pipeline.
    Lanza EnvironmentError si alguna variable obligatoria no está definida.
    """
    # Buscar .env en la raíz del repositorio (un nivel arriba de pipeline/)
    _env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    load_dotenv(_env_path, override=False)

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if not url:
        raise EnvironmentError(
            "Variable de entorno SUPABASE_URL no está definida. "
            "Verifica que el archivo .env en la raíz del repositorio existe "
            "y contiene SUPABASE_URL con un valor real."
        )
    if not key:
        raise EnvironmentError(
            "Variable de entorno SUPABASE_SERVICE_ROLE_KEY no está definida. "
            "Verifica que el archivo .env en la raíz del repositorio existe "
            "y contiene SUPABASE_SERVICE_ROLE_KEY con un valor real."
        )

    return create_client(url, key)


def verify_connectivity(client: Client) -> bool:
    """
    Prueba de conexión mínima contra Supabase.
    Ejecuta un SELECT mínimo en usr_sedes para confirmar que la BD responde.
    Retorna True si exitoso, False si lanza excepción.
    """
    try:
        client.table("usr_sedes").select("id_sede").limit(1).execute()
        return True
    except Exception:
        return False


# ── Funciones de verificación de esquema ─────────────────────────────────────

def _get_openapi_spec(client: Client) -> dict:
    """
    Obtiene la OpenAPI spec de PostgREST para el proyecto Supabase.
    Retorna el dict de 'definitions' con columnas y tipos de todas las tablas expuestas.
    Lanza RuntimeError si no puede obtener la spec.
    """
    url = str(client.supabase_url)
    key = client.supabase_key

    try:
        with httpx.Client(timeout=15.0) as http:
            resp = http.get(
                f"{url}/rest/v1/",
                headers={
                    "apikey": key,
                    "Authorization": f"Bearer {key}",
                    "Accept": "application/openapi+json",
                },
            )
        if resp.status_code != 200:
            raise RuntimeError(
                f"No se pudo obtener la OpenAPI spec de PostgREST. "
                f"Status: {resp.status_code}. Body: {resp.text[:200]}"
            )
        return resp.json().get("definitions", {})
    except httpx.TimeoutException as exc:
        raise RuntimeError(
            "Timeout al obtener la OpenAPI spec de PostgREST. "
            "Verifica la conectividad con Supabase."
        ) from exc


def get_table_columns(client: Client, table_name: str) -> list[dict]:
    """
    Obtiene las columnas de una tabla vía la OpenAPI spec de PostgREST.
    Retorna lista de dicts con column_name y data_type (mapeado desde el campo 'format').
    Las columnas se retornan en el orden que PostgREST las declara.
    Retorna lista vacía si la tabla no existe en la spec.
    """
    definitions = _get_openapi_spec(client)
    table_def = definitions.get(table_name, {})
    properties = table_def.get("properties", {})

    columnas = []
    for col_name, col_props in properties.items():
        # El campo 'format' en la OpenAPI spec de Supabase contiene el tipo PostgreSQL real
        data_type = col_props.get("format", col_props.get("type", "unknown"))
        columnas.append({
            "column_name": col_name,
            "data_type": data_type,
            "is_nullable": col_name not in table_def.get("required", []),
            "column_default": col_props.get("default", None),
        })
    return columnas


def verify_table_exists(client: Client, table_name: str) -> bool:
    """
    Verifica que la tabla existe en el schema public de Supabase.
    Estrategia: intenta un SELECT mínimo y captura el error PGRST205
    (tabla no encontrada en el schema cache de PostgREST).
    Retorna True si existe, False si no.
    """
    try:
        client.table(table_name).select("*").limit(1).execute()
        return True
    except APIError as exc:
        if exc.code == _PGRST_TABLE_NOT_FOUND:
            return False
        # Otro error de PostgREST (ej. permisos) — la tabla puede existir
        raise
    except Exception:
        return False


def verify_all_usr_tables(client: Client) -> dict[str, bool]:
    """
    Verifica las 4 tablas usr_* de una vez.
    Retorna {tabla: existe} para cada tabla en USR_TABLES.
    Si alguna retorna False, el llamador debe manejar el bloqueador RSK-01.
    """
    return {tabla: verify_table_exists(client, tabla) for tabla in USR_TABLES}


def verify_table_schema(
    client: Client,
    table_name: str,
    expected_cols: list[dict],
) -> dict:
    """
    Compara el esquema real de la tabla vs las columnas esperadas.
    La comparación usa únicamente column_name (no tipos estrictos en los tests de la SPEC).
    Retorna: {"match": bool, "missing": [...], "extra": [...], "type_mismatch": [...]}
    match=True solo si missing==[], extra==[] y type_mismatch==[].
    """
    real_cols = get_table_columns(client, table_name)
    real_names = {col["column_name"] for col in real_cols}
    expected_names = {col["column_name"] for col in expected_cols}

    missing = sorted(expected_names - real_names)
    extra = sorted(real_names - expected_names)

    # Comparación de tipos para columnas presentes en ambos lados
    real_by_name = {col["column_name"]: col for col in real_cols}
    type_mismatch = []
    for col in expected_cols:
        col_name = col["column_name"]
        if col_name in real_by_name and "data_type" in col:
            real_type = real_by_name[col_name].get("data_type", "")
            expected_type = col["data_type"]
            if real_type != expected_type:
                type_mismatch.append({
                    "column": col_name,
                    "expected": expected_type,
                    "actual": real_type,
                })

    match = missing == [] and extra == [] and type_mismatch == []
    return {
        "match": match,
        "missing": missing,
        "extra": extra,
        "type_mismatch": type_mismatch,
    }


# ── Funciones de creación de infraestructura ─────────────────────────────────

def create_tss_tables(client: Client) -> None:
    """
    Crea las 3 tablas tss_* operativas de forma idempotente.
    Usa CREATE TABLE IF NOT EXISTS — seguro de ejecutar múltiples veces.

    Estrategia:
    1. Verificar cuáles tablas ya existen (via verify_table_exists).
    2. Para las que no existen, ejecutar el DDL via Management API de Supabase.
    3. Si la Management API falla, lanzar RuntimeError con instrucciones de creación manual.

    Lanza RuntimeError si alguna creación falla y no puede recuperarse.
    """
    # Verificar cuáles tablas ya existen
    tablas_pendientes = [
        tabla for tabla in TSS_OPERATIONAL_TABLES
        if not verify_table_exists(client, tabla)
    ]

    if not tablas_pendientes:
        # Idempotencia confirmada: todas las tablas ya existen
        return

    # Obtener credenciales de la Management API
    project_id = os.environ.get("SUPABASE_PROJECT_ID")
    token = os.environ.get("SUPABASE_PERSONAL_ACCESS_TOKEN")

    if not project_id or not token:
        raise RuntimeError(
            f"Las tablas {tablas_pendientes} no existen en Supabase y no se pueden crear "
            f"automáticamente porque faltan las variables SUPABASE_PROJECT_ID y/o "
            f"SUPABASE_PERSONAL_ACCESS_TOKEN en el archivo .env. "
            f"Por favor crea las tablas manualmente usando el DDL en "
            f"docs/specs/f01_02_spec.md §2.2 o via el agente db-agent."
        )

    # Ejecutar el DDL de cada tabla pendiente via Management API
    errores = []
    for tabla in tablas_pendientes:
        ddl = _TSS_DDL_MAP[tabla]
        try:
            with httpx.Client(timeout=30.0) as http:
                resp = http.post(
                    f"https://api.supabase.com/v1/projects/{project_id}/database/query",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    json={"query": ddl.strip()},
                )
            if resp.status_code not in (200, 201):
                errores.append(
                    f"{tabla}: HTTP {resp.status_code} — {resp.text[:200]}"
                )
        except httpx.TimeoutException:
            errores.append(
                f"{tabla}: Timeout al ejecutar DDL via Management API"
            )
        except Exception as exc:
            errores.append(f"{tabla}: {str(exc)[:200]}")

    if errores:
        raise RuntimeError(
            f"Error creando tablas tss_* en Supabase:\n"
            + "\n".join(f"  - {e}" for e in errores)
            + "\n\nPor favor crea las tablas manualmente usando el DDL en "
            "docs/specs/f01_02_spec.md §2.2 o via el agente db-agent."
        )
