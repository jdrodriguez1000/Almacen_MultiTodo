# Tareas — Mockup Interactivo (`f02_01`)

> **Trazabilidad:** Este documento es generado por el skill `/sdd-doc` (Modo D — Jefe de Proyecto) a partir de `docs/plans/f02_01_plan.md`, `docs/reqs/f02_01_prd.md` y `docs/specs/f02_01_spec.md`.

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Cliente:** Almacén MultiTodo
**Fase:** 2 — Ingeniería de Datos e Integración | **Etapa:** 2.1
**Fecha:** 2026-03-25
**Estado:** ✅ Aprobado — listo para ejecución
**Documentos relacionados:** `docs/reqs/f02_01_prd.md` | `docs/specs/f02_01_spec.md` | `docs/plans/f02_01_plan.md`
**Trazabilidad upstream:** `CC_00002` | `CC_00003`

---

## Estado General

- **Total:** 62 tareas
- **Completadas:** 0 / 62
- **Bloque activo:** B0 — Preparación del Entorno
- **Rama de trabajo:** `feat/etapa-2-1` (código) | `main` (documentos SDD)

### Resumen por bloque

| Bloque | Nombre | Tareas | Estado |
|---|---|---|---|
| B0 | Preparación del Entorno | 8 | ⬜ Pendiente |
| B1 | Tipos, Datos y Servicios | 14 | ⬜ Pendiente |
| B2 | Layout Base | 8 | ⬜ Pendiente |
| B3 | Componentes Reutilizables | 11 | ⬜ Pendiente |
| B4 | Vistas | 4 | ⬜ Pendiente |
| B5 | Validación y Cierre | 17 | ⬜ Pendiente |
| **Total** | | **62** | |

> **Regla de avance entre bloques:** Cada bloque debe superar su gate de salida antes de iniciar el siguiente. Un gate fallido detiene el avance hasta resolverse. Ver protocolo de bloqueadores en `docs/plans/f02_01_plan.md §5`.

---

## Bloque 0 — Preparación del Entorno

> **Propósito:** Dejar el entorno de desarrollo completamente funcional antes de escribir una sola línea de código de negocio.
> **Gate de salida:** `npm run dev` levanta en `localhost:3000` sin errores en terminal ni en consola del navegador.

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-001` | Crear rama `feat/etapa-2-1` desde `main`. Comando: `git checkout main && git pull && git checkout -b feat/etapa-2-1` | `dev-frontend` | Plan B0-01 · CLAUDE.md §6 | ⬜ Pendiente |
| `TSK-2.1-002` | Inicializar proyecto Next.js 14 con TypeScript en `web/`. Comando: `npx create-next-app@latest web --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"`. Confirmar App Router = Yes. | `dev-frontend` | Plan B0-02 · SPEC §1.3 · [REQ-01] | ⬜ Pendiente |
| `TSK-2.1-003` | Verificar y configurar `web/tsconfig.json`: confirmar que `"strict": true` está presente. Si no, agregar la línea antes de continuar. | `dev-frontend` | Plan B0-03 · SPEC §1.3 | ⬜ Pendiente |
| `TSK-2.1-004` | Instalar dependencias adicionales desde `web/`: `npm install recharts lucide-react`. Verificar que ambas aparecen en `package.json` bajo `dependencies`. | `dev-frontend` | Plan B0-04 · SPEC §1.3 | ⬜ Pendiente |
| `TSK-2.1-005` | Verificar y configurar `web/tailwind.config.ts`: confirmar que `darkMode: 'class'` está presente. Si no, agregar la línea. | `dev-frontend` | Plan B0-05 · SPEC §1.3 · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-006` | Configurar regla ESLint `no-restricted-imports` en `web/.eslintrc.json`: prohibir `import` desde `@/data/` en cualquier archivo fuera de `@/services/`. Ver SPEC §2 para la regla exacta. | `dev-frontend` | Plan B0-06 · SPEC §1.2 y §2 · SPEC §9.2 | ⬜ Pendiente |
| `TSK-2.1-007` | Crear estructura de carpetas vacías en `web/src/`: `types/`, `data/`, `services/`, `hooks/`, `components/layout/`, `components/alertas/`, `components/inventario/`, `components/ventas/`, `components/shared/`. No crear archivos aún. | `dev-frontend` | Plan B0-07 · SPEC §2 | ⬜ Pendiente |
| `TSK-2.1-008` | Gate B0: ejecutar `npm run dev` desde `web/`. Confirmar que el servidor levanta en `localhost:3000` y la página de bienvenida Next.js carga sin errores en consola. Este gate es prerequisito de Bloque 1 y Bloque 2. | `dev-frontend` | Plan B0-08 · SPEC §9.1 | ⬜ Pendiente |

---

## Bloque 1 — Tipos, Datos y Servicios

> **Propósito:** Construir los contratos de tipos TypeScript, los datos ficticios en JSON y la capa de servicios. Es la capa más crítica: define los contratos que todo el código superior consume.
> **Gate de salida:** `npx tsc --noEmit` pasa sin errores. Los 6 servicios existen, compilan y no contienen `any`. Ningún componente importa desde `@/data/`.
> **Orden obligatorio:** B1-01 → B1-02 → B1-03 → B1-04 → B1-05 y B1-06 (en paralelo) → B1-07 → B1-08 → B1-09 a B1-14 (servicios).

### 1.1 Tipos TypeScript

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-009` | Crear `web/src/types/usr.types.ts`. Interfaces: `Venta`, `InventarioItem`, `Producto`, `Sede`. Deben espejear exactamente las columnas de las tablas `usr_*` de `docs/database/schema.sql`. Sin `created_at` ni `updated_at`. Sin `any`. Ver definición completa en SPEC §3. | `dev-frontend` | Plan B1-01 · SPEC §3 · schema.sql · [DAT-01]–[DAT-04] | ⬜ Pendiente |
| `TSK-2.1-010` | Crear `web/src/types/gold.types.ts`. Tipos: `ClaseABC`, `ClasificacionABC`, `MetricaInventario`, `TipoAlerta`, `SeveridadAlerta`, `Alerta`, `DatosGold`, `EstadoStock`. La función `getEstadoStock` va en `gold.service.ts`, no aquí. Ver definición completa en SPEC §4. | `dev-frontend` | Plan B1-02 · SPEC §4 · [DAT-05]–[DAT-06] | ⬜ Pendiente |

