# SPEC — Constitución del Proyecto (`f01_01`)

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Fase:** 1 — Gobernanza y Cimientos | **Etapa:** 1.1
**Estado:** ✅ Aprobado
**Fecha:** 2026-03-23

> Trazabilidad: Este documento implementa los requerimientos definidos en `docs/reqs/f01_01_prd.md`.

---

## 1. Arquitectura Lógica

Esta etapa no produce flujos de datos — produce la **estructura física del repositorio** y los **artefactos de gobernanza** que sostienen todo el proyecto.

```
Almacen_MuliTodo/                          ← Raíz del repositorio
│
├── CLAUDE.md                              ← [ARC-01] Constitución global
├── PROJECT_index.md                       ← [ARC-02] Mapa macro del proyecto
├── PROJECT_handoff.md                     ← [ARC-03] Bitácora de sesión
├── .gitignore                             ← [ARC-04] Control de versiones
│
├── .claude/
│   └── skills/                            ← [ARC-05] Skills de gobernanza del agente
│       ├── update-index/SKILL.md
│       ├── session-close/SKILL.md
│       ├── sdd-doc/SKILL.md
│       ├── close-stage/SKILL.md
│       └── change-control/SKILL.md
│
├── pipeline/                              ← [ARC-06] Motor de datos (Python)
│   ├── main.py                            ← Stub: gateway de modos (validate/etl/alerts)
│   ├── config.yaml                        ← Configuración global sin secretos
│   ├── pipelines/                         ← Orquestadores (vacío, Fase 2)
│   ├── src/                               ← Lógica atómica (vacío, Fase 2)
│   └── tests/                             ← Tests (vacío, Fase 2)
│
├── web/                                   ← [ARC-07] Dashboard Next.js (diferido Fase 3)
│   └── .gitkeep
│
└── docs/                                  ← [ARC-08] Documentación SDD y gobernanza
    ├── reqs/                              ← PRDs por etapa
    ├── specs/                             ← SPECs por etapa
    ├── plans/                             ← Planes de implementación
    ├── tasks/                             ← Task lists atómicas
    ├── executives/                        ← Resúmenes ejecutivos (gate de avance)
    ├── lessons/
    │   └── lessons-learned.md            ← Registro acumulativo de lecciones
    ├── changes/                           ← Controles de cambio (CC_XXXXX.md)
    └── database/
        └── schema.sql                     ← DDL Supabase (vacío, Etapa 1.2)
```

### Componentes de Arquitectura

| ID | Componente | Responsabilidad | REQ que satisface |
|---|---|---|---|
| `[ARC-01]` | `CLAUDE.md` | Fuente de verdad de reglas, dominio, stack y fases. Inmutable salvo CC aprobado. | `[REQ-01]` |
| `[ARC-02]` | `PROJECT_index.md` | Estado macro del proyecto. Actualizado por skill `/update-index`. | `[REQ-02]` |
| `[ARC-03]` | `PROJECT_handoff.md` | Estado táctico de sesión. Reescrito al cierre por skill `/session-close`. | `[REQ-03]` |
| `[ARC-04]` | `.gitignore` | Excluye del repositorio: secretos, entornos virtuales, caché y artefactos de build. | `[REQ-08]` |
| `[ARC-05]` | `.claude/skills/` | 5 skills de gobernanza invocables por el agente. Cada uno en `[nombre]/SKILL.md`. | `[REQ-07]` |
| `[ARC-06]` | `pipeline/` | Motor de datos Python. Stub en esta etapa; implementación en Fase 2. | `[REQ-05]` |
| `[ARC-07]` | `web/` | Dashboard Next.js. Placeholder en esta etapa; implementación en Fase 3. | `[REQ-06]` |
| `[ARC-08]` | `docs/` | Árbol documental SDD con 8 subdirectorios canónicos. | `[REQ-04]`, `[REQ-09]` |

---

## 2. Especificaciones de Artefactos de Gobernanza

> *Esta etapa no tiene tablas Supabase ni esquemas Pandera. Esta sección especifica el contenido mínimo obligatorio de cada artefacto de gobernanza.*

