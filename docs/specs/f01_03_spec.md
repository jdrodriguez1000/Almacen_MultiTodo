# SPEC — Data Contract (`f01_03`)

> **Trazabilidad:** Este documento implementa los requerimientos definidos en `docs/reqs/f01_03_prd.md`.

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Cliente:** Almacén MultiTodo
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.3
**Versión:** 2.0
**Fecha:** 2026-03-24
**Estado:** ✅ Aprobado
**Documentos relacionados:** `docs/reqs/f01_03_prd.md` | `docs/plans/f01_03_plan.md` | `docs/tasks/f01_03_task.md` | `docs/database/schema.sql`

---

## 1. Arquitectura Lógica

Esta SPEC especifica los **contratos de interfaz** del Data Contract. No especifica la implementación del pipeline de validación — eso es Etapa 2.1. Define qué debe cumplir esa implementación.

### Componentes de arquitectura

| ID | Componente | Responsabilidad |
|---|---|---|
| `[ARC-01]` | Tablas `usr_*` (Supabase) | Fuente de datos del cliente. Solo lectura para el pipeline. |
| `[ARC-02]` | Puerta de entrada — Validaciones (`modo: validate`) | Aplica las 5 restricciones del contrato antes de Bronze. |
| `[ARC-03]` | `tss_error_log` | Registro persistente de cada violación detectada. |
| `[ARC-04]` | `tss_quarantine` | Almacén de registros rechazados. Pendientes hasta corrección del cliente. |
| `[ARC-05]` | `tss_pipeline_log` | Canal 3 de la Triple Persistencia de Estado — historial de ejecuciones. |
| `[ARC-06]` | `pipeline/src/validators/` | Módulos Python que implementan los contratos de validación especificados aquí. |
| `[ARC-07]` | `pipeline/config.yaml` — sección `data_contract` | Parámetros del contrato leídos en tiempo de ejecución. Sin hardcoding. |

### Flujo de datos

```
Cliente (Almacén MultiTodo)
        │
        │  carga datos antes de 05:30 UTC
        ▼
┌───────────────────────────────────────┐
│  [ARC-01] Tablas usr_* en Supabase    │
│  usr_sedes, usr_productos             │
│  usr_ventas, usr_inventario           │
└───────────────────────────────────────┘
        │
        │  Pipeline Triple S inicia 08:30 UTC
        ▼
┌───────────────────────────────────────┐
│  [ARC-02] PUERTA DE ENTRADA           │
│  Validaciones (modo: validate)        │
│                                       │
│  1. Maestros completos                │
│     sku ∈ usr_productos               │
│     id_sede ∈ usr_sedes               │
│                                       │
│  2. Ventana operativa                 │
│     fecha_hora: 13:00–22:59 UTC       │
│                                       │
│  3. Anti-T+0                          │
│     fecha_hora.date < hoy UTC         │
│                                       │
│  4. Restricciones numéricas           │
│     precio > 0, cantidad > 0, etc.    │
└───────────────────────────────────────┘
        │
        ├─── INVÁLIDO ──────────────────────────────────────┐
        │                                                    │
        │                                          [ARC-03] tss_error_log
        │                                          [ARC-04] tss_quarantine
        │                                          Notificación al cliente
        │
        ▼
┌───────────────────────────────────────┐
│  VÁLIDO — Pasa a Bronze               │
│  (Etapa 2.2 — ETL Bronze → Silver)    │
└───────────────────────────────────────┘
        │
        └──────────── [ARC-05] tss_pipeline_log (siempre, éxito o fallo)
```

---

## 2. Especificaciones de Ingeniería de Datos

### 2.1 Esquemas de Tablas (Supabase)

#### `[ARC-01]` — `usr_sedes` (maestro de sedes)

**Propietario:** Almacén MultiTodo | **Acceso Triple S:** Solo lectura | **Frecuencia:** Cuando haya cambios en la red de sedes

| Columna | Tipo | Constraint | Descripción |
|---|---|---|---|
| `id_sede` | `serial` | PK, NOT NULL, autogenerado | Identificador único. No modificar manualmente. |
| `pais` | `text` | NOT NULL, DEFAULT `'Colombia'` | País de la sede. Valor esperado siempre `'Colombia'`. |
| `ciudad` | `text` | NOT NULL, NOT EMPTY | Ciudad donde opera la sede. |
| `nombre_sede` | `text` | NOT NULL, NOT EMPTY | Nombre del punto de venta. |
| `created_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Timestamp de creación. No modificar. |
| `updated_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Timestamp de última modificación. |