### 1.2 Datos Ficticios (JSON)

> **Regla de coherencia:** Los cuatro JSON de datos brutos se construyen en orden maestras → transaccionales → derivados. La coherencia inter-JSON es verificada antes de implementar los servicios.

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-011` | Crear `web/src/data/mock_sedes.json`. Array de exactamente 7 objetos `Sede`. Datos exactos de SPEC §7.5: id_sede 1–7, ciudades Bogotá (×2), Medellín, Cali (×2), Cartagena, Cúcuta con nombres de sede definidos en la SPEC. | `dev-frontend` | Plan B1-03 · SPEC §7.5 · [DAT-04] · [REQ-05] | ⬜ Pendiente |
| `TSK-2.1-012` | Crear `web/src/data/mock_productos.json`. Array de ~100 objetos `Producto`. Formato SKU: `MTD-XXXXX`. Mínimo 5 familias, 15 categorías, 30 subcategorías. Nombres de productos colombianos de abarrotes/consumo masivo (marcas genéricas). Ver jerarquía de referencia en SPEC §7.4. | `dev-frontend` | Plan B1-04 · SPEC §7.4 · [DAT-03] · [REQ-08] | ⬜ Pendiente |
| `TSK-2.1-013` | Crear `web/src/data/mock_ventas.json`. Array de mínimo 500 objetos `Venta`. Fechas UTC en ventana 13:00–22:59. Rango: `2026-03-11` a `2026-03-24` (14 días). Los 7 `id_sede` deben tener ventas. Mínimo 80 SKUs distintos. `costo` presente en ~80%. Distribución de sedes con mayor volumen en Bogotá y Medellín. Ver reglas completas en SPEC §7.2. | `dev-frontend` | Plan B1-05 · SPEC §7.1 y §7.2 · [DAT-01] · [REQ-08] | ⬜ Pendiente |
| `TSK-2.1-014` | Crear `web/src/data/mock_inventario.json`. Array de objetos `InventarioItem`. Cubre todos los combos sku×sede con ventas. Exactamente 5 SKUs con `stock_fisico = 0`. Al menos 10 SKUs con `dias_cobertura < 3` (calculado manualmente). Ver distribución en SPEC §7.3. | `dev-frontend` | Plan B1-06 · SPEC §7.3 · [DAT-02] · [REQ-06] | ⬜ Pendiente |
| `TSK-2.1-015` | Crear `web/src/data/mock_gold.json`. Objeto `DatosGold` con dos arrays. `clasificacion_abc`: un registro por SKU, distribución 20/30/50 (A/B/C). `metricas_inventario`: un registro por combo sku×sede con `dias_cobertura` coherente con `mock_inventario.json`. Los 5 SKUs con `stock_fisico = 0` deben tener `dias_cobertura = 0`. Los SKUs con mayores ventas son Clase A. Ver SPEC §7.6. | `dev-frontend` | Plan B1-07 · SPEC §7.6 · [DAT-05] · [REQ-04] | ⬜ Pendiente |
| `TSK-2.1-016` | Crear `web/src/data/mock_alertas.json`. Array de exactamente 12 objetos `Alerta`, uno por código ALT_NEG_001–006 y ALT_POS_001–006. Los SKUs y `id_sede` referenciados deben existir en `mock_productos.json` y `mock_sedes.json`. Severidades: `ALT_NEG_004` y `ALT_NEG_001` en crítico/alto; alertas positivas en `'medio'`. Ver tabla completa en SPEC §7.7. | `dev-frontend` | Plan B1-08 · SPEC §7.7 · [DAT-06] · [REQ-03] · CLAUDE.md §9 | ⬜ Pendiente |
| `TSK-2.1-017` | Verificar coherencia inter-JSON (obligatoria antes de implementar servicios): (1) todo `sku` en `mock_ventas.json` existe en `mock_productos.json`, (2) todo `sku` en `mock_inventario.json` existe en `mock_productos.json`, (3) todo `id_sede` en `mock_ventas.json` y `mock_inventario.json` existe en `mock_sedes.json`, (4) los 5 SKUs con `stock_fisico = 0` tienen `dias_cobertura = 0` en `mock_gold.json`, (5) los SKUs en `mock_alertas.json` existen en `mock_productos.json`, (6) los `id_sede` en `mock_alertas.json` existen en `mock_sedes.json`. | `dev-frontend` | Plan B1 (verificación pre-B1-09) · SPEC §7.1 · [SUP-07] | ⬜ Pendiente |

### 1.3 Servicios

> **Regla de Migración Cero:** Los servicios son la única capa que importa JSON. Los componentes y vistas no pueden importar desde `@/data/`. Ver SPEC §1.2.

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-018` | Implementar `web/src/services/sedes.service.ts`. Funciones exportadas: `getSedes(): Promise<Sede[]>`, `getSedeById(id_sede: number): Promise<Sede \| null>`. Importa `mock_sedes.json`. Ver SPEC §5.5. | `dev-frontend` | Plan B1-09 · SPEC §5.5 · [REQ-11] | ⬜ Pendiente |
| `TSK-2.1-019` | Implementar `web/src/services/productos.service.ts`. Funciones exportadas: `getProductos(): Promise<Producto[]>`, `getProductoBySku(sku: string): Promise<Producto \| null>`, `getProductosByCategoria(categoria: string): Promise<Producto[]>`. Ver SPEC §5.4. | `dev-frontend` | Plan B1-10 · SPEC §5.4 · [REQ-11] | ⬜ Pendiente |
| `TSK-2.1-020` | Implementar `web/src/services/ventas.service.ts`. Funciones exportadas: `getVentas(): Promise<Venta[]>`, `getVentasPorSede(id_sede?: number): Promise<Venta[]>`, `getTendencia7d(): Promise<TendenciaDia[]>`, `getResumenPorSede(): Promise<ResumenSede[]>`. Tipos auxiliares `TendenciaDia` y `ResumenSede` definidos en el mismo archivo. Ver SPEC §5.2 y §5.8. | `dev-frontend` | Plan B1-11 · SPEC §5.2 y §5.8 · [REQ-11] | ⬜ Pendiente |
| `TSK-2.1-021` | Implementar `web/src/services/inventario.service.ts`. Funciones exportadas: `getInventario(): Promise<InventarioItem[]>`, `getInventarioPorSede(id_sede?: number): Promise<InventarioItem[]>`, `getInventarioPorClase(clase: ClaseABC): Promise<InventarioItem[]>`, `getStockCritico(): Promise<InventarioItem[]>`. `getInventarioPorClase` cruza con `mock_gold.json`. Ver SPEC §5.3. | `dev-frontend` | Plan B1-12 · SPEC §5.3 · [REQ-11] | ⬜ Pendiente |
| `TSK-2.1-022` | Implementar `web/src/services/gold.service.ts`. Funciones exportadas: `getClasificacionABC(): Promise<ClasificacionABC[]>`, `getClasePorSku(sku: string): Promise<ClaseABC \| null>`, `getMetricasInventario(): Promise<MetricaInventario[]>`, `getMetricasBySku(sku: string): Promise<MetricaInventario[]>`. Función pura (sin async): `getEstadoStock(dias_cobertura: number): EstadoStock`. Ver implementación exacta en SPEC §5.7. | `dev-frontend` | Plan B1-13 · SPEC §5.7 · [REQ-11] | ⬜ Pendiente |
| `TSK-2.1-023` | Implementar `web/src/services/alertas.service.ts`. Funciones exportadas: `getAlertas(): Promise<Alerta[]>`, `getAlertasNegativas(): Promise<Alerta[]>`, `getAlertasPositivas(): Promise<Alerta[]>`, `getAlertasCriticas(): Promise<Alerta[]>`, `contarPorSeveridad(): Promise<ConteoSeveridad>`. Tipo auxiliar `ConteoSeveridad` definido en el mismo archivo. `getAlertas()` retorna negativas primero (critico→alto→medio) luego positivas. Ver SPEC §5.6 y §5.8. | `dev-frontend` | Plan B1-14 · SPEC §5.6 y §5.8 · [REQ-03] · [REQ-11] | ⬜ Pendiente |

