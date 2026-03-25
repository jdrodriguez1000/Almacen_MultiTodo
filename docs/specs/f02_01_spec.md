# SPEC — Mockup Interactivo (`f02_01`)

> **Trazabilidad:** Este documento implementa los requerimientos definidos en `docs/reqs/f02_01_prd.md`.

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Cliente:** Almacén MultiTodo
**Fase:** 2 — Ingeniería de Datos e Integración | **Etapa:** 2.1
**Versión:** 1.0
**Fecha:** 2026-03-25
**Estado:** ✅ Aprobado
**Documentos relacionados:** `docs/reqs/f02_01_prd.md` | `docs/plans/f02_01_plan.md` | `docs/tasks/f02_01_task.md`
**Trazabilidad upstream:** `CC_00002` | `CC_00003` | `docs/specs/f01_03_spec.md` | `docs/database/schema.sql`

---

## 1. Arquitectura del Mockup

### 1.1 Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAPA DE DATOS (JSON LOCAL)                       │
│  web/src/data/                                                          │
│  mock_ventas.json  mock_inventario.json  mock_productos.json            │
│  mock_sedes.json   mock_gold.json        mock_alertas.json              │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │  Única capa que importa los JSON
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      CAPA DE SERVICIO (Service Layer)                   │
│  web/src/services/                                                      │
│  ventas.service.ts    inventario.service.ts    productos.service.ts     │
│  sedes.service.ts     alertas.service.ts       gold.service.ts          │
│                                                                         │
│  Implementación Mockup: retorna datos del JSON local.                   │
│  Implementación Producción (Etapa 3.3): retorna queries a Supabase.     │
│  Los componentes son indiferentes a cuál implementación está activa.    │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │  Funciones tipadas — sin `any`
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     CAPA DE COMPONENTES (React)                         │
│  web/src/components/                                                    │
│  layout/   alertas/   inventario/   ventas/   shared/                   │
│                                                                         │
│  Componentes React + TypeScript. Consumen datos exclusivamente          │
│  a través de funciones del Service Layer. Nunca importan JSON.          │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │  Props tipadas
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          CAPA DE VISTAS (App Router)                    │
│  web/src/app/                                                           │
│  page.tsx           (/)            Resumen General                      │
│  alertas/page.tsx   (/alertas)     Alertas y Oportunidades              │
│  inventarios/page.tsx (/inventarios) Inventarios filtrable              │
│  ventas/page.tsx    (/ventas)      Ventas por Sede                      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Principio de Migración Cero

**Definición:** El Service Layer es la única barrera de cambio entre el mockup y el dashboard de producción. Todo lo que esté por encima del Service Layer (componentes, vistas, tipos TypeScript) no se modifica al conectar Supabase en Etapa 3.3.

**Contrato del principio:**

| Capa | Mockup (Etapa 2.1) | Producción (Etapa 3.3) | ¿Cambia? |
|---|---|---|---|
| `data/mock_*.json` | Fuente de datos ficticia | Se descarta | Sí — se elimina |
| `services/*.service.ts` | Importa JSON y retorna datos | Ejecuta query a Supabase | Sí — solo la implementación |
| `types/usr.types.ts` | Tipos que espejean `usr_*` | Idénticos — mismos campos | No |
| `types/gold.types.ts` | Tipos para métricas derivadas | Idénticos — mismos campos | No |
| `components/**` | Consumen funciones del servicio | Consumen funciones del servicio | No |
| `app/**` (vistas) | Llaman al servicio | Llaman al servicio | No |

**Regla de cumplimiento:** Si al crear un componente se produce un `import` desde `data/mock_*.json`, hay una violación del principio. El componente debe pasar por el servicio.

### 1.3 Stack Tecnológico Exacto

| Tecnología | Versión | Uso |
|---|---|---|
| Next.js | 14+ (App Router) | Framework web, enrutamiento, SSR/SSG |
| TypeScript | 5+ (`strict: true`) | Tipado estático obligatorio en todo el código |
| Tailwind CSS | 3+ (`darkMode: 'class'`) | Estilos utilitarios — sin CSS-in-JS ni módulos CSS |
| React | 18+ | Librería de componentes (incluida en Next.js 14) |
| Node.js | 18+ | Runtime para `npm run dev` |
| `lucide-react` | latest | Íconos outline para sidebar y UI — estilo consistente con Inspiración 2 |
| `next/font/google` | (built-in Next.js) | Fuente Inter — tipografía de referencia de ambas imágenes de inspiración |
| Recharts | latest | Gráficos (AreaChart, BarChart) — colores dinámicos según modo claro/oscuro |

**Dependencias `package.json` (sección `dependencies`):**
```json
"recharts": "^2.x",
"lucide-react": "^0.x"
```
`next/font/google` no requiere instalación adicional — viene incluido en Next.js 14.

---

## 2. Estructura de Carpetas (`web/`)

La estructura completa del directorio `web/` al finalizar la etapa:

```
web/
├── package.json                   # Next.js 14, TypeScript, Tailwind, Recharts
├── tsconfig.json                  # strict: true obligatorio
├── tailwind.config.ts
├── next.config.ts
├── .eslintrc.json
└── src/
    ├── app/                       # App Router — rutas del dashboard
    │   ├── layout.tsx             # Layout raíz con Header persistente + banners
    │   ├── page.tsx               # Vista: Resumen General (/)
    │   ├── globals.css            # Estilos globales Tailwind
    │   ├── alertas/
    │   │   └── page.tsx           # Vista: Alertas (/alertas)
    │   ├── inventarios/
    │   │   └── page.tsx           # Vista: Inventarios (/inventarios)
    │   └── ventas/
    │       └── page.tsx           # Vista: Ventas por Sede (/ventas)
    ├── components/                # Componentes React reutilizables
    │   ├── layout/
    │   │   ├── Header.tsx         # Encabezado superior: nombre dashboard, banner T-1
    │   │   ├── Sidebar.tsx        # Navegación lateral izquierda con íconos + etiquetas
    │   │   └── BannerPrototipo.tsx # Banner fijo top: "PROTOTIPO — Datos ficticios..."
    │   ├── alertas/
    │   │   ├── AlertaCard.tsx     # Tarjeta individual de alerta (código, ícono, mensaje, sede)
    │   │   ├── AlertaList.tsx     # Lista de alertas con separación negativas/positivas
    │   │   └── SeveridadBadge.tsx # Badge visual: critico/alto/medio con colores
    │   ├── inventario/
    │   │   ├── TablaInventario.tsx  # Tabla filtrable por sede y clase ABC
    │   │   ├── StockBadge.tsx       # Badge de estado: Crítico/Bajo/Normal/Óptimo
    │   │   └── FiltrosInventario.tsx # Controles dropdown: sede, clase ABC
    │   ├── ventas/
    │   │   ├── GraficoVentasSedes.tsx  # Gráfico barras comparativo Recharts
    │   │   ├── TablaResumenSedes.tsx   # Tabla: sede, ventas, variación %, margen, ranking
    │   │   └── FiltroPeriodo.tsx       # Selector de período ficticio
    │   └── shared/
    │       ├── KpiCard.tsx         # Tarjeta de KPI: título, valor, variación, ícono
    │       ├── TendenciaChart.tsx  # Gráfico barras 7 días Recharts
    │       ├── TopSkuRiesgo.tsx    # Tabla top 5 SKUs en riesgo
    │       └── LoadingState.tsx    # Estado de carga (spinner/skeleton)
    ├── services/                  # Capa de abstracción de datos
    │   ├── ventas.service.ts
    │   ├── inventario.service.ts
    │   ├── productos.service.ts
    │   ├── sedes.service.ts
    │   ├── alertas.service.ts
    │   └── gold.service.ts
    ├── types/                     # Contratos de tipos TypeScript
    │   ├── usr.types.ts           # Espeja exactamente las tablas usr_*
    │   └── gold.types.ts          # Tipos para métricas derivadas (capa Gold)
    └── data/                      # JSON de datos ficticios
        ├── mock_ventas.json
        ├── mock_inventario.json
        ├── mock_productos.json
        ├── mock_sedes.json
        ├── mock_gold.json
        └── mock_alertas.json
```