**Reglas de validación:** Esta tabla es origen de `ERR_MTD_003`. Su validez se mide por completitud del catálogo.

**Registro válido:**
```json
{ "id_sede": 1, "pais": "Colombia", "ciudad": "Bogota", "nombre_sede": "MultiTodo Centro" }
```

**Registro inválido** (violación NOT EMPTY en `ciudad`):
```json
{ "id_sede": 8, "pais": "Colombia", "ciudad": "", "nombre_sede": "Sede Nueva" }
```

---

#### `[ARC-01]` — `usr_productos` (maestro de SKUs)

**Propietario:** Almacén MultiTodo | **Acceso Triple S:** Solo lectura | **Frecuencia:** Cuando haya altas, bajas o modificaciones en el catálogo

| Columna | Tipo | Constraint | Descripción |
|---|---|---|---|
| `sku` | `text` | PK, NOT NULL, UNIQUE | Identificador único del producto. No reutilizar SKUs descontinuados. |
| `nombre` | `text` | NOT NULL, NOT EMPTY | Nombre comercial del producto. |
| `familia` | `text` | NOT NULL, NOT EMPTY | Nivel 1 de la jerarquía del catálogo. |
| `categoria` | `text` | NOT NULL, NOT EMPTY | Nivel 2 de la jerarquía. |
| `subcategoria` | `text` | NOT NULL, NOT EMPTY | Nivel 3 de la jerarquía (más específico). |
| `created_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Timestamp de creación. |
| `updated_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Timestamp de modificación. |

**Reglas de validación:** Esta tabla es origen de `ERR_MTD_002`.

**Registro válido:**
```json
{ "sku": "LAV-001", "nombre": "Jabón en barra x3", "familia": "Aseo", "categoria": "Cuidado Personal", "subcategoria": "Higiene Corporal" }
```

**Registro inválido** (violación NOT EMPTY en `familia`):
```json
{ "sku": "LAV-001", "nombre": "Jabón en barra x3", "familia": "", "categoria": "Cuidado Personal", "subcategoria": "Higiene Corporal" }
```

---

#### `[ARC-01]` — `usr_ventas` (transacciones de venta)

**Propietario:** Almacén MultiTodo | **Acceso Triple S:** Solo lectura | **Frecuencia:** Diaria — datos completos del día anterior (T-1), antes de las 05:30 UTC

| Columna | Tipo | Constraint | Descripción |
|---|---|---|---|
| `id_venta` | `bigserial` | PK, NOT NULL, autogenerado | Identificador único. No modificar. |
| `fecha_hora` | `timestamp with time zone` | NOT NULL | UTC. Ventana válida: `hora_utc ∈ [13, 22]`. No T+0. |
| `sku` | `text` | NOT NULL, FK → `usr_productos.sku` | Producto vendido. Debe existir en el maestro. |
| `id_sede` | `integer` | NOT NULL, FK → `usr_sedes.id_sede` | Sede donde ocurrió la venta. Debe existir en el maestro. |
| `cantidad` | `integer` | NOT NULL, `> 0` | Unidades vendidas. No cero ni negativo. |
| `precio` | `numeric(10,2)` | NOT NULL, `> 0` | Precio unitario COP. |
| `costo` | `numeric(10,2)` | NULLABLE, `> 0` si se informa | Costo unitario COP. Opcional. |
| `created_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Timestamp de inserción. |
| `updated_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Timestamp de modificación. |

**Códigos de error aplicables:**

| Código | Condición de activación |
|---|---|
| `ERR_MTD_001` | `fecha_hora` fuera de ventana 13:00–22:59 UTC |
| `ERR_MTD_002` | `sku` no existe en `usr_productos` |
| `ERR_MTD_003` | `id_sede` no existe en `usr_sedes` |
| `ERR_MTD_004` | `fecha_hora.date == hoy_utc` (dato T+0) |
| `ERR_MTD_005` | `cantidad ≤ 0`, `precio ≤ 0`, o `costo ≤ 0` cuando no es nulo |