---

## Bloque 2 — Layout Base

> **Propósito:** Construir el esqueleto navegable del dashboard: hook de tema, banners, header, sidebar y root layout.
> **Gate de salida:** `npm run dev` muestra el shell completo en modo claro y oscuro. Toggle funcional. Preferencia persiste en recarga. Sin errores de compilación.
> **Prerequisito de inicio:** Bloque 1 completado (`npx tsc --noEmit` en verde).

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-024` | Crear `web/src/hooks/useTheme.ts`. Hook custom: lee/escribe en `localStorage` la clave `theme`. Aplica y remueve la clase `dark` en `document.documentElement`. Expone `{ theme, toggleTheme }`. Al montar: lee `localStorage`; si no hay valor, usa preferencia del sistema (`prefers-color-scheme`). | `dev-frontend` | Plan B2-01 · SPEC §1.3 · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-025` | Crear `web/src/components/layout/BannerPrototipo.tsx`. Componente sin props. Barra fija ancho completo, `fixed top-0 z-50`, fondo `bg-amber-400 dark:bg-amber-500`, texto `"PROTOTIPO — Datos ficticios para validación de diseño"` en `text-amber-900 font-semibold text-sm text-center`. Ver SPEC §8.1 y §8.2. | `dev-frontend` | Plan B2-02 · SPEC §8.1 y §8.2 · [RSK-02] | ⬜ Pendiente |
| `TSK-2.1-026` | Crear `web/src/components/layout/ThemeToggle.tsx`. Botón que invoca `toggleTheme()` del hook `useTheme`. Icono `Sun` (modo claro) o `Moon` (modo oscuro) de `lucide-react`, tamaño `w-4 h-4`. Clases: `p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800`. | `dev-frontend` | Plan B2-03 · SPEC §1.3 · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-027` | Crear `web/src/components/layout/Header.tsx`. Contiene: nombre del dashboard (`"Dashboard MultiTodo"`), banner T-1 (`"Datos al cierre de: 24/03/2026"`, fondo `bg-blue-50 dark:bg-blue-950`, texto `text-blue-700 dark:text-blue-300`, `text-xs`) y `ThemeToggle` alineado a la derecha. Clases de contenedor: `bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-700 px-6 py-3`. Ver SPEC §8.1. | `dev-frontend` | Plan B2-04 · SPEC §8.1 · [REQ-07] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-028` | Crear `web/src/components/layout/Sidebar.tsx`. Sidebar lateral fijo izquierdo, `w-56`, altura completa. Secciones etiquetadas: `ANÁLISIS` (Dashboard, Inventarios, Ventas) y `ALERTAS` (Alertas). Íconos Lucide outline: `LayoutDashboard`, `BarChart2`, `Package`, `Bell`. Estado activo/inactivo según ruta actual con `usePathname` de Next.js. Perfil de usuario al pie. Dark mode completo. Ver SPEC §12.2 (referencia de clases). | `dev-frontend` | Plan B2-05 · SPEC §2 · [REQ-02] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-029` | Crear `web/src/app/globals.css`. Directivas Tailwind: `@tailwind base`, `@tailwind components`, `@tailwind utilities`. Regla global: `html { @apply bg-gray-50 dark:bg-gray-950 }`. Sin CSS custom adicional. | `dev-frontend` | Plan B2-06 · SPEC §2 | ⬜ Pendiente |
| `TSK-2.1-030` | Crear `web/src/app/layout.tsx` (root layout). Aplica fuente Inter via `next/font/google`. Importa `globals.css`. Monta `BannerPrototipo` fijo en el top. Monta `Sidebar` en el lateral izquierdo. Monta `Header` en la parte superior del área de contenido. El `{children}` ocupa el área de contenido con clases `ml-56` y padding apropiado. La clase `dark` se gestiona en `document.documentElement` via `useTheme`. | `dev-frontend` | Plan B2-07 · SPEC §2 · [REQ-07] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-031` | Gate B2: ejecutar `npm run dev`. Verificar: (a) banner ámbar visible en la parte superior, (b) sidebar visible con ítems de navegación, (c) header visible con nombre y banner T-1 azul, (d) toggle Sun/Moon funcional, (e) al hacer clic en toggle el fondo cambia entre claro y oscuro, (f) al recargar la página el modo persiste. | `dev-frontend` | Plan B2-08 · SPEC §9.7 · [REQ-12] | ⬜ Pendiente |