**Regla de organización:** Ningún archivo fuera de `src/services/` puede importar desde `src/data/`. Esta restricción se verifica con una regla de ESLint (`no-restricted-imports`) configurada en `.eslintrc.json`.

---

## 3. Contratos de Tipos TypeScript — `usr.types.ts`

Los tipos en este archivo espejean **exactamente** los esquemas de las tablas `usr_*` de Supabase definidos en `docs/database/schema.sql`. Los nombres de campo son idénticos a los nombres de columna SQL. Los tipos TypeScript son los equivalentes directos de los tipos PostgreSQL.

**Referencia de equivalencia de tipos:**

| PostgreSQL | TypeScript |
|---|---|
| `bigserial` / `integer` / `serial` | `number` |
| `text` | `string` |
| `numeric(10,2)` | `number` |
| `timestamp with time zone` | `string` (ISO 8601) |
| `NULL` permitido | `\| null` |

```typescript
// web/src/types/usr.types.ts
// IMPORTANTE: Este archivo es la fuente de verdad de tipos en el frontend.
// Los campos deben mantenerse sincronizados con docs/database/schema.sql.
// Cambios en el esquema Supabase requieren CC aprobado antes de modificar este archivo.

// Espeja public.usr_ventas
// fecha_hora se almacena en UTC. Al mostrar en UI, convertir a COT (America/Bogota).
// Ejemplo: "2024-03-22T15:30:00Z" = 10:30 AM COT del 22 de marzo
export interface Venta {
  id_venta: number              // bigserial PK
  fecha_hora: string            // ISO 8601 UTC — ej: "2024-03-22T15:30:00Z"
  sku: string                   // FK -> usr_productos.sku
  id_sede: number               // FK -> usr_sedes.id_sede
  cantidad: number              // > 0
  precio: number                // numeric(10,2) > 0
  costo: number | null          // numeric(10,2) > 0 si presente
}

// Espeja public.usr_inventario
// Clave primaria compuesta: (sku, id_sede)
export interface InventarioItem {
  sku: string                   // FK -> usr_productos.sku
  id_sede: number               // FK -> usr_sedes.id_sede
  stock_fisico: number          // integer >= 0
  costo_reposicion: number | null  // numeric(10,2) > 0 si presente
}

// Espeja public.usr_productos
// Jerarquía: familia > categoria > subcategoria
export interface Producto {
  sku: string                   // PK
  nombre: string                // nombre comercial del producto
  familia: string               // nivel 1 de la jerarquía
  categoria: string             // nivel 2 de la jerarquía
  subcategoria: string          // nivel 3 de la jerarquía
}

// Espeja public.usr_sedes
// Total de registros en datos reales: exactamente 7 sedes activas
export interface Sede {
  id_sede: number               // serial PK
  pais: string                  // DEFAULT 'Colombia'
  ciudad: string                // ciudad de operación
  nombre_sede: string           // nombre del punto de venta
}
```

**Campos excluidos intencionalmente:** `created_at` y `updated_at` están presentes en las tablas `usr_*` pero no son campos de negocio — el mockup no los necesita para ninguna visualización. Si algún componente los requiriera en el futuro, se agregan al tipo con un CC previo.

---

## 4. Contratos de Tipos TypeScript — `gold.types.ts`

Los tipos en este archivo representan datos derivados que en el sistema productivo provendrán de las tablas `tss_gold_*` (creadas en Etapa 2.4). En el mockup se consumen desde `mock_gold.json` y `mock_alertas.json`.

```typescript
// web/src/types/gold.types.ts
// Tipos para datos calculados de la capa Gold.
// En producción (Etapa 3.3) estos tipos mapearán a tss_gold_* en Supabase.
// Los nombres de campo de los tipos deben mantenerse estables — son el contrato entre
// el Service Layer y los componentes. Si la implementación del servicio cambia,
// el tipo no cambia.

// Clasificación ABC — recalculada cada lunes sobre últimos 90 días
// Distribución objetivo: A=20%, B=30%, C=50% del total de SKUs
export type ClaseABC = 'A' | 'B' | 'C'

export interface ClasificacionABC {
  sku: string
  clase_abc: ClaseABC
}

// Métricas de inventario por SKU/sede — calculadas sobre datos T-7 a T-1
export interface MetricaInventario {
  sku: string
  id_sede: number
  promedio_venta_7d: number     // unidades vendidas por día en promedio (últimos 7 días)
  dias_cobertura: number        // stock_fisico / promedio_venta_7d (0 si promedio = 0)
}

// Alerta generada por el motor de alertas (CLAUDE.md §9)
// En mockup: pre-calculada en mock_alertas.json
// En producción: calculada por Etapa 3.2 sobre capa Gold
export type TipoAlerta = 'negativa' | 'positiva'
export type SeveridadAlerta = 'critico' | 'alto' | 'medio'

export interface Alerta {
  codigo: string                // ej: "ALT_NEG_001" | "ALT_POS_003"
  tipo: TipoAlerta
  severidad: SeveridadAlerta    // solo aplica a tipo 'negativa'
  sku: string | null            // null para alertas de categoría o sede
  id_sede: number | null        // null para alertas globales
  mensaje: string               // mensaje en lenguaje natural (español)
  fecha_calculo: string         // ISO 8601 — fecha en que se calculó la alerta
}

// Estructura raíz del archivo mock_gold.json
// Agrupa todas las métricas derivadas en un solo objeto
export interface DatosGold {
  clasificacion_abc: ClasificacionABC[]
  metricas_inventario: MetricaInventario[]
}

// Tipo auxiliar para estado visual de stock (usado en TablaInventario)
export type EstadoStock = 'critico' | 'bajo' | 'normal' | 'optimo'

// Función auxiliar de clasificación (lógica de dominio — va en gold.service.ts, no aquí)
// critico: dias_cobertura < 3
// bajo:    dias_cobertura >= 3 y < 7
// normal:  dias_cobertura >= 7 y <= 14
// optimo:  dias_cobertura > 14
```

---

## 5. Contratos de Servicio — `services/`

### 5.1 Regla de implementación

Cada servicio sigue este patrón invariable:

```typescript
// Patrón de implementación de un servicio (mockup)
import tipo from '@/types/...'
import datos from '@/data/mock_....json'  // SOLO en services/ — nunca en componentes

export async function getFuncion(): Promise<Tipo[]> {
  // En mockup: retorna datos del JSON
  // En producción: retorna datos de Supabase (mismo tipo de retorno)
  return datos as Tipo[]
}
```

La firma de las funciones (nombre, parámetros, tipo de retorno) es inmutable una vez que un componente la consume. Cambios de firma requieren CC.