**Registro válido:**
```json
{ "fecha_hora": "2026-03-23T16:30:00+00:00", "sku": "LAV-001", "id_sede": 3, "cantidad": 2, "precio": 4500.00, "costo": 3100.00 }
```
*Interpretación: 23-mar-2026 a las 11:30 AM COT (16:30 UTC — dentro de ventana).*

**Registro inválido — `ERR_MTD_001`:**
```json
{ "fecha_hora": "2026-03-23T11:00:00+00:00", "sku": "LAV-001", "id_sede": 3, "cantidad": 1, "precio": 4500.00 }
```
*Motivo: 11:00 UTC = 6:00 AM COT — el almacén no había abierto.*

**Registro inválido — `ERR_MTD_004`:**
```json
{ "fecha_hora": "2026-03-24T15:00:00+00:00", "sku": "LAV-001", "id_sede": 3, "cantidad": 5, "precio": 4500.00 }
```
*Motivo: `fecha_hora` es del día en curso. Dato T+0.*

**Registro inválido — `ERR_MTD_005`:**
```json
{ "fecha_hora": "2026-03-23T18:00:00+00:00", "sku": "LAV-001", "id_sede": 3, "cantidad": 0, "precio": 4500.00 }
```
*Motivo: `cantidad = 0` viola `cantidad > 0`.*

---

#### `[ARC-01]` — `usr_inventario` (stock por SKU/sede)

**Propietario:** Almacén MultiTodo | **Acceso Triple S:** Solo lectura | **Frecuencia:** Diaria — estado al cierre de T-1. Modelo de sobreescritura (upsert).

| Columna | Tipo | Constraint | Descripción |
|---|---|---|---|
| `sku` | `text` | PK compuesta, NOT NULL, FK → `usr_productos.sku` | SKU del producto. Debe existir en el maestro. |
| `id_sede` | `integer` | PK compuesta, NOT NULL, FK → `usr_sedes.id_sede` | Sede. Debe existir en el maestro. |
| `stock_fisico` | `integer` | NOT NULL, `>= 0` | Unidades disponibles al cierre. Puede ser 0. |
| `costo_reposicion` | `numeric(10,2)` | NULLABLE, `> 0` si se informa | Costo de reponer 1 unidad COP. Opcional. |
| `created_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Timestamp de creación. |
| `updated_at` | `timestamp with time zone` | NOT NULL, DEFAULT `now()` | Debe actualizarse en cada carga diaria. |

**Códigos de error aplicables:** `ERR_MTD_002`, `ERR_MTD_003`, `ERR_MTD_005`.

**Registro válido:**
```json
{ "sku": "LAV-001", "id_sede": 3, "stock_fisico": 45, "costo_reposicion": 3100.00 }
```

**Registro inválido — `ERR_MTD_005`** (`stock_fisico < 0`):
```json
{ "sku": "LAV-001", "id_sede": 3, "stock_fisico": -5 }
```

**Registro inválido — `ERR_MTD_002`** (SKU no registrado):
```json
{ "sku": "XXX-999", "id_sede": 3, "stock_fisico": 10 }
```

---

### 2.2 Esquemas Pandera (Validación)

Los esquemas Pandera son la representación Python del contrato de datos. Se implementan en Etapa 2.1 en `[ARC-06]` (`pipeline/src/validators/`). Esta sección es la especificación que esa implementación debe satisfacer.

> **Nota:** El pseudocódigo siguiente es especificación de contrato, no código ejecutable. El desarrollador debe traducirlo a `pandera.DataFrameSchema` real en Etapa 2.1.

#### Schema `usr_ventas`

```python
# ESPECIFICACIÓN — Archivo destino: pipeline/src/validators/schema_ventas.py