---

## Bloque 3 — Componentes Reutilizables

> **Propósito:** Construir todos los componentes React que las vistas ensamblarán. Los componentes reciben datos como props — nunca llaman a servicios directamente.
> **Gate de salida:** `npx tsc --noEmit` en verde. 11 componentes creados. Ninguno importa desde `@/data/`. `npm run lint` sin errores de `no-restricted-imports`.
> **Prerequisito de inicio:** Bloques 1 y 2 completados.

### 3.1 Componentes Compartidos (`shared/`)

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-032` | Crear `web/src/components/shared/KpiCard.tsx`. Props: `titulo: string`, `valor: string \| number`, `variacion?: number`, `tendencia?: 'up' \| 'down' \| 'neutral'`, `icono: React.ReactNode`. Fondo `bg-white dark:bg-gray-900`. Valor en `text-2xl font-bold`. Variación con color verde (positivo) o rojo (negativo) y flecha ↑↓. Dark mode completo. Ver SPEC §6.1. | `dev-frontend` | Plan B3-01 · SPEC §6.1 · [REQ-06] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-033` | Crear `web/src/components/shared/TendenciaChart.tsx`. Gráfico de área Recharts (`AreaChart`). Props: `datos: TendenciaDia[]` (tipo importado de `ventas.service.ts`). Colores dinámicos según modo claro/oscuro (consume `useTheme`). Ejes con fechas en formato `DD/MM`. Tooltip con monto en COP. `ResponsiveContainer` para ajuste automático. | `dev-frontend` | Plan B3-02 · SPEC §6.1 · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-034` | Crear `web/src/components/shared/TopSkuRiesgo.tsx`. Tabla compacta con top 5 SKUs de menor `dias_cobertura`. Props: `items: Array<{ sku: string, nombre: string, dias_cobertura: number, id_sede: number, nombre_sede: string }>`. Columnas: SKU (monoespaciado), nombre (truncado), días cobertura (resaltado en rojo si < 3), sede. Dark mode completo. Ver SPEC §6.1. | `dev-frontend` | Plan B3-03 · SPEC §6.1 · [REQ-10] | ⬜ Pendiente |

### 3.2 Componentes de Alertas (`alertas/`)

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-035` | Crear `web/src/components/alertas/SeveridadBadge.tsx`. Props: `severidad: SeveridadAlerta`. Colores: `critico` → `bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400`, `alto` → naranja, `medio` → amarillo. Texto en mayúsculas, `text-xs font-semibold`, `rounded-full px-2 py-0.5`. Ver SPEC §6.2. | `dev-frontend` | Plan B3-04 · SPEC §6.2 · [REQ-03] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-036` | Crear `web/src/components/alertas/AlertaCard.tsx`. Props: `alerta: Alerta`, `nombreSede: string \| null`. Muestra: código (monoespaciado, `text-xs`), `SeveridadBadge`, mensaje completo, nombre de sede o `"Todas las sedes"` si `id_sede = null`, fecha en formato `DD/MM/YYYY`. Borde izquierdo de color según severidad. Dark mode completo. Ver SPEC §6.2. | `dev-frontend` | Plan B3-05 · SPEC §6.2 · [REQ-03] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-037` | Crear `web/src/components/alertas/AlertaList.tsx`. Props: `negativas: Alerta[]`, `positivas: Alerta[]`, `sedes: Sede[]`. Secciones: `"Alertas Activas"` (negativas) y `"Oportunidades del Día"` (positivas). Usa `AlertaCard` para cada ítem, resolviendo nombre de sede del `id_sede`. Ver layout en SPEC §6.2. | `dev-frontend` | Plan B3-06 · SPEC §6.2 · [REQ-03] | ⬜ Pendiente |