### 5.2 `ventas.service.ts`

| Función | Parámetros | Retorno | Descripción |
|---|---|---|---|
| `getVentas()` | — | `Promise<Venta[]>` | Todas las ventas del período ficticio |
| `getVentasPorSede(id_sede?: number)` | `id_sede` opcional | `Promise<Venta[]>` | Ventas filtradas por sede. Sin parámetro: todas las sedes |
| `getTendencia7d()` | — | `Promise<TendenciaDia[]>` | Ventas agrupadas por día, últimos 7 días. Tipo auxiliar: `{ fecha: string, total_ventas: number, total_monto: number }` |
| `getResumenPorSede()` | — | `Promise<ResumenSede[]>` | Ventas agregadas por sede con variación y margen. Tipo auxiliar definido en §5.7 |

### 5.3 `inventario.service.ts`

| Función | Parámetros | Retorno | Descripción |
|---|---|---|---|
| `getInventario()` | — | `Promise<InventarioItem[]>` | Todo el inventario (todos los combos sku×sede) |
| `getInventarioPorSede(id_sede?: number)` | `id_sede` opcional | `Promise<InventarioItem[]>` | Inventario filtrado por sede |
| `getInventarioPorClase(clase: ClaseABC)` | `clase: ClaseABC` | `Promise<InventarioItem[]>` | Inventario filtrado por clasificación ABC |
| `getStockCritico()` | — | `Promise<InventarioItem[]>` | Registros con `stock_fisico = 0` o `dias_cobertura < 3` |

### 5.4 `productos.service.ts`

| Función | Parámetros | Retorno | Descripción |
|---|---|---|---|
| `getProductos()` | — | `Promise<Producto[]>` | Catálogo completo de productos |
| `getProductoBySku(sku: string)` | `sku: string` | `Promise<Producto \| null>` | Producto por SKU. `null` si no existe |
| `getProductosByCategoria(categoria: string)` | `categoria: string` | `Promise<Producto[]>` | Productos de una categoría |

### 5.5 `sedes.service.ts`

| Función | Parámetros | Retorno | Descripción |
|---|---|---|---|
| `getSedes()` | — | `Promise<Sede[]>` | Las 7 sedes activas |
| `getSedeById(id_sede: number)` | `id_sede: number` | `Promise<Sede \| null>` | Sede por ID. `null` si no existe |

### 5.6 `alertas.service.ts`

| Función | Parámetros | Retorno | Descripción |
|---|---|---|---|
| `getAlertas()` | — | `Promise<Alerta[]>` | Las 12 alertas ordenadas: negativas primero por severidad, luego positivas |
| `getAlertasNegativas()` | — | `Promise<Alerta[]>` | Solo las 6 alertas negativas, ordenadas: critico → alto → medio |
| `getAlertasPositivas()` | — | `Promise<Alerta[]>` | Solo las 6 alertas positivas |
| `getAlertasCriticas()` | — | `Promise<Alerta[]>` | Solo alertas con `severidad = 'critico'` (subset de negativas) |
| `contarPorSeveridad()` | — | `Promise<ConteoSeveridad>` | Tipo auxiliar: `{ critico: number, alto: number, medio: number }` |

### 5.7 `gold.service.ts`

| Función | Parámetros | Retorno | Descripción |
|---|---|---|---|
| `getClasificacionABC()` | — | `Promise<ClasificacionABC[]>` | Clasificación de todos los SKUs |
| `getClasePorSku(sku: string)` | `sku: string` | `Promise<ClaseABC \| null>` | Clase de un SKU específico |
| `getMetricasInventario()` | — | `Promise<MetricaInventario[]>` | Métricas derivadas para todos los combos sku×sede |
| `getMetricasBySku(sku: string)` | `sku: string` | `Promise<MetricaInventario[]>` | Métricas de un SKU en todas sus sedes |
| `getEstadoStock(dias_cobertura: number)` | `dias_cobertura: number` | `EstadoStock` | Función pura: clasifica días de cobertura en estado visual |

**Implementación de `getEstadoStock`** (función pura, sin async):

```typescript
export function getEstadoStock(dias_cobertura: number): EstadoStock {
  if (dias_cobertura < 3)  return 'critico'
  if (dias_cobertura < 7)  return 'bajo'
  if (dias_cobertura <= 14) return 'normal'
  return 'optimo'
}
```

### 5.8 Tipos auxiliares de servicio

Estos tipos se definen dentro de cada archivo de servicio (no en `types/`) porque son específicos de la capa de presentación y no espejean tablas de base de datos:

```typescript
// En ventas.service.ts
export interface TendenciaDia {
  fecha: string          // formato "YYYY-MM-DD"
  total_ventas: number   // cantidad de transacciones
  total_monto: number    // suma de (cantidad * precio)
}

export interface ResumenSede {
  id_sede: number
  nombre_sede: string
  ciudad: string
  total_monto: number
  variacion_pct: number  // vs período anterior ficticio
  margen_estimado: number  // porcentaje promedio del período
  ranking: number
}

// En alertas.service.ts
export interface ConteoSeveridad {
  critico: number
  alto: number
  medio: number
}
```

---

## 6. Especificación de Vistas

### 6.1 Vista: Resumen General (`/`)

**Propósito:** Vista de inicio del dashboard. El Gerente General debe entender el estado del negocio en menos de 1 minuto (`[MET-02]`).

**Componentes:**
- `Header` (layout) — encabezado persistente con banner T-1 y banner prototipo
- `KpiCard` × 4 (shared) — tarjetas de KPI
- `TopSkuRiesgo` (shared) — tabla top 5 SKUs en riesgo
- `TendenciaChart` (shared) — gráfico de barras 7 días
- Mini-panel de alertas (inline en la vista, no componente separado)

**Funciones de servicio consumidas:**
- `getVentas()` — para calcular total de ventas del período
- `getAlertasCriticas()` — para conteo de alertas críticas activas
- `getSedes()` — para conteo de sedes activas
- `getClasificacionABC()` + `getInventario()` + `getMetricasInventario()` — para SKUs Clase A sin stock
- `getTendencia7d()` — para gráfico de tendencia
- `getMetricasInventario()` — para tabla Top 5 SKUs en riesgo (menor `dias_cobertura`)
- `contarPorSeveridad()` — para mini-panel de alertas

**KPIs de la vista (4 tarjetas):**

| KPI | Cálculo | Icono sugerido |
|---|---|---|
| Ventas Totales (período) | Suma de `cantidad * precio` de `mock_ventas.json` | Tendencia al alza |
| SKUs en alerta crítica | Longitud de `getAlertasCriticas()` | Campana de alerta |
| Sedes activas | Longitud de `getSedes()` | Mapa pin |
| SKUs Clase A sin stock | SKUs con `clase_abc = 'A'` y `stock_fisico = 0` | Caja vacía |