### 2.1 — `.gitignore` (implementa `[REQ-08]`)

Exclusiones mínimas obligatorias:

```gitignore
# Entornos virtuales Python
venv/
.venv/
env/

# Caché Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Secretos y configuración local
.env
.env.*
*.env

# Configuración MCP local (credenciales de herramientas)
.mcp.json

# Dependencias Node.js
node_modules/

# Build Next.js
web/.next/
web/out/

# Artefactos de datos (DVC gestiona esto)
*.csv
*.parquet
*.pkl

# OS
.DS_Store
Thumbs.db

# IDEs
.vscode/settings.json
.idea/
```

### 2.2 — `pipeline/config.yaml` (implementa `[REQ-10]`)

Estructura base con claves placeholder. **Prohibido valores reales de credenciales:**

```yaml
# config.yaml — Dashboard MultiTodo
# Configuración global del pipeline. Los secretos van en .env (nunca aquí).

project:
  name: "Dashboard MultiTodo"
  client: "Almacen MultiTodo"
  developer: "Sabbia Solutions & Services (Triple S)"
  timezone: "America/Bogota"         # UTC-5. Usar pytz — nunca offsets manuales.
  data_lag_days: 1                   # T-1: siempre datos del día anterior completo.

supabase:
  url: "${SUPABASE_URL}"             # Definir en .env
  key: "${SUPABASE_KEY}"             # Definir en .env — anon key para lectura
  service_role_key: "${SUPABASE_SERVICE_ROLE_KEY}"  # Definir en .env — solo pipeline

tables:
  # Tablas del cliente (solo lectura para Triple S)
  ventas: "usr_ventas"
  inventario: "usr_inventario"
  productos: "usr_productos"
  sedes: "usr_sedes"
  # Tablas de Triple S
  bronze_ventas: "tss_bronze_ventas"
  bronze_inventario: "tss_bronze_inventario"
  silver_ventas: "tss_silver_ventas"
  silver_inventario: "tss_silver_inventario"
  gold_metricas: "tss_gold_metricas"
  gold_clasificacion_abc: "tss_gold_clasificacion_abc"
  error_log: "tss_error_log"
  pipeline_log: "tss_pipeline_log"
  quarantine: "tss_quarantine"
  alerts: "tss_alerts"

pipeline:
  modes:
    - validate
    - etl
    - alerts
  operational_window_utc:
    start: "13:00"                   # 08:00 COT
    end: "23:00"                     # 18:00 COT

alerts:
  abc_recalc_day: "monday"           # Clasificación ABC recalculada cada lunes
  abc_window_days: 90                # Ventana de análisis ABC: últimos 90 días
  default_window_days: 7             # Ventana de análisis de alertas: últimos 7 días
  thresholds:
    stock_critico_dias: 3            # ALT_NEG_001: stock < 3 días de venta
    stock_saludable_dias: 7          # ALT_POS_003: stock > 7 días de venta
    rotacion_lenta_pct: 0.30         # ALT_NEG_002: ventas < 30% del promedio categoría
    caida_ventas_pct: 0.50           # ALT_NEG_003: ventas < 50% del histórico día semana
    alta_rotacion_pct: 1.50          # ALT_POS_001: ventas > 150% del promedio histórico SKU
    crecimiento_categoria_pct: 0.20  # ALT_POS_002: crecimiento > 20% vs mes anterior
    margen_minimo_pct: 0.15          # ALT_NEG_006: margen < 15% en Clase A
    margen_estrella_pct: 0.35        # ALT_POS_004/006: margen > 35%
    sede_alto_rendimiento_pct: 0.15  # ALT_POS_005: margen sede > promedio + 15%
    obsoleto_dias_sin_venta: 30      # ALT_NEG_005: sin ventas en 30+ días
    abc_clase_a_percentil: 0.20      # Top 20% SKUs por valor acumulado
    abc_clase_b_percentil: 0.50      # Siguientes 30% (20% a 50%)
```

### 2.3 — `pipeline/main.py` stub (implementa `[REQ-05]`)