### 3.3 Componentes de Inventario (`inventario/`)

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-038` | Crear `web/src/components/inventario/StockBadge.tsx`. Props: `estado: EstadoStock`. Colores según SPEC §6.3: `critico` → rojo, `bajo` → naranja, `normal` → amarillo, `optimo` → verde. Misma estructura visual que `SeveridadBadge`. Dark mode completo. | `dev-frontend` | Plan B3-07 · SPEC §6.3 · [REQ-04] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-039` | Crear `web/src/components/inventario/FiltrosInventario.tsx`. Props: `sedes: Sede[]`, `sedeFiltro: number \| null`, `claseFiltro: ClaseABC \| null`, `onSedeCambio: (id: number \| null) => void`, `onClaseCambio: (clase: ClaseABC \| null) => void`. Opciones "Todas las sedes" y "Todas las clases" como valor nulo. Componente controlado — estado gestionado en la vista padre. Dark mode completo. Ver SPEC §6.3. | `dev-frontend` | Plan B3-08 · SPEC §6.3 · [REQ-04] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-040` | Crear `web/src/components/inventario/TablaInventario.tsx`. Props: `items: InventarioItem[]`, `productos: Producto[]`, `clasificaciones: ClasificacionABC[]`, `metricas: MetricaInventario[]`. Columnas según SPEC §6.3: SKU, nombre (join con `productos`), clase (join con `clasificaciones`), stock actual, días cobertura (1 decimal), `StockBadge`. Mensaje vacío si no hay datos con los filtros activos. Dark mode completo. | `dev-frontend` | Plan B3-09 · SPEC §6.3 · [REQ-04] · [REQ-12] | ⬜ Pendiente |

### 3.4 Componentes de Ventas (`ventas/`)

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-041` | Crear `web/src/components/ventas/GraficoVentasSedes.tsx`. BarChart horizontal Recharts. Props: `datos: ResumenSede[]`. Eje Y: nombres de sedes. Eje X: monto total de ventas (formato COP). Barras coloreadas por ranking (sede top en verde, menor rendimiento en naranja). `ResponsiveContainer`. Colores dinámicos con `useTheme`. Ver SPEC §6.4. | `dev-frontend` | Plan B3-10 · SPEC §6.4 · [REQ-05] · [REQ-12] | ⬜ Pendiente |
| `TSK-2.1-042` | Crear `web/src/components/ventas/TablaResumenSedes.tsx`. Props: `datos: ResumenSede[]`. Columnas según SPEC §6.4: ranking (con ícono medalla para top 3), sede, ciudad, ventas período (COP con separador de miles), variación % (flecha ↑↓ con color), margen estimado %. Dark mode completo. | `dev-frontend` | Plan B3-11 · SPEC §6.4 · [REQ-05] · [REQ-12] | ⬜ Pendiente |