VentasSchema = DataFrameSchema(
    columns={
        "id_venta":   Column(pa.Int64,   nullable=False, unique=True, checks=[Check.gt(0)]),
        "fecha_hora": Column(pa.DateTime, nullable=False, checks=[
            # ERR_MTD_001: hora UTC entre 13 y 22 (inclusivo)
            Check(lambda s: s.dt.hour.between(13, 22), error="ERR_MTD_001"),
            # ERR_MTD_004: no puede ser del día actual UTC
            Check(lambda s: s.dt.date < datetime.now(pytz.utc).date(), error="ERR_MTD_004"),
        ]),
        "sku":        Column(pa.String,  nullable=False, checks=[Check(lambda s: s.str.len() > 0)]),
        "id_sede":    Column(pa.Int64,   nullable=False, checks=[Check.gt(0)]),
        "cantidad":   Column(pa.Int64,   nullable=False, checks=[Check.gt(0,  error="ERR_MTD_005")]),
        "precio":     Column(pa.Float64, nullable=False, checks=[Check.gt(0.0, error="ERR_MTD_005")]),
        "costo":      Column(pa.Float64, nullable=True,  checks=[
            Check(lambda s: s.dropna().gt(0).all(), error="ERR_MTD_005"),
        ]),
    },
    coerce=False,
    strict=False,   # Permitir columnas extra (created_at, updated_at)
    name="usr_ventas"
)
```

**Checks de referencia cruzada** — `ERR_MTD_002` y `ERR_MTD_003` requieren consultar otras tablas. No pueden expresarse en el schema Pandera. Se implementan en `cross_validators.py`:

```python
# ESPECIFICACIÓN — Archivo destino: pipeline/src/validators/cross_validators.py

def validate_skus_exist(df, productos_skus: set) -> pd.Series:
    """True si sku ∈ usr_productos. False → ERR_MTD_002."""
    return df["sku"].isin(productos_skus)

def validate_sedes_exist(df, sedes_ids: set) -> pd.Series:
    """True si id_sede ∈ usr_sedes. False → ERR_MTD_003."""
    return df["id_sede"].isin(sedes_ids)
```

#### Schema `usr_inventario`

```python
# ESPECIFICACIÓN — Archivo destino: pipeline/src/validators/schema_inventario.py

InventarioSchema = DataFrameSchema(
    columns={
        "sku":              Column(pa.String,  nullable=False, checks=[Check(lambda s: s.str.len() > 0)]),
        "id_sede":          Column(pa.Int64,   nullable=False, checks=[Check.gt(0)]),
        "stock_fisico":     Column(pa.Int64,   nullable=False, checks=[Check.gte(0, error="ERR_MTD_005")]),
        "costo_reposicion": Column(pa.Float64, nullable=True,  checks=[
            Check(lambda s: s.dropna().gt(0).all(), error="ERR_MTD_005"),
        ]),
    },
    coerce=False,
    strict=False,
    name="usr_inventario"
)
```

#### Validación de maestros no vacíos

Las tablas maestras no se validan con Pandera durante la ingesta diaria — son fuente de referencia. El pipeline verifica que no estén vacías antes de procesar ventas e inventario:

```python
# ESPECIFICACIÓN — Archivo destino: pipeline/src/validators/master_validators.py

def validate_masters_not_empty(productos_df, sedes_df) -> dict:
    """
    Verifica que los maestros tengan al menos un registro.
    Si alguno está vacío, el pipeline aborta antes de procesar ventas/inventario.
    """
    return {
        "productos_ok": len(productos_df) > 0,
        "sedes_ok":     len(sedes_df) > 0
    }
```

---

## 3. Diseño del Módulo / Función

| Función / Clase | Módulo (`src/validators/`) | Input | Output | REQ que implementa |
|---|---|---|---|---|
| `VentasSchema` | `schema_ventas.py` | DataFrame `usr_ventas` | DataFrame válido / excepción Pandera | `[REQ-03]` |
| `InventarioSchema` | `schema_inventario.py` | DataFrame `usr_inventario` | DataFrame válido / excepción Pandera | `[REQ-03]` |
| `validate_skus_exist()` | `cross_validators.py` | DataFrame + `set` de SKUs válidos | `pd.Series[bool]` | `[REQ-03]` — `ERR_MTD_002` |
| `validate_sedes_exist()` | `cross_validators.py` | DataFrame + `set` de IDs válidos | `pd.Series[bool]` | `[REQ-03]` — `ERR_MTD_003` |
| `validate_masters_not_empty()` | `master_validators.py` | DataFrames productos y sedes | `dict` con flags bool | `[REQ-01]` |
| `utc_to_cot()` | `temporal_validators.py` | `datetime` UTC | `datetime` COT | `[REQ-03]`, `[REQ-06]` |
| `is_within_operating_hours()` | `temporal_validators.py` | `datetime` UTC | `bool` | `[REQ-03]` — `ERR_MTD_001` |
| `is_not_current_day()` | `temporal_validators.py` | `datetime` UTC | `bool` | `[REQ-06]` — `ERR_MTD_004` |
| `ERR_MTD_XXX` constantes + plantillas | `error_catalog.py` | — | `str` con mensaje renderizado | `[REQ-03]`, `[REQ-04]` |
| Escritura en `tss_error_log` | `rejection_handler.py` | Registro inválido + código error | Registro en Supabase | `[REQ-04]` |
| Escritura en `tss_quarantine` | `rejection_handler.py` | Registro inválido + código error | Registro en Supabase | `[REQ-04]` |
| Reporte de notificación al cliente | `report_generator.py` | Resumen del pipeline_run | Texto estructurado | `[REQ-04]`, `[REQ-05]` |

### Restricciones temporales — especificación de funciones

**Librería obligatoria:** `pytz` (`America/Bogota`). Prohibido usar offsets manuales como `-timedelta(hours=5)`.

```python
# ESPECIFICACIÓN — pipeline/src/validators/temporal_validators.py