**Layout:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ BANNER PROTOTIPO (sticky top, amber)                                │
├──────────────┬──────────────────────────────────────────────────────┤
│              │ Header: "Dashboard MultiTodo" + banner T-1 (azul)    │
│  SIDEBAR     ├──────────────────────────────────────────────────────┤
│  ─────────   │ [KPI 1]   [KPI 2]   [KPI 3]   [KPI 4]               │
│  Dashboard ← │                                                      │
│  Alertas     ├───────────────────────────────┬──────────────────────┤
│  Inventarios │ Gráfico tendencia 7 días       │ Top 5 SKUs en riesgo │
│  Ventas      │ (Recharts AreaChart o BarChart)│ (tabla compacta)     │
│              ├───────────────────────────────┴──────────────────────┤
│              │ Resumen alertas: [N crítico] [N alto] [N medio] →    │
└──────────────┴──────────────────────────────────────────────────────┘
```

### 6.2 Vista: Alertas (`/alertas`)

**Propósito:** Vista dedicada a las 12 alertas del sistema. Un gerente debe identificar qué alertas son críticas en menos de 30 segundos (`[REQ-03]`).

**Componentes:**
- `Header` (layout)
- `AlertaList` (alertas) — lista completa con secciones
- `AlertaCard` × 12 (alertas) — una tarjeta por alerta
- `SeveridadBadge` (alertas) — badge de severidad en cada tarjeta

**Funciones de servicio consumidas:**
- `getAlertasNegativas()` — sección "Alertas Activas"
- `getAlertasPositivas()` — sección "Oportunidades del Día"

**Estructura de una `AlertaCard`:**

| Campo | Fuente | Presentación |
|---|---|---|
| Código | `alerta.codigo` | Texto monoespaciado: `ALT_NEG_001` |
| Ícono severidad | `alerta.severidad` | Rojo=critico, naranja=alto, amarillo=medio |
| Mensaje | `alerta.mensaje` | Texto en lenguaje natural |
| Sede | `alerta.id_sede` → `getSedes()` | Nombre de la sede o "Todas las sedes" |
| Fecha | `alerta.fecha_calculo` | Formato `DD/MM/YYYY` |

**Layout:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ BANNER PROTOTIPO                                                     │
├──────────────┬──────────────────────────────────────────────────────┤
│              │ Header + banner T-1                                  │
│  SIDEBAR     ├──────────────────────────────────────────────────────┤
│  ─────────   │ ALERTAS ACTIVAS (6)                                  │
│  Dashboard   │ ┌──────────────────────────────────────────────────┐ │
│  Alertas  ←  │ │ 🔴 ALT_NEG_004 — Mensaje — Sede X — Fecha       │ │
│  Inventarios │ │ 🔴 ALT_NEG_001 — Mensaje — Sede Y — Fecha       │ │
│  Ventas      │ │ 🟠 ALT_NEG_002 — Mensaje — Sede Z — Fecha       │ │
│              │ │ ...                                              │ │
│              │ └──────────────────────────────────────────────────┘ │
│              ├──────────────────────────────────────────────────────┤
│              │ OPORTUNIDADES DEL DÍA (6)                           │
│              │ ┌──────────────────────────────────────────────────┐ │
│              │ │ 🟢 ALT_POS_001 — Mensaje — Sede X — Fecha       │ │
│              │ │ ...                                              │ │
│              │ └──────────────────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────────────────┘
```

**Orden de alertas negativas:** `ALT_NEG_004` (crítico, desabastecimiento) → `ALT_NEG_001` (crítico/alto, stock crítico) → resto ordenado por severidad descendente.

### 6.3 Vista: Inventarios (`/inventarios`)

**Propósito:** Vista operativa para el Gerente de Operaciones. Debe poder filtrar y encontrar el inventario de una sede en menos de 10 segundos (`[REQ-04]`).

**Componentes:**
- `Header` (layout)
- `FiltrosInventario` (inventario) — dropdowns de sede y clase ABC
- `TablaInventario` (inventario) — tabla filtrable con estado visual
- `StockBadge` (inventario) — badge de estado por fila

**Funciones de servicio consumidas:**
- `getSedes()` — para poblar el dropdown de sede
- `getInventario()` — dataset base para la tabla
- `getProductos()` — para mostrar nombre del producto junto al SKU
- `getClasificacionABC()` — para columna de clasificación
- `getMetricasInventario()` — para columna de días de cobertura
- `getEstadoStock(dias_cobertura)` — para `StockBadge`

**Columnas de la tabla:**

| Columna | Fuente | Tipo |
|---|---|---|
| SKU | `InventarioItem.sku` | Texto |
| Nombre | `Producto.nombre` (join por sku) | Texto |
| Clase | `ClasificacionABC.clase_abc` (join por sku) | Badge A/B/C |
| Stock actual | `InventarioItem.stock_fisico` | Número |
| Días cobertura | `MetricaInventario.dias_cobertura` | Número con 1 decimal |
| Estado | `getEstadoStock(dias_cobertura)` | `StockBadge` |

**Comportamiento de filtros:**
- Filtro por sede: dropdown con "Todas las sedes" + las 7 sedes. Al seleccionar, filtra `inventario` por `id_sede`.
- Filtro por clase ABC: dropdown con "Todas" + A, B, C. Al seleccionar, filtra `clasificacion_abc` y muestra solo los SKUs de esa clase.
- Los filtros son acumulables: se puede filtrar por sede Y por clase simultáneamente.
- El filtrado ocurre en el cliente (estado React) — sin recarga de página ni llamada al servicio.

**Colores de `StockBadge`:**

| Estado | Condición | Color Tailwind |
|---|---|---|
| Crítico | `dias_cobertura < 3` | `bg-red-100 text-red-800` |
| Bajo | `3 <= dias_cobertura < 7` | `bg-orange-100 text-orange-800` |
| Normal | `7 <= dias_cobertura <= 14` | `bg-yellow-100 text-yellow-800` |
| Óptimo | `dias_cobertura > 14` | `bg-green-100 text-green-800` |

### 6.4 Vista: Ventas por Sede (`/ventas`)

**Propósito:** Vista estratégica para el Gerente de Ventas. Debe poder identificar la sede con mejor y peor desempeño de forma visual e inmediata (`[REQ-05]`).

**Componentes:**
- `Header` (layout)
- `FiltroPeriodo` (ventas) — selector de período ficticio (últimos 7 días)
- `GraficoVentasSedes` (ventas) — gráfico Recharts BarChart comparativo
- `TablaResumenSedes` (ventas) — tabla con métricas agregadas por sede

**Funciones de servicio consumidas:**
- `getResumenPorSede()` — datos agregados para tabla y gráfico
- `getSedes()` — para enriquecer con nombre y ciudad

**Columnas de `TablaResumenSedes`:**

| Columna | Fuente | Formato |
|---|---|---|
| Ranking | `ResumenSede.ranking` | Número con ícono medalla para top 3 |
| Sede | `ResumenSede.nombre_sede` | Texto |
| Ciudad | `ResumenSede.ciudad` | Texto |
| Ventas período | `ResumenSede.total_monto` | Moneda COP con separador de miles |
| Variación | `ResumenSede.variacion_pct` | Porcentaje con flecha ↑↓ y color |
| Margen estimado | `ResumenSede.margen_estimado` | Porcentaje |

**`GraficoVentasSedes`:** BarChart horizontal de Recharts. Eje Y: nombres de sedes. Eje X: monto total de ventas. Las barras se colorean por ranking (la sede top en verde, la sede con menor rendimiento en naranja).

---

## 7. Especificación de Datos Ficticios

### 7.1 Reglas Generales

