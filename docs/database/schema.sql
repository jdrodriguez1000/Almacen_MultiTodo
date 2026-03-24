-- =============================================================================
-- schema.sql — Dashboard MultiTodo
-- Fuente de verdad técnica del esquema de Supabase.
-- Actualizar este archivo inmediatamente después de cada CREATE TABLE,
-- ALTER TABLE o nuevo trigger en Supabase.
-- =============================================================================
-- Última sincronización: 2026-03-24 (Etapa 1.2 — Validación de Infraestructura)
-- Proyecto Supabase: Demo_Dashboard (ebqrvegxefahumxytgbj) | Región: us-east-1
-- Tablas incluidas: 4 usr_* (cliente) + 3 tss_* operativas (Triple S)
-- =============================================================================


-- ─── TABLAS DEL CLIENTE (usr_*) ───────────────────────────────────────────────
-- Propiedad: Almacén MultiTodo
-- Acceso Triple S: SOLO LECTURA
-- No alterar DDL sin CC aprobado.
-- Orden de creación respeta dependencias FK:
--   usr_sedes → usr_productos → usr_ventas → usr_inventario

-- SEDES: Maestro de puntos de venta. pais default 'Colombia'.
create table public.usr_sedes (
  id_sede        serial not null,
  pais           text   not null default 'Colombia'::text,
  ciudad         text   not null,
  nombre_sede    text   not null,
  created_at     timestamp with time zone not null default now(),
  updated_at     timestamp with time zone not null default now(),
  constraint usr_sedes_pkey primary key (id_sede)
);

-- PRODUCTOS: Maestro de SKUs con jerarquía familia > categoría > subcategoría
create table public.usr_productos (
  sku            text not null,
  nombre         text not null,
  familia        text not null,
  categoria      text not null,
  subcategoria   text not null,
  created_at     timestamp with time zone not null default now(),
  updated_at     timestamp with time zone not null default now(),
  constraint usr_productos_pkey primary key (sku)
);

-- VENTAS: 1 registro por transacción de venta
-- fecha_hora almacenada en UTC. Ventana válida: 13:00–23:00 UTC (8AM–6PM COT)
create table public.usr_ventas (
  id_venta       bigserial                    not null,
  fecha_hora     timestamp with time zone     not null,
  sku            text                         not null,
  id_sede        integer                      not null,
  cantidad       integer                      not null,
  precio         numeric(10, 2)               not null,
  costo          numeric(10, 2)               null,
  created_at     timestamp with time zone     not null default now(),
  updated_at     timestamp with time zone     not null default now(),
  constraint usr_ventas_pkey              primary key (id_venta),
  constraint usr_ventas_id_sede_fkey      foreign key (id_sede) references usr_sedes (id_sede),
  constraint usr_ventas_sku_fkey          foreign key (sku)     references usr_productos (sku),
  constraint usr_ventas_cantidad_check    check (cantidad > 0),
  constraint usr_ventas_precio_check      check (precio > 0),
  constraint usr_ventas_costo_check       check (costo > 0)
);

-- INVENTARIO: 1 registro por SKU/sede. Se sobreescribe en cada actualización diaria.
create table public.usr_inventario (
  sku                 text              not null,
  id_sede             integer           not null,
  stock_fisico        integer           not null default 0,
  costo_reposicion    numeric(10, 2)    null,
  created_at          timestamp with time zone not null default now(),
  updated_at          timestamp with time zone not null default now(),
  constraint usr_inventario_pkey                    primary key (sku, id_sede),
  constraint usr_inventario_id_sede_fkey            foreign key (id_sede) references usr_sedes (id_sede),
  constraint usr_inventario_sku_fkey                foreign key (sku)     references usr_productos (sku),
  constraint usr_inventario_stock_fisico_check      check (stock_fisico >= 0),
  constraint usr_inventario_costo_reposicion_check  check (costo_reposicion > 0)
);


-- ─── TABLAS OPERATIVAS DE TRIPLE S (tss_*) ────────────────────────────────────
-- Propiedad: Sabbia Solutions & Services (Triple S)
-- Acceso: Lectura/Escritura exclusiva del pipeline
-- Creadas en Etapa 1.2. Idempotentes: CREATE TABLE IF NOT EXISTS.
-- No crear tss_bronze_*, tss_silver_*, tss_gold_* hasta Fase 2.
-- No crear tss_alerts hasta Etapa 3.2.

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