---

## Bloque 4 — Vistas

> **Propósito:** Ensamblar los componentes en las 4 vistas del dashboard. Las vistas son el único punto donde se invocan los servicios y se pasan los datos como props.
> **Gate de salida:** Las 4 vistas cargan con datos visibles y sin errores en consola. El sidebar marca correctamente la vista activa.
> **Prerequisito de inicio:** Bloques 1, 2 y 3 completados.

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-043` | Crear `web/src/app/page.tsx` (Resumen General — `/`). Servicios consumidos: `getVentas()`, `getAlertasCriticas()`, `getSedes()`, `getClasificacionABC()`, `getInventario()`, `getMetricasInventario()`, `getTendencia7d()`, `contarPorSeveridad()`. Renderiza: 4 `KpiCard` (ventas totales, SKUs en alerta crítica, sedes activas, SKUs Clase A sin stock), `TendenciaChart`, `TopSkuRiesgo` (top 5 menor `dias_cobertura`), mini-panel de conteo de alertas con enlace a `/alertas`. Ver layout en SPEC §6.1. | `dev-frontend` | Plan B4-01 · SPEC §6.1 · [REQ-06] · [MET-02] · [OBJ-03] | ⬜ Pendiente |
| `TSK-2.1-044` | Crear `web/src/app/alertas/page.tsx` (Vista Alertas — `/alertas`). Servicios consumidos: `getAlertasNegativas()`, `getAlertasPositivas()`, `getSedes()`. Renderiza: título de sección, `AlertaList` con las 12 alertas separadas en secciones negativas y positivas. Ver layout en SPEC §6.2. | `dev-frontend` | Plan B4-02 · SPEC §6.2 · [REQ-03] · [OBJ-02] | ⬜ Pendiente |
| `TSK-2.1-045` | Crear `web/src/app/inventarios/page.tsx` (Vista Inventarios — `/inventarios`). Estado local React: `sedeFiltro: number \| null`, `claseFiltro: ClaseABC \| null`. Servicios consumidos: `getSedes()`, `getInventario()`, `getProductos()`, `getClasificacionABC()`, `getMetricasInventario()`. Filtros aplicados en el cliente sin nueva llamada al servicio. Renderiza: `FiltrosInventario`, `TablaInventario` con datos filtrados. Ver SPEC §6.3. | `dev-frontend` | Plan B4-03 · SPEC §6.3 · [REQ-04] · [OBJ-03] | ⬜ Pendiente |
| `TSK-2.1-046` | Crear `web/src/app/ventas/page.tsx` (Vista Ventas — `/ventas`). Servicios consumidos: `getResumenPorSede()`, `getSedes()`. Renderiza: título de sección, `GraficoVentasSedes`, `TablaResumenSedes`. Ver SPEC §6.4. | `dev-frontend` | Plan B4-04 · SPEC §6.4 · [REQ-05] · [OBJ-03] | ⬜ Pendiente |

---

## Bloque 5 — Validación y Cierre

> **Propósito:** Verificar que el mockup cumple todos los criterios de aceptación técnicos de SPEC §9 antes de presentarlo al cliente. Ninguna tarea de este bloque es opcional.
> **Criterio de avance de etapa:** `TSK-2.1-062` con aprobación registrada. Sin aprobación del cliente, la etapa no se cierra aunque todos los criterios técnicos pasen.
> **Prerequisito de inicio:** Bloque 4 completado.

### 5.1 Verificación de Compilación y Calidad

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-047` | Ejecutar `npx tsc --noEmit` desde `web/`. Debe pasar con 0 errores y 0 instancias de `any` en `src/`. Si hay errores, corregirlos antes de avanzar. | `dev-frontend` | Plan B5-01 · SPEC §9.1 | ⬜ Pendiente |
| `TSK-2.1-048` | Ejecutar `npm run build` desde `web/`. Debe completar sin errores de TypeScript ni de Next.js. Si hay errores, corregirlos antes de avanzar. | `dev-frontend` | Plan B5-03 · SPEC §9.1 | ⬜ Pendiente |
| `TSK-2.1-049` | Ejecutar `npm run dev` desde `web/`. Verificar que no hay errores en consola del navegador ni en la terminal al cargar `localhost:3000`. | `dev-frontend` | Plan B5 · SPEC §9.1 | ⬜ Pendiente |