- Todos los JSON deben pasar validación de tipos TypeScript sin `any`.
- Los JSON se ubican en `web/src/data/` y nunca se commitean datos reales del cliente.
- Las fechas en `mock_ventas.json` usan UTC y caen dentro de la ventana operativa: horas entre 13 y 22 (inclusive). El formato es ISO 8601: `"2026-03-18T14:30:00Z"`.
- Las fechas de las ventas deben ser T-1 a T-7 relativas a una fecha ficticia de referencia (no T+0 ni fechas del día actual real).
- La fecha de referencia ficticia para los datos es `2026-03-24` (T-1 = lunes, inicio de semana laboral para el cliente). El banner T-1 del header mostrará `"Datos al cierre de: 24/03/2026"`.

### 7.2 `mock_ventas.json`

**Estructura:** Array de objetos `Venta[]`

**Reglas de construcción:**

| Parámetro | Valor requerido |
|---|---|
| Cantidad de registros | Mínimo 500 |
| Rango de fechas | 7 días: `2026-03-18` a `2026-03-24` (T-7 a T-1) + 7 días previos `2026-03-11` a `2026-03-17` para calcular variaciones |
| Horas UTC | Entre 13:00 y 22:59 (ventana operativa válida) |
| Sedes | Los 7 `id_sede` (1 al 7) deben tener ventas. Distribución no uniforme: Bogotá/Medellín con más volumen |
| SKUs | Mínimo 80 SKUs distintos activos en el período |
| `costo` | Presente en ~80% de los registros, `null` en ~20% |
| Cantidades | Entre 1 y 20 unidades por transacción |
| Precios | Entre $2.000 y $150.000 COP |
| Márgenes implícitos | Costo entre 55% y 85% del precio (margen bruto 15%–45%) |

### 7.3 `mock_inventario.json`

**Estructura:** Array de objetos `InventarioItem[]`

**Reglas de construcción:**

| Parámetro | Valor requerido |
|---|---|
| Cobertura | Todos los combos sku×sede donde hubo ventas en el período |
| SKUs sin stock | Exactamente 5 SKUs con `stock_fisico = 0` (activan `ALT_NEG_004`) |
| SKUs con stock crítico | Al menos 10 SKUs con `dias_cobertura < 3` (activan `ALT_NEG_001`) |
| Distribución | ~60% stock normal u óptimo, ~25% bajo, ~15% crítico o sin stock |
| `costo_reposicion` | Presente en ~70% de los registros, `null` en ~30% |

### 7.4 `mock_productos.json`

**Estructura:** Array de objetos `Producto[]`

**Reglas de construcción:**

| Parámetro | Valor requerido |
|---|---|
| Total de SKUs | ~100 productos (entre 90 y 110) |
| Familias | Mínimo 5: Alimentos, Aseo del Hogar, Bebidas, Cuidado Personal, Lácteos y Frescos |
| Categorías | Mínimo 15, distribuidas entre las familias |
| Subcategorías | Mínimo 30, distribuidas entre las categorías |
| Nombres | Representativos de abarrotes/consumo masivo colombiano (marcas genéricas — sin marcas reales registradas) |
| SKUs | Formato alfanumérico: `MTD-XXXXX` (ej: `MTD-00001`, `MTD-00087`) |

**Ejemplos de jerarquía para referencia:**

| Familia | Categoría | Subcategoría | Ejemplo de nombre |
|---|---|---|---|
| Alimentos | Granos y Cereales | Arroz | Arroz blanco premium x 500g |
| Alimentos | Granos y Cereales | Frijoles | Frijoles bola roja x 500g |
| Bebidas | Bebidas Calientes | Café | Café molido x 250g |
| Aseo del Hogar | Limpieza | Detergentes | Detergente en polvo x 1kg |
| Lácteos y Frescos | Lácteos | Leche | Leche entera UHT x 1L |

### 7.5 `mock_sedes.json`

**Estructura:** Array de objetos `Sede[]`

**Reglas de construcción:** Exactamente 7 registros. Los datos corresponden al dominio de negocio definido en `CLAUDE.md §7`:

| `id_sede` | `pais` | `ciudad` | `nombre_sede` |
|---|---|---|---|
| 1 | Colombia | Bogotá | MultiTodo Chapinero |
| 2 | Colombia | Bogotá | MultiTodo Suba |
| 3 | Colombia | Medellín | MultiTodo El Poblado |
| 4 | Colombia | Cali | MultiTodo Norte |
| 5 | Colombia | Cali | MultiTodo Sur |
| 6 | Colombia | Cartagena | MultiTodo Bocagrande |
| 7 | Colombia | Cúcuta | MultiTodo Centro |

### 7.6 `mock_gold.json`

**Estructura:** Objeto `DatosGold` con dos arrays

**Reglas de construcción:**

| Sección | Contenido | Distribución requerida |
|---|---|---|
| `clasificacion_abc` | Un registro por SKU del catálogo | Clase A: ~20% (20 SKUs), Clase B: ~30% (30 SKUs), Clase C: ~50% (50 SKUs) |
| `metricas_inventario` | Un registro por combo sku×sede con stock | `promedio_venta_7d` coherente con `mock_ventas.json`. `dias_cobertura` coherente con `mock_inventario.json` |

**Coherencia obligatoria:** Los SKUs con `stock_fisico = 0` en `mock_inventario.json` deben tener `dias_cobertura = 0` en `mock_gold.json`. Los SKUs con las ventas más altas deben ser Clase A.

### 7.7 `mock_alertas.json`

**Estructura:** Array de objetos `Alerta[]`

**Reglas de construcción:** Exactamente 12 registros — uno por código de alerta definido en `CLAUDE.md §9`:

| Código | Tipo | Severidad | Referencia de mensaje |
|---|---|---|---|
| `ALT_NEG_001` | negativa | alto | Stock crítico — referencia un SKU con `dias_cobertura < 3` de `mock_gold.json` |
| `ALT_NEG_002` | negativa | medio | Rotación lenta Clase A/B — referencia un SKU Clase A de `mock_gold.json` |
| `ALT_NEG_003` | negativa | medio | Caída anómala de ventas — referencia una categoría de `mock_productos.json` |
| `ALT_NEG_004` | negativa | critico | Desabastecimiento — referencia uno de los 5 SKUs con `stock_fisico = 0` |
| `ALT_NEG_005` | negativa | medio | Producto obsoleto — referencia un SKU Clase C con stock |
| `ALT_NEG_006` | negativa | alto | Margen comprimido Clase A — referencia un SKU Clase A |
| `ALT_POS_001` | positiva | medio | Alta rotación — referencia un SKU con `promedio_venta_7d` elevado |
| `ALT_POS_002` | positiva | medio | Categoría en crecimiento — referencia una categoría |
| `ALT_POS_003` | positiva | medio | Reabastecimiento exitoso — referencia un SKU con buen stock |
| `ALT_POS_004` | positiva | medio | Producto estratégico — SKU Clase A con margen > 35% |
| `ALT_POS_005` | positiva | medio | Sede de alto rendimiento — referencia una sede |
| `ALT_POS_006` | positiva | medio | Equilibrio óptimo — SKU Clase A con días cobertura entre 7 y 14 |

**Nota sobre `severidad` en alertas positivas:** El tipo `SeveridadAlerta` aplica formalmente solo a alertas negativas. Para las alertas positivas, el campo `severidad` se fija en `'medio'` por convención — no implica urgencia sino que mantiene consistencia del tipo.

---

## 8. Banner de Prototipo

### 8.1 Especificación del banner