Gateway mínimo que define los modos sin implementar lógica de negocio:

```python
"""
main.py — Gateway del Pipeline Dashboard MultiTodo
Modos: validate | etl | alerts

Uso:
    python main.py --mode validate
    python main.py --mode etl
    python main.py --mode alerts
"""
import argparse


VALID_MODES = ["validate", "etl", "alerts"]


def main():
    parser = argparse.ArgumentParser(description="Pipeline Dashboard MultiTodo")
    parser.add_argument(
        "--mode",
        choices=VALID_MODES,
        required=True,
        help=f"Modo de ejecución: {', '.join(VALID_MODES)}"
    )
    args = parser.parse_args()

    # Stub: implementación en Fase 2
    print(f"[Pipeline] Modo '{args.mode}' recibido. Implementación pendiente — Fase 2.")


if __name__ == "__main__":
    main()
```

### 2.4 — `docs/lessons/lessons-learned.md` (implementa `[REQ-09]`)

Estructura base obligatoria:

```markdown
# Lecciones Aprendidas — Dashboard MultiTodo

> Registro acumulativo por etapa. Solo leer la sección de la etapa activa al iniciar sesión.
> Actualizado automáticamente por el skill `/session-close` al cierre de cada sesión.

---

## Fase 1 — Gobernanza y Cimientos

### Etapa 1.1 — Constitución del Proyecto
*(Sección creada. Se poblará con lecciones al cerrar la etapa.)*

### Etapa 1.2 — Validación de Infraestructura
*(Pendiente de inicio.)*

### Etapa 1.3 — Data Contract
*(Pendiente de inicio.)*

---

## Fase 2 — Ingeniería de Datos e Integración
*(Pendiente de inicio.)*

---

## Fase 3 — Analítica y Alertas
*(Pendiente de inicio.)*

---

## Fase 4 — Operación y Mejora Continua
*(Pendiente de inicio.)*
```

---

## 3. Convenciones de Nombres y Rutas

> *Esta etapa no produce módulos Python de negocio. Esta sección especifica las convenciones que todos los artefactos futuros deben respetar.*

### 3.1 — Convención de archivos SDD

| Tipo de Doc | Patrón de nombre | Ejemplo (Fase 1, Etapa 2) |
|---|---|---|
| PRD | `docs/reqs/f[FF]_[EE]_prd.md` | `docs/reqs/f01_02_prd.md` |
| SPEC | `docs/specs/f[FF]_[EE]_spec.md` | `docs/specs/f01_02_spec.md` |
| Plan | `docs/plans/f[FF]_[EE]_plan.md` | `docs/plans/f01_02_plan.md` |
| Tasks | `docs/tasks/f[FF]_[EE]_task.md` | `docs/tasks/f01_02_task.md` |
| Ejecutivo | `docs/executives/f[FF]_[EE]_executive.md` | `docs/executives/f01_02_executive.md` |
| Control de Cambio | `docs/changes/CC_[NNNNN].md` | `docs/changes/CC_00001.md` |

- `[FF]` = número de fase con cero a la izquierda (01, 02, 03, 04)
- `[EE]` = número de etapa con cero a la izquierda (01, 02, 03)
- `[NNNNN]` = número secuencial de 5 dígitos (00001, 00002…)

### 3.2 — Convención de archivos Python (`pipeline/`)

| Componente | Convención | Ejemplo |
|---|---|---|
| Módulos `src/` | `snake_case.py` | `supabase_client.py` |
| Tests | `test_[nombre_modulo].py` | `test_supabase_client.py` |
| Clases | `CamelCase` | `BronzeLoader` |
| Funciones | `snake_case` | `load_bronze_ventas()` |
| Constantes | `UPPER_SNAKE_CASE` | `ERR_MTD_001` |

### 3.3 — Convención de tablas Supabase