import pytz
from datetime import datetime

BOGOTA_TZ = pytz.timezone('America/Bogota')
UTC_TZ    = pytz.utc

VENTANA_APERTURA_UTC = 13   # 8:00 AM COT = 13:00 UTC
VENTANA_CIERRE_UTC   = 22   # 5:59 PM COT = 22:59 UTC (23:00 UTC = 6:00 PM = fuera)

def utc_to_cot(utc_ts: datetime) -> datetime:
    if utc_ts.tzinfo is None:
        utc_ts = UTC_TZ.localize(utc_ts)
    return utc_ts.astimezone(BOGOTA_TZ)

def is_within_operating_hours(utc_ts: datetime) -> bool:
    """True si hora_utc ∈ [13, 22]. False → ERR_MTD_001."""
    return VENTANA_APERTURA_UTC <= utc_ts.hour <= VENTANA_CIERRE_UTC

def is_not_current_day(utc_ts: datetime) -> bool:
    """True si fecha_utc < hoy_utc. False → ERR_MTD_004."""
    hoy_utc = datetime.now(UTC_TZ).date()
    fecha   = utc_ts.date() if utc_ts.tzinfo else UTC_TZ.localize(utc_ts).date()
    return fecha < hoy_utc
```

**Tabla de conversiones de referencia:**

| Timestamp UTC | Hora COT | Válido |
|---|---|---|
| `2026-03-23T13:00:00+00:00` | 08:00 COT | ✅ (apertura exacta) |
| `2026-03-23T16:30:00+00:00` | 11:30 COT | ✅ |
| `2026-03-23T22:59:00+00:00` | 17:59 COT | ✅ (un minuto antes del cierre) |
| `2026-03-23T23:00:00+00:00` | 18:00 COT | ❌ `ERR_MTD_001` (cierre exacto, no inclusivo) |
| `2026-03-23T11:00:00+00:00` | 06:00 COT | ❌ `ERR_MTD_001` (antes de apertura) |
| `2026-03-24T15:00:00+00:00` | 10:00 COT (hoy) | ❌ `ERR_MTD_004` (T+0) |

---

## 4. Contratos de Datos entre Capas

| Capa Origen | Capa Destino | Formato | Validación |
|---|---|---|---|
| `[ARC-01]` `usr_*` (cliente) | `[ARC-02]` Puerta de entrada | DataFrame pandas | Schemas Pandera + cross-validators + temporal-validators |
| `[ARC-02]` Registros válidos | Bronze `tss_bronze_*` (Etapa 2.2) | DataFrame pandas | Pandera aprobado — pasa limpio |
| `[ARC-02]` Registros inválidos | `[ARC-03]` `tss_error_log` + `[ARC-04]` `tss_quarantine` | Registro jsonb + código `ERR_MTD_XXX` | Estructura definida en secciones 4.1 y 4.2 |

### 4.1 Estructura del registro en `tss_error_log`

| Campo | Tipo | Valor esperado |
|---|---|---|
| `error_code` | `text` | `'ERR_MTD_001'` a `'ERR_MTD_005'` |
| `error_message` | `text` | Plantilla del catálogo renderizada (ver §4.4) |
| `source_table` | `text` | `'usr_ventas'` o `'usr_inventario'` |
| `source_record` | `jsonb` | Registro raw completo que causó el error |
| `pipeline_run_id` | `text` | UUID de la ejecución — FK lógica a `tss_pipeline_log.run_id` |

**Ejemplo:**
```json
{
  "error_code": "ERR_MTD_001",
  "error_message": "Transacción fuera de horario operativo: id_venta=10246, fecha_hora=2026-03-23T11:00:00+00:00 (6:00 AM COT). El almacén opera de 8:00 AM a 6:00 PM COT.",
  "source_table": "usr_ventas",
  "source_record": { "id_venta": 10246, "fecha_hora": "2026-03-23T11:00:00+00:00", "sku": "LAV-001", "id_sede": 3, "cantidad": 1, "precio": 4500.00 },
  "pipeline_run_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 4.2 Estructura del registro en `tss_quarantine`

| Campo | Tipo | Valor esperado |
|---|---|---|
| `source_table` | `text` | `'usr_ventas'` o `'usr_inventario'` |
| `source_record` | `jsonb` | Registro raw completo sin modificación |
| `error_code` | `text` | `'ERR_MTD_001'` a `'ERR_MTD_005'` |
| `error_detail` | `text` | Campo afectado, valor recibido, valor esperado |
| `pipeline_run_id` | `text` | UUID de la ejecución que rechazó el registro |
| `resolved_at` | `timestamp with time zone` | `NULL` hasta que el cliente corrija y reentregue |

**Ejemplo:**
```json
{
  "source_table": "usr_ventas",
  "source_record": { "id_venta": 10246, "fecha_hora": "2026-03-23T11:00:00+00:00", "sku": "LAV-001", "id_sede": 3, "cantidad": 1, "precio": 4500.00 },
  "error_code": "ERR_MTD_001",
  "error_detail": "Campo 'fecha_hora': hora UTC=11, fuera de ventana válida [13, 22].",
  "pipeline_run_id": "550e8400-e29b-41d4-a716-446655440000",
  "resolved_at": null
}
```

### 4.3 Condiciones de bloqueo al paso a Bronze

| Condición | Comportamiento | Justificación |
|---|---|---|
| ≥ 1 registro con `ERR_MTD_004` | Bloqueo total del lote de ventas | Datos T+0 contaminan jornadas incompletas |
| ≥ 1 registro con `ERR_MTD_001`, `002`, `003`, `005` | Solo ese registro va a cuarentena. Los demás avanzan. | Registros independientes — un error no invalida el lote |
| > 50% del lote rechazado (cualquier código) | `status = 'failure'` en `tss_pipeline_log` + alerta alta prioridad | Salvaguarda ante errores sistémicos en la fuente |
| `usr_ventas` sin nuevos registros | `status = 'partial'` + alerta interna | Posible fallo en la carga del cliente |

### 4.4 Catálogo de mensajes de error

| Código | Plantilla del mensaje | Variables |
|---|---|---|
| `ERR_MTD_001` | `"Transacción fuera de horario operativo: id_venta={id_venta}, fecha_hora={fecha_hora} ({hora_cot} hora Colombia). Horario: 8:00 AM–6:00 PM COT. Verifique que el timestamp esté en UTC."` | `id_venta`, `fecha_hora`, `hora_cot` |
| `ERR_MTD_002` | `"Producto no registrado: SKU '{sku}' no existe en usr_productos. Regístrelo antes de cargar ventas o inventario que lo referencien."` | `sku` |
| `ERR_MTD_003` | `"Sede no registrada: id_sede={id_sede} no existe en usr_sedes. Regístrela antes de cargar transacciones que la referencien."` | `id_sede` |
| `ERR_MTD_004` | `"Dato del día en curso rechazado: id_venta={id_venta}, fecha_hora={fecha_hora} ({fecha_hoy_cot} COT). Solo se procesan jornadas cerradas. Este registro estará disponible mañana."` | `id_venta`, `fecha_hora`, `fecha_hoy_cot` |
| `ERR_MTD_005` | `"Valor numérico inválido en {tabla}: campo '{campo}' = {valor}. Restricción: {restriccion}. Verifique la integridad de los datos en la fuente."` | `tabla`, `campo`, `valor`, `restriccion` |

### 4.5 Protocolo de notificación al cliente

Reporte generado al finalizar el modo `validate` cuando hay rechazos:

```
REPORTE DE VALIDACIÓN — Dashboard MultiTodo
Fecha de procesamiento: {fecha_ejecucion_cot} (hora Colombia)
Período de datos procesados: {fecha_datos_cot} (T-1)
Identificador de ejecución: {pipeline_run_id}

RESUMEN:
  - Registros procesados usr_ventas:     {n_ventas_total}
  - Registros válidos usr_ventas:        {n_ventas_ok}
  - Registros rechazados usr_ventas:     {n_ventas_rechazados}
  - Registros procesados usr_inventario: {n_inv_total}
  - Registros válidos usr_inventario:    {n_inv_ok}
  - Registros rechazados usr_inventario: {n_inv_rechazados}

ERRORES DETECTADOS:
  {lista_de_errores_agrupados_por_codigo}

ACCIÓN REQUERIDA:
  Los registros rechazados están en cuarentena y NO aparecerán en el dashboard.
  1. Revise los registros indicados en su sistema fuente.
  2. Corrija el problema según la descripción del error.
  3. Actualice los datos en las tablas usr_* de Supabase.
  4. Notifique a Triple S para reprocesar los datos.
```

---

## 5. Configuración (`config.yaml`)

Sección a agregar en `pipeline/config.yaml` (ver `[ARC-07]`). Ningún valor del Data Contract puede estar hardcodeado en el código.

```yaml
# ─── DATA CONTRACT ──────────────────────────────────────────────────────────
# Parámetros del contrato de datos cliente–Triple S.
# Definidos en docs/specs/f01_03_spec.md.
# No modificar sin Control de Cambios aprobado.

data_contract:

  client_tables:
    ventas:     "usr_ventas"
    inventario: "usr_inventario"
    productos:  "usr_productos"
    sedes:      "usr_sedes"

  tss_tables:
    error_log:    "tss_error_log"
    quarantine:   "tss_quarantine"
    pipeline_log: "tss_pipeline_log"

  error_codes:
    ventana_operativa:     "ERR_MTD_001"
    sku_no_registrado:     "ERR_MTD_002"
    sede_no_registrada:    "ERR_MTD_003"
    dato_dia_actual:       "ERR_MTD_004"
    valor_numerico_invalido: "ERR_MTD_005"

  # Ventana operativa en horas UTC (inclusivo en ambos extremos)
  # Equivale a 8:00 AM – 5:59 PM COT
  operating_hours_utc:
    open:  13   # 8:00 AM COT
    close: 22   # 5:59 PM COT (23 UTC = 6:00 PM exacto = fuera de ventana)

  timezone: "America/Bogota"

  # Ventana de entrega del cliente
  delivery_deadline_utc: "05:30"   # 00:30 COT

  # Inicio del pipeline Triple S
  pipeline_start_utc: "08:30"      # 03:30 COT

  # Umbral de fallo total (% de registros rechazados → status='failure')
  failure_threshold_pct: 50

  # Comportamiento por código de error
  error_behavior:
    ERR_MTD_001: "quarantine_record"
    ERR_MTD_002: "quarantine_record"
    ERR_MTD_003: "quarantine_record"
    ERR_MTD_004: "block_batch"
    ERR_MTD_005: "quarantine_record"
```

---

## 6. Matriz de Diseño vs PRD

| REQ | Componente que lo implementa | Archivo (`src/validators/`) | Notas |
|---|---|---|---|
| `[REQ-01]` | Esquemas campo a campo §2.1 + `master_validators.py` | `master_validators.py` | Garantiza que maestros están completos antes de validar transacciones |
| `[REQ-02]` | `delivery_deadline_utc` en `config.yaml` | `config.yaml` | La ventana de entrega es configuración, no lógica de código |
| `[REQ-03]` — `ERR_MTD_001` | `is_within_operating_hours()` | `temporal_validators.py` | Ventana `[13, 22]` UTC leída desde `config.yaml` |
| `[REQ-03]` — `ERR_MTD_002` | `validate_skus_exist()` | `cross_validators.py` | Requires set de SKUs precargado desde Supabase |
| `[REQ-03]` — `ERR_MTD_003` | `validate_sedes_exist()` | `cross_validators.py` | Requires set de IDs precargado desde Supabase |
| `[REQ-03]` — `ERR_MTD_004` | `is_not_current_day()` | `temporal_validators.py` | Compara fecha UTC del registro vs `datetime.now(UTC)` |
| `[REQ-03]` — `ERR_MTD_005` | `VentasSchema`, `InventarioSchema` | `schema_ventas.py`, `schema_inventario.py` | Checks `gt(0)` y `gte(0)` en Pandera |
| `[REQ-04]` | Escritura en `tss_error_log` + `tss_quarantine` | `rejection_handler.py` | Un error → 1 registro en error_log + 1 en quarantine |
| `[REQ-04]` | Condiciones de bloqueo §4.3 | Orquestador `pipelines/validate_pipeline.py` | Solo `ERR_MTD_004` bloquea el lote completo |
| `[REQ-04]` | Reporte de notificación §4.5 | `report_generator.py` | Se genera al finalizar el modo `validate` |
| `[REQ-05]` | Catálogo de mensajes §4.4 | `error_catalog.py` | Mensajes comprensibles para el cliente, sin jerga interna |
| `[REQ-06]` | `is_not_current_day()` + `ERR_MTD_004` en `block_batch` | `temporal_validators.py` + config | Bloqueo total del lote si hay datos T+0 |
| `[REQ-07]` | `validate_sedes_exist()` + `usr_sedes` como maestro | `cross_validators.py` | 7 sedes activas registradas en `usr_sedes` |

### Criterios de verificación técnica

| ID | Criterio | Cómo verificar | REQ |
|---|---|---|---|
| `[CVT-01]` | `schema_ventas.py` rechaza `fecha_hora` fuera de 13:00–22:59 UTC | Test unitario con hora=12 UTC (falla) y hora=13 UTC (pasa) | `[REQ-03]` |
| `[CVT-02]` | `schema_ventas.py` rechaza `fecha_hora` del día en curso | Test con `datetime.now(UTC)` (falla) | `[REQ-06]` |
| `[CVT-03]` | `cross_validators.py` genera `ERR_MTD_002` para SKUs inexistentes | Test con `'SKU_INEXISTENTE_TEST'` | `[REQ-03]` |
| `[CVT-04]` | `cross_validators.py` genera `ERR_MTD_003` para `id_sede=9999` | Test con sede inexistente | `[REQ-03]` |
| `[CVT-05]` | `schema_ventas.py` rechaza `cantidad=0` y `cantidad=-1` | Tests unitarios ambos casos | `[REQ-03]` |
| `[CVT-06]` | `schema_ventas.py` rechaza `precio=0` | Test unitario | `[REQ-03]` |
| `[CVT-07]` | `schema_inventario.py` rechaza `stock_fisico=-1` | Test unitario | `[REQ-03]` |
| `[CVT-08]` | `ERR_MTD_004` bloquea el lote completo (registros T-1 también) | Test con lote mixto T+0 y T-1: ninguno pasa | `[REQ-06]` |
| `[CVT-09]` | `ERR_MTD_001/002/003/005` aplican cuarentena por registro | Test con lote mixto: válidos pasan, inválidos van a cuarentena | `[REQ-04]` |
| `[CVT-10]` | Cada rechazo genera exactamente 1 registro en `tss_error_log` | Verificar estructura en Supabase | `[REQ-04]` |
| `[CVT-11]` | Cada rechazo genera exactamente 1 registro en `tss_quarantine` con `resolved_at=NULL` | Verificar en Supabase | `[REQ-04]` |
| `[CVT-12]` | La conversión UTC→COT usa `pytz.timezone('America/Bogota')`, no offsets manuales | Grep por `timedelta(hours` en `src/` — no debe existir | `[REQ-03]` |
| `[CVT-13]` | El reporte de notificación se genera al finalizar el modo `validate` con rechazos | Ejecutar pipeline en modo validate con datos inválidos | `[REQ-04]` |
| `[CVT-14]` | Si >50% de registros son rechazados → `tss_pipeline_log.status = 'failure'` | Test con lote donde 60% tiene errores | `[REQ-03]` |
| `[CVT-15]` | El pipeline lee `operating_hours_utc` desde `config.yaml`, no hardcodeado | Cambiar `open: 13` a `open: 14` en config y verificar que el comportamiento cambia | `[REQ-03]` |

---

*Documento generado con `/sdd-doc` (Modo B — Tech Lead). Para plan de ejecución, ver `docs/plans/f01_03_plan.md`.*