El mockup debe mostrar dos banners diferenciados en el encabezado, visibles en todas las vistas:

**Banner 1 — Indicador T-1 (permanente en producción):**
```
Datos al cierre de: 24/03/2026
```
- Posición: parte superior del `Header`, siempre visible
- Estilo: fondo `bg-blue-50`, texto `text-blue-700`, borde inferior sutil
- Propósito: representa el comportamiento real del dashboard en producción

**Banner 2 — Indicador de Prototipo (solo en mockup):**
```
PROTOTIPO — Datos ficticios para validación de diseño
```
- Posición: barra fija en la parte superior del viewport (por encima del Header)
- Estilo: fondo `bg-amber-400`, texto `text-amber-900`, `font-semibold`, ancho completo
- `position: sticky, top: 0, z-index: 50`
- Propósito: prevenir que el cliente confunda el mockup con el dashboard funcional (`[RSK-02]`)
- Este banner se elimina al construir el dashboard real en Etapa 3.3

### 8.2 Componente `BannerPrototipo`

El banner de prototipo se implementa como un componente independiente (`BannerPrototipo.tsx`) importado en `layout.tsx`. Al eliminar el mockup, basta con remover esa línea del layout — ningún otro componente se afecta.

---

## 9. Criterios de Aceptación Técnicos

Lista verificable para considerar la Etapa 2.1 técnicamente completa. Cada ítem debe pasar antes de presentar el mockup al cliente.

### 9.1 Compilación y arranque

- [ ] `npm install` completa sin errores ni conflictos de dependencias
- [ ] `npm run build` completa sin errores de TypeScript (`strict: true` activo en `tsconfig.json`)
- [ ] `npm run dev` levanta la aplicación en `localhost:3000` sin errores en consola del navegador ni en terminal
- [ ] `npx tsc --noEmit` pasa sin errores — cero instancias de `any` en `src/`

### 9.2 Principio de Migración Cero

- [ ] Ningún archivo en `src/components/` contiene `import ... from '@/data/mock_*.json'`
- [ ] Ningún archivo en `src/app/` contiene `import ... from '@/data/mock_*.json'`
- [ ] La regla ESLint `no-restricted-imports` está configurada para prevenir imports de `@/data/` fuera de `@/services/`
- [ ] Los tipos en `usr.types.ts` compilan sin errores contra los datos de los JSON locales

### 9.3 Vistas y navegación

- [ ] Las 4 vistas (`/`, `/alertas`, `/inventarios`, `/ventas`) cargan y muestran datos sin errores
- [ ] La navegación entre vistas es fluida — sin recarga completa de página (Next.js App Router)
- [ ] El botón "Volver al inicio" o la navegación principal está presente en todas las vistas

### 9.4 Funcionalidad específica

- [ ] Los filtros de la vista Inventarios (sede y clase ABC) funcionan sin recarga de página
- [ ] Los filtros son acumulables: sede + clase funcionan simultáneamente
- [ ] La vista de Alertas muestra exactamente 6 alertas negativas y 6 positivas
- [ ] Las alertas negativas están ordenadas por severidad (crítico primero)
- [ ] El gráfico de ventas por sede en `/ventas` renderiza correctamente con Recharts
- [ ] El gráfico de tendencia 7 días en `/` renderiza correctamente con Recharts

### 9.5 Banners

- [ ] El banner de prototipo (`"PROTOTIPO — Datos ficticios..."`) está visible en las 4 vistas
- [ ] El banner T-1 (`"Datos al cierre de: 24/03/2026"`) está visible en las 4 vistas
- [ ] Los banners no obstruyen el contenido principal de ninguna vista

### 9.6 Datos y consistencia

- [ ] `mock_sedes.json` tiene exactamente 7 registros
- [ ] `mock_alertas.json` tiene exactamente 12 registros (uno por cada código ALT_*)
- [ ] Los SKUs en `mock_alertas.json` existen en `mock_productos.json`
- [ ] Los `id_sede` en `mock_alertas.json` existen en `mock_sedes.json`
- [ ] La distribución ABC en `mock_gold.json` es aproximadamente 20/30/50

### 9.7 Modo Oscuro / Modo Claro

- [ ] El toggle `ThemeToggle` está visible en el header en todas las vistas
- [ ] Al hacer clic, el modo cambia visualmente de inmediato (sin parpadeo)
- [ ] Al recargar la página, el modo seleccionado se mantiene (`localStorage`)
- [ ] Todos los componentes son legibles en modo oscuro: sidebar, header, tarjetas KPI, tablas, gráficos, badges y banners
- [ ] Los gráficos Recharts usan `chartColors` dinámicos — no se ven blancos sobre blanco ni negros sobre negro en ningún modo
- [ ] El banner de prototipo (amber) y el banner T-1 (blue) son legibles en ambos modos

### 9.8 Responsivo

- [ ] El mockup es legible y funcional en resolución `1920×1080`
- [ ] El mockup es legible y funcional en resolución `1366×768`
- [ ] Ninguna tabla o gráfico se corta o vuelve ilegible en `1366×768`

### 9.8 Rendimiento

- [ ] El tiempo de carga inicial (primera carga desde `npm run dev`) es menor a 2 segundos (`[MET-03]`)
- [ ] Los filtros de Inventarios responden en menos de 500ms (`[MET-04]`)

---

## 10. Restricciones Técnicas

| ID | Restricción | Fuente |
|---|---|---|
| `[RES-01]` | TypeScript `strict: true` es obligatorio. Cero `any` en el código de producción. | CLAUDE.md §5 |
| `[RES-02]` | Los JSON de datos ficticios deben estructurarse exactamente como los esquemas `usr_*` de Supabase. Sin campos inventados en `usr.types.ts`. | PRD `[SUP-07]` |
| `[RES-03]` | Los servicios son la única capa que importa los JSON. Componentes y vistas son agnósticos a la fuente de datos. | PRD `[REQ-11]` |
| `[RES-04]` | El mockup es completamente client-side. Sin Server Actions, sin fetch a APIs externas, sin variables de entorno de runtime. | PRD `[REQ-08]` |
| `[RES-05]` | Tailwind CSS es la única herramienta de estilos. Sin CSS Modules, sin styled-components, sin inline styles complejos. | CLAUDE.md §3 |
| `[RES-06]` | Recharts es la librería de gráficos. No instalar alternativas (Chart.js, Victory, nivo) en esta etapa. | SPEC §1.3 |
| `[RES-07]` | El código del frontend va a rama `feat/etapa-2-1`. Los documentos SDD van a rama `main`. | CLAUDE.md §6 |
| `[RES-08]` | Sin autenticación, sin cookies, sin localStorage. El mockup no persiste ningún estado entre sesiones. | PRD fuera de alcance |
| `[RES-09]` | Las fechas del mockup son UTC. Al mostrar en UI: convertir a formato colombiano `DD/MM/YYYY`. No mostrar timestamps al usuario. | CLAUDE.md §2 |

---

## 11. Matriz de Trazabilidad SPEC → PRD

