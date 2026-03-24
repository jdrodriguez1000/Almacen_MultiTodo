"""
test_supabase_client.py — Tests de integración para supabase_client.py
Etapa 1.2: Validación de Infraestructura — Dashboard MultiTodo

Mandato CLAUDE.md §5: Sin mocks de base de datos.
Tests de integración contra Supabase real.
Prerequisito: .env con credenciales reales en la raíz del repositorio.
"""
import uuid
import pytest
from datetime import datetime, timezone

from src.supabase_client import (
    get_client,
    verify_connectivity,
    verify_all_usr_tables,
    verify_table_schema,
    create_tss_tables,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    """Retorna un cliente Supabase válido para todos los tests del módulo."""
    return get_client()


# ── Columnas esperadas por tabla (basadas en CLAUDE.md §8) ───────────────────

EXPECTED_USR_SEDES = [
    {"column_name": "id_sede"},
    {"column_name": "pais"},
    {"column_name": "ciudad"},
    {"column_name": "nombre_sede"},
    {"column_name": "created_at"},
    {"column_name": "updated_at"},
]

EXPECTED_USR_PRODUCTOS = [
    {"column_name": "sku"},
    {"column_name": "nombre"},
    {"column_name": "familia"},
    {"column_name": "categoria"},
    {"column_name": "subcategoria"},
    {"column_name": "created_at"},
    {"column_name": "updated_at"},
]

EXPECTED_USR_VENTAS = [
    {"column_name": "id_venta"},
    {"column_name": "fecha_hora"},
    {"column_name": "sku"},
    {"column_name": "id_sede"},
    {"column_name": "cantidad"},
    {"column_name": "precio"},
    {"column_name": "costo"},
    {"column_name": "created_at"},
    {"column_name": "updated_at"},
]

EXPECTED_USR_INVENTARIO = [
    {"column_name": "sku"},
    {"column_name": "id_sede"},
    {"column_name": "stock_fisico"},
    {"column_name": "costo_reposicion"},
    {"column_name": "created_at"},
    {"column_name": "updated_at"},
]


# ── Tests de conexión ─────────────────────────────────────────────────────────

def test_get_client_returns_client():
    """get_client() debe retornar una instancia de supabase.Client sin lanzar excepción."""
    from supabase import Client
    result = get_client()
    assert isinstance(result, Client), (
        "get_client() debe retornar una instancia de supabase.Client"
    )


def test_get_client_fails_without_env(monkeypatch):
    """get_client() debe lanzar EnvironmentError si SUPABASE_URL no está definida.
    Se parchea load_dotenv para evitar que recargue el archivo .env durante el test.
    """
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    # Parchear load_dotenv para que no restaure la variable desde el archivo .env
    monkeypatch.setattr("src.supabase_client.load_dotenv", lambda *args, **kwargs: None)
    with pytest.raises(EnvironmentError):
        get_client()


def test_verify_connectivity_true(client):
    """verify_connectivity() debe retornar True con un cliente válido."""
    result = verify_connectivity(client)
    assert result is True, (
        "verify_connectivity() debe retornar True cuando la conexión es válida"
    )


# ── Tests de verificación de tablas usr_* ─────────────────────────────────────

def test_all_usr_tables_exist(client):
    """verify_all_usr_tables() debe retornar True para las 4 tablas usr_*."""
    result = verify_all_usr_tables(client)
    assert isinstance(result, dict), "El resultado debe ser un diccionario"
    for tabla in ["usr_ventas", "usr_inventario", "usr_productos", "usr_sedes"]:
        assert result.get(tabla) is True, (
            f"La tabla '{tabla}' debe existir en Supabase. "
            f"Resultado actual: {result}"
        )


# ── Tests de verificación de esquemas usr_* ───────────────────────────────────

def test_usr_ventas_schema_matches(client):
    """verify_table_schema() debe retornar match=True con 0 discrepancias para usr_ventas."""
    result = verify_table_schema(client, "usr_ventas", EXPECTED_USR_VENTAS)
    assert result["match"] is True, (
        f"usr_ventas: se esperaba match=True. "
        f"Faltantes: {result.get('missing')}, "
        f"Extra: {result.get('extra')}, "
        f"Tipo incorrecto: {result.get('type_mismatch')}"
    )
    assert result["missing"] == [], f"usr_ventas: columnas faltantes: {result['missing']}"
    assert result["extra"] == [], f"usr_ventas: columnas extra: {result['extra']}"


def test_usr_inventario_schema_matches(client):
    """verify_table_schema() debe retornar match=True con 0 discrepancias para usr_inventario."""
    result = verify_table_schema(client, "usr_inventario", EXPECTED_USR_INVENTARIO)
    assert result["match"] is True, (
        f"usr_inventario: se esperaba match=True. "
        f"Faltantes: {result.get('missing')}, "
        f"Extra: {result.get('extra')}, "
        f"Tipo incorrecto: {result.get('type_mismatch')}"
    )
    assert result["missing"] == [], f"usr_inventario: columnas faltantes: {result['missing']}"
    assert result["extra"] == [], f"usr_inventario: columnas extra: {result['extra']}"


def test_usr_productos_schema_matches(client):
    """verify_table_schema() debe retornar match=True con 0 discrepancias para usr_productos."""
    result = verify_table_schema(client, "usr_productos", EXPECTED_USR_PRODUCTOS)
    assert result["match"] is True, (
        f"usr_productos: se esperaba match=True. "
        f"Faltantes: {result.get('missing')}, "
        f"Extra: {result.get('extra')}, "
        f"Tipo incorrecto: {result.get('type_mismatch')}"
    )
    assert result["missing"] == [], f"usr_productos: columnas faltantes: {result['missing']}"
    assert result["extra"] == [], f"usr_productos: columnas extra: {result['extra']}"


def test_usr_sedes_schema_matches(client):
    """verify_table_schema() debe retornar match=True con 0 discrepancias para usr_sedes."""
    result = verify_table_schema(client, "usr_sedes", EXPECTED_USR_SEDES)
    assert result["match"] is True, (
        f"usr_sedes: se esperaba match=True. "
        f"Faltantes: {result.get('missing')}, "
        f"Extra: {result.get('extra')}, "
        f"Tipo incorrecto: {result.get('type_mismatch')}"
    )
    assert result["missing"] == [], f"usr_sedes: columnas faltantes: {result['missing']}"
    assert result["extra"] == [], f"usr_sedes: columnas extra: {result['extra']}"


# ── Tests de creación e idempotencia de tablas tss_* ─────────────────────────

def test_create_tss_tables_idempotent(client):
    """create_tss_tables() debe poder llamarse dos veces sin lanzar excepción (idempotencia)."""
    # Primera llamada: crea las tablas (o confirma que ya existen)
    create_tss_tables(client)
    # Segunda llamada: debe terminar sin error gracias a CREATE TABLE IF NOT EXISTS
    create_tss_tables(client)


# ── Tests CRUD en tablas tss_* ───────────────────────────────────────────────

def test_tss_error_log_crud(client):
    """INSERT y SELECT en tss_error_log deben funcionar sin error. Limpia el registro al final."""
    run_id = f"test-{uuid.uuid4()}"
    registro = {
        "error_code": "ERR_MTD_001",
        "error_message": "Test de integración — CRUD tss_error_log",
        "source_table": "usr_ventas",
        "source_record": {"test": True},
        "pipeline_run_id": run_id,
    }

    # INSERT
    insert_resp = client.table("tss_error_log").insert(registro).execute()
    assert insert_resp.data, "INSERT en tss_error_log no retornó datos"
    inserted_id = insert_resp.data[0]["id"]

    # SELECT
    select_resp = (
        client.table("tss_error_log")
        .select("*")
        .eq("id", inserted_id)
        .execute()
    )
    assert len(select_resp.data) == 1, "SELECT en tss_error_log no retornó el registro insertado"
    assert select_resp.data[0]["error_code"] == "ERR_MTD_001"

    # CLEANUP: eliminar el registro de prueba
    client.table("tss_error_log").delete().eq("id", inserted_id).execute()


def test_tss_pipeline_log_crud(client):
    """INSERT y SELECT en tss_pipeline_log deben funcionar. Verifica constraint de mode y status."""
    run_id = f"test-{uuid.uuid4()}"
    now_utc = datetime.now(timezone.utc).isoformat()
    registro = {
        "run_id": run_id,
        "mode": "validate",
        "status": "success",
        "records_processed": 10,
        "records_failed": 0,
        "started_at": now_utc,
    }

    # INSERT con valores válidos
    insert_resp = client.table("tss_pipeline_log").insert(registro).execute()
    assert insert_resp.data, "INSERT en tss_pipeline_log no retornó datos"
    inserted_id = insert_resp.data[0]["id"]

    # SELECT
    select_resp = (
        client.table("tss_pipeline_log")
        .select("*")
        .eq("id", inserted_id)
        .execute()
    )
    assert len(select_resp.data) == 1, "SELECT en tss_pipeline_log no retornó el registro insertado"
    assert select_resp.data[0]["mode"] == "validate"
    assert select_resp.data[0]["status"] == "success"

    # Verificar constraint de mode: INSERT con valor inválido debe fallar
    run_id_invalido = f"test-{uuid.uuid4()}"
    registro_invalido = {
        "run_id": run_id_invalido,
        "mode": "invalido",  # Valor no permitido por constraint
        "status": "success",
        "records_processed": 0,
        "records_failed": 0,
        "started_at": now_utc,
    }
    with pytest.raises(Exception):
        client.table("tss_pipeline_log").insert(registro_invalido).execute()

    # CLEANUP
    client.table("tss_pipeline_log").delete().eq("id", inserted_id).execute()


def test_tss_quarantine_crud(client):
    """INSERT y SELECT en tss_quarantine deben funcionar sin error. Limpia el registro al final."""
    run_id = f"test-{uuid.uuid4()}"
    registro = {
        "source_table": "usr_ventas",
        "source_record": {"id_venta": 99999, "test": True},
        "error_code": "ERR_MTD_004",
        "error_detail": "Test de integración — CRUD tss_quarantine",
        "pipeline_run_id": run_id,
    }

    # INSERT
    insert_resp = client.table("tss_quarantine").insert(registro).execute()
    assert insert_resp.data, "INSERT en tss_quarantine no retornó datos"
    inserted_id = insert_resp.data[0]["id"]

    # SELECT
    select_resp = (
        client.table("tss_quarantine")
        .select("*")
        .eq("id", inserted_id)
        .execute()
    )
    assert len(select_resp.data) == 1, "SELECT en tss_quarantine no retornó el registro insertado"
    assert select_resp.data[0]["error_code"] == "ERR_MTD_004"

    # CLEANUP
    client.table("tss_quarantine").delete().eq("id", inserted_id).execute()