### 5.2 Verificación del Principio de Migración Cero

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-050` | Auditar todos los archivos en `web/src/components/`: confirmar que ninguno contiene `import ... from '@/data/mock_*.json'` ni `import ... from '@/data/'`. Si se encuentra alguno, corregirlo antes de avanzar. | `dev-frontend` | Plan B5-04 · SPEC §9.2 · [REQ-11] | ⬜ Pendiente |
| `TSK-2.1-051` | Auditar todos los archivos en `web/src/app/`: confirmar que ninguno importa directamente desde `@/data/`. Si se encuentra alguno, corregirlo antes de avanzar. | `dev-frontend` | Plan B5-05 · SPEC §9.2 · [REQ-11] | ⬜ Pendiente |

### 5.3 Verificación Funcional

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-052` | Verificar las 4 vistas: navegar a `/`, `/alertas`, `/inventarios`, `/ventas`. Confirmar que cada vista carga datos sin errores en consola y que la navegación entre vistas no recarga la página (App Router). | `dev-frontend` | Plan B5-06 · SPEC §9.3 · [REQ-02] · [MET-05] | ⬜ Pendiente |
| `TSK-2.1-053` | Verificar filtros de Inventarios: aplicar filtro por sede (tabla se actualiza), aplicar filtro por clase ABC (tabla se actualiza), aplicar ambos filtros simultáneamente (acumulables). Confirmar sin recarga de página. | `dev-frontend` | Plan B5-07 · SPEC §9.4 · [REQ-04] | ⬜ Pendiente |
| `TSK-2.1-054` | Verificar exactitud de alertas en `/alertas`: contar exactamente 6 alertas negativas y 6 positivas. Confirmar que las negativas están ordenadas con `ALT_NEG_004` (crítico) primero. | `dev-frontend` | Plan B5-08 · SPEC §9.4 · [REQ-03] · [MET-06] | ⬜ Pendiente |
| `TSK-2.1-055` | Verificar gráficos Recharts: `TendenciaChart` en `/` y `GraficoVentasSedes` en `/ventas` renderizan correctamente (áreas/barras visibles, ejes con etiquetas). En modo oscuro los gráficos no presentan colores ilegibles. | `dev-frontend` | Plan B5-12 · SPEC §9.4 y §9.7 · [REQ-12] | ⬜ Pendiente |

### 5.4 Verificación de Banners y Modo Oscuro

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-056` | Verificar banners: confirmar que el banner ámbar (`"PROTOTIPO — Datos ficticios para validación de diseño"`) está visible en las 4 vistas sin obstruir el contenido principal. | `dev-frontend` | Plan B5-10 · SPEC §9.5 · [RSK-02] | ⬜ Pendiente |
| `TSK-2.1-057` | Verificar banner T-1: confirmar que el banner azul (`"Datos al cierre de: 24/03/2026"`) está visible en las 4 vistas. | `dev-frontend` | Plan B5-10 · SPEC §9.5 · [REQ-07] | ⬜ Pendiente |
| `TSK-2.1-058` | Verificar dark mode completo: (a) toggle funcional — modo cambia de inmediato, (b) recarga mantiene el modo (localStorage), (c) sidebar, header, tarjetas KPI, tablas, gráficos, badges y banners son legibles en modo oscuro sin pérdida de información. | `dev-frontend` | Plan B5-09 · SPEC §9.7 · [REQ-12] | ⬜ Pendiente |

### 5.5 Verificación de Datos

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-059` | Verificar coherencia de datos: (a) `mock_sedes.json` tiene exactamente 7 registros, (b) `mock_alertas.json` tiene exactamente 12 registros, (c) los SKUs en `mock_alertas.json` existen en `mock_productos.json`, (d) los `id_sede` en `mock_alertas.json` existen en `mock_sedes.json`, (e) distribución ABC aproximadamente 20/30/50 en `mock_gold.json`. | `dev-frontend` | Plan B5-11 · SPEC §9.6 · [REQ-08] | ⬜ Pendiente |