| Sección SPEC | Cubre REQ del PRD |
|---|---|
| §1 Arquitectura | `[REQ-01]`, `[REQ-08]`, `[REQ-11]` |
| §2 Estructura de carpetas | `[REQ-01]`, `[REQ-09]`, `[REQ-11]` |
| §12 Sistema Visual | `[REQ-02]`, `[REQ-09]`, `[REQ-10]`, `[RSK-02]` |
| §3 Tipos `usr.types.ts` | `[DAT-01]`–`[DAT-04]`, `[SUP-07]` |
| §4 Tipos `gold.types.ts` | `[DAT-05]`, `[DAT-06]` |
| §5 Contratos de servicio | `[REQ-11]` |
| §6.1 Vista Resumen General | `[REQ-06]`, `[REQ-07]`, `[REQ-10]` |
| §6.2 Vista Alertas | `[REQ-03]` |
| §6.3 Vista Inventarios | `[REQ-04]`, `[REQ-06]` |
| §6.4 Vista Ventas | `[REQ-05]` |
| §7 Datos ficticios | `[DAT-01]`–`[DAT-06]`, `[REQ-08]`, `[RSK-03]` |
| §8 Banner de prototipo | `[REQ-07]`, `[RSK-02]` |
| §9 Criterios de aceptación | `[MET-01]`–`[MET-07]` |
| §10 Restricciones | `[SUP-01]`–`[SUP-07]` |

---

---

## 12. Sistema Visual de Referencia

> Esta sección es la guía de diseño visual del mockup. Se deriva de la imagen de inspiración aprobada por el equipo (`Inspiracion 1.webp`). El mockup debe seguir estos lineamientos para garantizar un resultado profesional alineado con las expectativas del cliente.

### 12.1 Patrón de Layout General

El mockup adopta el patrón **sidebar + contenido principal** presente en la imagen de referencia:

| Zona | Descripción | Tailwind base |
|---|---|---|
| **Banner prototipo** | Barra fija en el top, ámbar, ancho completo | `fixed top-0 w-full z-50 bg-amber-400 dark:bg-amber-500` |
| **Sidebar** | Panel lateral izquierdo, fondo blanco/oscuro, ancho fijo `w-56`, altura completa | `fixed left-0 h-full bg-white dark:bg-gray-900 border-r border-gray-100 dark:border-gray-700 shadow-sm` |
| **Header** | Barra superior del área de contenido, con nombre del dashboard y banner T-1 | `bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-700` |
| **Área de contenido** | Fondo gris claro/muy oscuro, ocupa el resto del viewport | `ml-56 pt-[header] bg-gray-50 dark:bg-gray-950 min-h-screen` |

### 12.2 Sidebar (`Sidebar.tsx`)

El sidebar adopta el patrón de **menú + submenú con secciones etiquetadas** observado en la segunda imagen de referencia (`Inspiracion 2.webp`): los ítems se agrupan bajo etiquetas de sección en `uppercase tracking-wider text-xs`, y hay un bloque de perfil de usuario al pie.

**Estructura completa del sidebar:**

```
┌────────────────────────┐
│  🏪 MultiTodo          │  ← Logo + nombre (font-semibold)
│     Dashboard          │  ← subtítulo (text-xs text-gray-400)
├────────────────────────┤
│                        │
│ ⊞  Dashboard           │  ← ítem sin sección (activo: bg-green-50)
│                        │
│  ANÁLISIS              │  ← etiqueta de sección (text-xs uppercase tracking-wider text-gray-400)
│ ▦  Ventas por Sede     │
│ ◫  Inventarios         │
│                        │
│  ALERTAS               │  ← etiqueta de sección
│ 🔔 Alertas Activas     │
│ ✦  Oportunidades       │
│                        │
├────────────────────────┤
│ [avatar] Almacén       │  ← perfil al pie (text-sm font-medium)
│          MultiTodo     │  ← rol (text-xs text-gray-400)
└────────────────────────┘
```

**Especificación de ítems y secciones:**

| Sección | Ítem | Ruta | Ícono Lucide |
|---|---|---|---|
| *(sin sección)* | Dashboard | `/` | `LayoutDashboard` |
| **ANÁLISIS** | Ventas por Sede | `/ventas` | `BarChart2` |
| **ANÁLISIS** | Inventarios | `/inventarios` | `Package` |
| **ALERTAS** | Alertas Activas | `/alertas` | `Bell` |
| **ALERTAS** | Oportunidades | `/alertas#positivas` | `TrendingUp` |

**Clases por estado de ítem:**

| Estado | Clases Tailwind |
|---|---|
| Activo | `bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 font-medium rounded-lg` |
| Inactivo | `text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg` |
| Etiqueta de sección | `text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500 px-3 mt-4 mb-1` |

**Perfil al pie:**
```tsx
<div className="flex items-center gap-3 p-3 border-t border-gray-100 dark:border-gray-700">
  <div className="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
    <span className="text-green-700 dark:text-green-400 text-sm font-bold">AM</span>
  </div>
  <div>
    <p className="text-sm font-medium text-gray-900 dark:text-gray-50">Almacén MultiTodo</p>
    <p className="text-xs text-gray-400">Dashboard v2.1</p>
  </div>
</div>
```

**Íconos:** Todos los íconos de `lucide-react`, estilo **outline** (por defecto en Lucide), tamaño `w-4 h-4`. No usar íconos filled para mantener consistencia con la referencia.

### 12.3 Paleta de Colores — Modo Claro y Modo Oscuro

El mockup soporta modo claro y modo oscuro (`[REQ-12]`). Tailwind CSS gestiona el dark mode mediante la clase `dark` en el elemento `<html>` (estrategia `class`). Cada token tiene su variante dark definida.

**Configuración obligatoria en `tailwind.config.ts`:**
```typescript
darkMode: 'class'  // activa dark mode por clase, no por preferencia del sistema
```

| Token | Modo Claro | Modo Oscuro | Uso |
|---|---|---|---|
| **Primary** | `green-600` | `green-500` | Ítem activo sidebar, bordes de énfasis |
| **Primary light** | `green-50` | `green-900/30` | Fondo ítem activo sidebar |
| **Background** | `gray-50` | `gray-950` | Fondo área de contenido |
| **Surface** | `white` | `gray-900` | Tarjetas, sidebar, header |
| **Surface elevated** | `gray-100` | `gray-800` | Fondos de tablas, inputs |
| **Border** | `gray-100` | `gray-700` | Separadores, bordes de tarjetas |
| **Text primary** | `gray-900` | `gray-50` | Títulos, valores KPI |
| **Text secondary** | `gray-500` | `gray-400` | Labels, metadatos, fechas |
| **Danger** | `red-600` | `red-400` | Alertas críticas, badges rojo |
| **Warning** | `orange-500` | `orange-400` | Alertas alto, badges naranja |
| **Caution** | `yellow-500` | `yellow-400` | Alertas medio, badges amarillo |
| **Success** | `green-500` | `green-400` | Alertas positivas, stock óptimo |
| **Info** | `blue-600` | `blue-400` | Banner T-1, información neutral |
| **Prototype** | `amber-400` | `amber-500` | Banner de prototipo |

**Ejemplo de uso en componente (clase dual):**
```tsx
<div className="bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-700">
  <p className="text-gray-900 dark:text-gray-50 text-3xl font-bold">{valor}</p>
  <p className="text-gray-500 dark:text-gray-400 text-sm">{titulo}</p>
</div>
```

### 12.4 Toggle de Modo Oscuro

**Componente:** `ThemeToggle.tsx` en `components/layout/`

**Ubicación:** Esquina superior derecha del `Header`, siempre visible.