| Prefijo | Propietario | Acceso | Ejemplo |
|---|---|---|---|
| `usr_` | Cliente (Almacén MultiTodo) | Solo lectura para Triple S | `usr_ventas` |
| `tss_bronze_` | Triple S — capa Bronze | Lectura/Escritura pipeline | `tss_bronze_ventas` |
| `tss_silver_` | Triple S — capa Silver | Lectura/Escritura pipeline | `tss_silver_ventas` |
| `tss_gold_` | Triple S — capa Gold | Lectura/Escritura pipeline | `tss_gold_metricas` |
| `tss_` (otros) | Triple S — operacional | Lectura/Escritura pipeline | `tss_error_log` |

---

## 4. Estructura de Carpetas Vacías (`.gitkeep`)

Git no trackea directorios vacíos. Cada carpeta que debe existir en el repositorio pero aún no tiene contenido requiere un archivo `.gitkeep`:

| Carpeta | `.gitkeep` requerido | Razón |
|---|---|---|
| `pipeline/pipelines/` | ✅ Sí | Vacía hasta Fase 2 |
| `pipeline/src/` | ✅ Sí | Vacía hasta Fase 2 |
| `pipeline/tests/` | ✅ Sí | Vacía hasta Fase 2 |
| `web/` | ✅ Sí | Vacía hasta Fase 3 |
| `docs/reqs/` | ❌ No | Tendrá `f01_01_prd.md` al crear esta SPEC |
| `docs/specs/` | ❌ No | Tendrá este archivo |
| `docs/plans/` | ✅ Sí | Vacía hasta crear el Plan |
| `docs/tasks/` | ✅ Sí | Vacía hasta crear las Tasks |
| `docs/executives/` | ✅ Sí | Vacía hasta cerrar Etapa 1.1 |
| `docs/changes/` | ✅ Sí | Vacía hasta el primer CC |
| `docs/database/` | ✅ Sí | Vacía hasta Etapa 1.2 |

---

## 5. Configuración de Entorno (`.env`)

El archivo `.env` **no se commitea** (está en `.gitignore`). Se crea manualmente en cada entorno. Estructura mínima esperada:

```env
# .env — Dashboard MultiTodo
# NUNCA commitear este archivo. Está en .gitignore.

# Supabase
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_KEY=[anon-public-key]
SUPABASE_SERVICE_ROLE_KEY=[service-role-key]
```

> La existencia y validez de estas variables se verifica en Etapa 1.2, no en esta etapa.

---

## 6. Matriz de Diseño vs PRD

| REQ | Artefacto que lo implementa | Ruta | Notas |
|---|---|---|---|
| `[REQ-01]` | `CLAUDE.md` — 11 secciones completas | `CLAUDE.md` | Ya existe. Verificar completitud. |
| `[REQ-02]` | `PROJECT_index.md` — plantilla `/update-index` | `PROJECT_index.md` | Ya existe (creado en sesión actual). |
| `[REQ-03]` | `PROJECT_handoff.md` — plantilla `/session-close` | `PROJECT_handoff.md` | Pendiente de crear. |
| `[REQ-04]` | 8 subdirectorios en `docs/` | `docs/[reqs|specs|plans|tasks|executives|lessons|changes|database]/` | Parcialmente existentes (reqs/ y specs/ ya tienen contenido). |
| `[REQ-05]` | `pipeline/main.py` stub + `config.yaml` + subcarpetas | `pipeline/` | Pendiente de crear (ver §2.2 y §2.3). |
| `[REQ-06]` | `web/` con `.gitkeep` | `web/.gitkeep` | Pendiente de crear. |
| `[REQ-07]` | 5 skills en `.claude/skills/[nombre]/SKILL.md` | `.claude/skills/` | Ya existe (creado en sesión actual). |
| `[REQ-08]` | `.gitignore` con exclusiones mínimas | `.gitignore` | Pendiente de crear (ver §2.1). |
| `[REQ-09]` | `docs/lessons/lessons-learned.md` con estructura base | `docs/lessons/lessons-learned.md` | Pendiente de crear (ver §2.4). |
| `[REQ-10]` | `pipeline/config.yaml` con claves placeholder | `pipeline/config.yaml` | Pendiente de crear (ver §2.2). |