### 5.6 Verificación de Responsivo y Rendimiento

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-060` | Verificar responsive en resolución 1366×768: usando DevTools cambiar viewport y navegar las 4 vistas. Confirmar que ninguna tabla o gráfico se corta o vuelve ilegible. | `dev-frontend` | Plan B5-14 · SPEC §9.8 · [REQ-09] | ⬜ Pendiente |

### 5.7 Cierre y Entrega

| ID | Tarea | Responsable | Referencia | Estado |
|---|---|---|---|---|
| `TSK-2.1-061` | Commit final en rama `feat/etapa-2-1`. Stagear todos los archivos de `web/` (excluir `web/node_modules/`, `web/.next/`, archivos de entorno). Mensaje en español: `feat: mockup interactivo etapa 2.1 — 4 vistas, 6 JSON, 6 servicios, 11 componentes`. | `dev-frontend` | Plan B5-15 · CLAUDE.md §6 | ⬜ Pendiente |
| `TSK-2.1-062` | Presentar mockup al cliente y registrar aprobación. Verificar que `npm run dev` levanta sin errores. Recorrido de demostración: `/` → `/alertas` → `/inventarios` (demostrar filtros) → `/ventas` → activar dark mode. Si el cliente aprueba: registrar frase literal de aprobación y fecha en `PROJECT_handoff.md`. Si solicita cambios: registrar observaciones y evaluar si requieren CC. | `project-manager` | Plan B5-16 y B5-17 · SPEC §9 completo · [MET-01] · [OBJ-01] | ⬜ Pendiente |

---

## Mapa de Dependencias Resumido

```
TSK-2.1-001 a 008 (B0 — Entorno)
    └── TSK-2.1-009 (usr.types.ts)
        └── TSK-2.1-010 (gold.types.ts)
            └── TSK-2.1-011 (mock_sedes.json)
                └── TSK-2.1-012 (mock_productos.json)
                    ├── TSK-2.1-013 (mock_ventas.json)
                    ├── TSK-2.1-014 (mock_inventario.json)
                    │       └── TSK-2.1-015 (mock_gold.json)
                    │               └── TSK-2.1-016 (mock_alertas.json)
                    │                       └── TSK-2.1-017 (verificación coherencia)
                    │                               └── TSK-2.1-018 a 023 (servicios)
    └── TSK-2.1-024 (useTheme.ts)
        ├── TSK-2.1-025 (BannerPrototipo.tsx)
        ├── TSK-2.1-026 (ThemeToggle.tsx)
        │       └── TSK-2.1-027 (Header.tsx)
        ├── TSK-2.1-028 (Sidebar.tsx)
        ├── TSK-2.1-029 (globals.css)
        └── TSK-2.1-030 (layout.tsx) ← requiere 025–029
                └── TSK-2.1-031 (Gate B2)

[Gate B1: TSK-2.1-023] + [Gate B2: TSK-2.1-031]
    └── TSK-2.1-032 a 042 (B3 — Componentes)
        └── TSK-2.1-043 a 046 (B4 — Vistas)
            └── TSK-2.1-047 a 062 (B5 — Validación y Cierre)
```

---

## Tabla de Artefactos Generados

| Bloque | Tipo | Cantidad | Archivos / Artefactos |
|---|---|---|---|
| B0 | Config / Setup | 8 tareas | Rama Git, `web/`, `tsconfig.json`, dependencias, `tailwind.config.ts`, `.eslintrc.json`, carpetas, gate |
| B1 | Tipos TypeScript | 2 archivos | `usr.types.ts`, `gold.types.ts` |
| B1 | JSON de datos ficticios | 6 archivos | `mock_sedes`, `mock_productos`, `mock_ventas`, `mock_inventario`, `mock_gold`, `mock_alertas` |
| B1 | Servicios | 6 archivos | `sedes.service`, `productos.service`, `ventas.service`, `inventario.service`, `gold.service`, `alertas.service` |
| B2 | Hook custom | 1 archivo | `useTheme.ts` |
| B2 | Componentes de layout | 4 archivos | `BannerPrototipo.tsx`, `ThemeToggle.tsx`, `Header.tsx`, `Sidebar.tsx` |
| B2 | App base | 2 archivos | `globals.css`, `layout.tsx` |
| B3 | Componentes shared | 3 archivos | `KpiCard.tsx`, `TendenciaChart.tsx`, `TopSkuRiesgo.tsx` |
| B3 | Componentes alertas | 3 archivos | `SeveridadBadge.tsx`, `AlertaCard.tsx`, `AlertaList.tsx` |
| B3 | Componentes inventario | 3 archivos | `StockBadge.tsx`, `FiltrosInventario.tsx`, `TablaInventario.tsx` |
| B3 | Componentes ventas | 2 archivos | `GraficoVentasSedes.tsx`, `TablaResumenSedes.tsx` |
| B4 | Vistas (App Router) | 4 archivos | `page.tsx` (/), `alertas/page.tsx`, `inventarios/page.tsx`, `ventas/page.tsx` |
| B5 | Verificaciones y cierre | 17 tareas | Compilación, migracion-cero, funcional, banners, dark mode, datos, responsive, commit, demo cliente |
| **Total** | | **62 tareas** | **36 artefactos de código** |

---

*Documento generado con `/sdd-doc` (Modo D — Jefe de Proyecto). Para plan de ejecución ver `docs/plans/f02_01_plan.md`. Para criterios de aceptación técnicos ver `docs/specs/f02_01_spec.md §9`.*
*Trazabilidad: `CC_00002` (incorporación Mockup Interactivo) y `CC_00003` (reubicación como Etapa 2.1).*