**Comportamiento:**
1. Al montar, lee `localStorage.getItem('theme')`. Si es `'dark'`, agrega clase `dark` al `<html>`.
2. Al hacer clic, alterna la clase `dark` en `<html>` y persiste en `localStorage`.
3. Si no hay preferencia guardada, usa modo claro por defecto.

**Implementación del hook:**
```typescript
// web/src/hooks/useTheme.ts
export function useTheme() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    const saved = localStorage.getItem('theme')
    if (saved === 'dark') {
      document.documentElement.classList.add('dark')
      setIsDark(true)
    }
  }, [])

  const toggle = () => {
    const next = !isDark
    setIsDark(next)
    document.documentElement.classList.toggle('dark', next)
    localStorage.setItem('theme', next ? 'dark' : 'light')
  }

  return { isDark, toggle }
}
```

**UI del toggle:** Ícono `Sun` (modo claro activo) / `Moon` (modo oscuro activo) de `lucide-react`. Botón circular `p-2 rounded-full` con hover sutil.

**Gráficos en modo oscuro (Recharts):** Los colores de ejes, grid y tooltips deben adaptarse:
```typescript
// Colores de Recharts según el modo
const chartColors = {
  bar: isDark ? '#22c55e' : '#16a34a',      // green-400 / green-600
  grid: isDark ? '#374151' : '#e5e7eb',     // gray-700 / gray-200
  text: isDark ? '#9ca3af' : '#6b7280',     // gray-400 / gray-500
  tooltip: isDark ? '#1f2937' : '#ffffff',  // gray-800 / white
}
```

### 12.4 Tipografía

**Fuente:** `Inter` (Google Fonts). Configurar en `layout.tsx` con `next/font/google`:

```typescript
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'] })
// Aplicar: <html className={inter.className}>
```

| Elemento | Clase Tailwind (claro + oscuro) | Referencia visual |
|---|---|---|
| Saludo / título principal de vista | `text-2xl font-semibold text-gray-900 dark:text-gray-50` | "Welcome back, Salung" → "Bienvenido" |
| Subtítulo / descripción de vista | `text-sm text-gray-500 dark:text-gray-400` | Debajo del título principal |
| **Etiqueta KPI** (label arriba del valor) | `text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400` | "TOTAL REVENUE", "NEW CUSTOMERS" |
| **Valor KPI** (número principal) | `text-2xl font-bold text-gray-900 dark:text-gray-50` | "$20,320" → "COP 4.2M" |
| Tendencia KPI positiva | `text-xs font-medium text-green-600 dark:text-green-400` | "↑ 8.3% last week" |
| Tendencia KPI negativa | `text-xs font-medium text-red-500 dark:text-red-400` | "↓ 2.1% last week" |
| Nombre de ítem de menú | `text-sm text-gray-700 dark:text-gray-300` | "Dashboard", "Transactions" |
| **Etiqueta de sección** (sidebar) | `text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500` | "CUSTOMERS", "MANAGEMENT" → "ANÁLISIS" |
| Encabezado de columna (tabla) | `text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400` | "NAME", "PROJECT", "STATUS" |
| Contenido de celda (tabla) | `text-sm text-gray-700 dark:text-gray-300` | Datos de filas |
| Texto secundario / metadatos | `text-xs text-gray-400 dark:text-gray-500` | Fechas, IDs, subtextos |
| Botón primario | `text-sm font-medium` + fondo green-600 | "Export CSV" → "Exportar" |

> **Patrón clave de la Inspiración 2:** las etiquetas de KPI y de sección del sidebar usan exactamente el mismo estilo — `text-xs uppercase tracking-wider` — creando consistencia visual entre el sidebar y el contenido principal.

### 12.5 Tarjetas KPI (`KpiCard.tsx`)

Inspiradas en las 4 tarjetas superiores de la imagen de referencia:

```
┌─────────────────────────────────┐
│ Ventas Totales          [ícono] │  ← label (gray-500) + ícono
│                                 │
│ COP 4.2M                        │  ← valor (3xl bold gray-900)
│ ↑ 8.3% vs semana anterior       │  ← variación (sm green-600 o red-600)
└─────────────────────────────────┘
```

**Props de `KpiCard`:**
```typescript
interface KpiCardProps {
  titulo: string
  valor: string           // ya formateado: "COP 4.2M", "7 sedes", "3 SKUs"
  variacion?: string      // ej: "+8.3%" o "-2.1%"
  tendencia?: 'up' | 'down' | 'neutral'
  icono: React.ReactNode  // componente Lucide
}
```

### 12.6 Gráficos

Inspirados en los gráficos de la imagen de referencia:

| Vista | Gráfico | Tipo Recharts | Notas |
|---|---|---|---|
| Resumen General | Tendencia 7 días | `AreaChart` con gradiente verde | Área rellena verde semi-transparente, línea verde sólida |
| Ventas por Sede | Comparativo sedes | `BarChart` con barras verdes | Barras verticales, una por sede |
| Resumen General (panel derecho) | Top 5 SKUs en riesgo | Tabla compacta, sin gráfico | Visual más limpio que un gráfico para datos tabulares |

**Paleta de gráficos (adaptada al modo):** Los colores de Recharts no leen clases Tailwind — se pasan como props. Usar el hook `useTheme` para obtener `isDark` y calcular los colores:

```typescript
const chartColors = {
  bar:     isDark ? '#22c55e' : '#16a34a',   // green-400 / green-600
  grid:    isDark ? '#374151' : '#e5e7eb',   // gray-700 / gray-200
  text:    isDark ? '#9ca3af' : '#6b7280',   // gray-400 / gray-500
  tooltip: isDark ? '#1f2937' : '#ffffff',   // gray-800 / white
  area:    isDark ? '#16a34a33' : '#16a34a1a', // verde 20% opacidad
}
```

### 12.7 Panel de Acciones / Alertas en Home

Inspirado en el panel "Recommended Actions" de la imagen de referencia, adaptado al sistema de alertas del proyecto:

```
┌──────────────────────────────────────────────────────┐
│ Alertas Activas                          Ver todas → │
│ ──────────────────────────────────────────────────── │
│ 🔴  SKU MTD-00012 sin stock en Chapinero             │
│      ALT_NEG_004 · Crítico · 24/03/2026              │
│                                                      │
│ 🟠  MTD-00034 (Clase A): Rotación baja esta semana   │
│      ALT_NEG_002 · Alto · 24/03/2026                 │
│                                                      │
│ 🟡  Categoría Bebidas cayó 55% vs histórico          │
│      ALT_NEG_003 · Medio · 24/03/2026                │
└──────────────────────────────────────────────────────┘
```

Este panel muestra solo las 3 alertas más críticas en el home. El link "Ver todas →" navega a `/alertas`.

---

*Documento generado con `/sdd-doc` (Modo B — Arquitecto de Software). Para requerimientos de negocio, ver `docs/reqs/f02_01_prd.md`.*
*Trazabilidad: `CC_00002` (incorporación) → `CC_00003` (reubicación como Etapa 2.1) → `docs/specs/f01_03_spec.md` (esquemas `usr_*`).*
*§12 agregado en sesión 2026-03-25 — inspiración visual:*
- *`Inspiracion 1.webp` — patrón sidebar + contenido, paleta verde, KPI cards con tendencia, gráficos AreaChart/BarChart.*
- *`Inspiracion 2.webp` — tipografía Inter, sidebar con secciones etiquetadas (menú/submenú), íconos outline Lucide, perfil al pie del sidebar.*
