# Plan de Implementación — Mockup Interactivo (`f02_01`)

> **Trazabilidad:** Este documento traduce los requerimientos de `docs/reqs/f02_01_prd.md` y los contratos técnicos de `docs/specs/f02_01_spec.md` en una secuencia de ejecución ordenada y verificable.

**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Cliente:** Almacén MultiTodo
**Fase:** 2 — Ingeniería de Datos e Integración | **Etapa:** 2.1
**Versión:** 1.0
**Fecha:** 2026-03-25
**Estado:** ✅ Aprobado
**Documentos relacionados:** `docs/reqs/f02_01_prd.md` | `docs/specs/f02_01_spec.md` | `docs/tasks/f02_01_task.md`
**Trazabilidad upstream:** `CC_00002` | `CC_00003` | `docs/specs/f01_03_spec.md`

---

## 1. Estrategia de Implementación

### 1.1 Principio Rector

El mockup es un artefacto de validación, no de producción. La estrategia de construcción prioriza la **velocidad de validación con el cliente** por encima de la exhaustividad técnica, sin sacrificar el Principio de Migración Cero: todo lo que se construya en esta etapa debe ser reutilizable en Etapa 3.3 sin modificar componentes ni tipos.

### 1.2 Flujo de Capas (de abajo hacia arriba)

El plan sigue el orden natural de dependencias de la arquitectura de 4 capas definida en `SPEC §1`:

```
Capa 0 — Entorno (prerequisito)
    ↓
Capa 1 — Datos y Servicios (fundamentos)
    ↓
Capa 2 — Layout Base (shell navegable)
    ↓
Capa 3 — Componentes Reutilizables
    ↓
Capa 4 — Vistas (ensambla los componentes)
    ↓
Capa 5 — Validación y Cierre (gate de aprobación)
```

No se puede construir una vista sin sus componentes. No se puede construir un componente sin los servicios. No se puede construir un servicio sin los tipos y los JSON. Esta jerarquía es inviolable.

### 1.3 Rama de Trabajo

| Artefacto | Rama Git |
|---|---|
| Código del mockup (`web/`) | `feat/etapa-2-1` |
| Documentos SDD (`docs/`) | `main` |

La rama `feat/etapa-2-1` se crea en el Bloque 0 y es la única rama donde se commitea código. Los documentos SDD ya están en `main` y no se modifican durante la implementación salvo por CCs aprobados.

### 1.4 Reglas de Ejecución del Plan

1. **Prerequisito de avance entre bloques:** Cada bloque debe terminar con su verificación de salida antes de iniciar el siguiente. Una verificación fallida detiene el avance hasta resolverse.
2. **TypeScript correcto desde el primer archivo:** No se acepta `any` ni errores de compilación en ningún punto del desarrollo. `strict: true` es activo desde la instalación.
3. **Principio de Migración Cero en todo momento:** Si en algún punto de la implementación un componente importa directamente desde `@/data/`, la tarea se detiene y se corrige antes de continuar.
4. **Los JSON se construyen antes de los servicios:** Un servicio vacío que no puede testear su retorno no agrega valor. Los datos ficticios son el prerequisito de todos los servicios.
5. **Coherencia de datos es responsabilidad del Bloque 1:** Los cuatro JSON de datos brutos (`ventas`, `inventario`, `productos`, `sedes`) deben ser coherentes entre sí antes de construir `gold` y `alertas`. Los SKUs referenciados en `inventario` deben existir en `productos`. Los `id_sede` deben existir en `sedes`.

---

## 2. Bloques de Trabajo

### Bloque 0 — Preparación del Entorno

> **Propósito:** Dejar el entorno de desarrollo completamente funcional antes de escribir una sola línea de código de negocio. Este bloque se ejecuta una única vez al inicio de la etapa.
>
> **Verificación de salida (gate):** `npm run dev` levanta en `localhost:3000` sin errores en terminal ni en consola del navegador.

| ID | Tarea | Descripción | Prerequisito |
|---|---|---|---|
| B0-01 | Crear rama `feat/etapa-2-1` desde `main` | `git checkout main && git pull && git checkout -b feat/etapa-2-1` | — |
| B0-02 | Inicializar proyecto Next.js 14 en `web/` | `npx create-next-app@latest web --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"`. Confirmar App Router = Yes. | B0-01 |
| B0-03 | Verificar `tsconfig.json` con `strict: true` | Abrir `web/tsconfig.json` y confirmar que `"strict": true` está presente. Si no, agregarlo. | B0-02 |
| B0-04 | Instalar dependencias adicionales | Desde `web/`: `npm install recharts lucide-react`. Verificar que ambas aparecen en `package.json`. | B0-02 |
| B0-05 | Verificar configuración Tailwind `darkMode: 'class'` | Abrir `web/tailwind.config.ts` y confirmar `darkMode: 'class'`. Si no está, agregar la línea. | B0-02 |
| B0-06 | Configurar regla ESLint `no-restricted-imports` | Editar `web/.eslintrc.json` para agregar regla que prohíba `import` desde `@/data/` en cualquier archivo fuera de `@/services/`. Detalles en SPEC §2. | B0-02 |
| B0-07 | Crear estructura de carpetas vacías en `web/src/` | Crear: `types/`, `data/`, `services/`, `components/layout/`, `components/alertas/`, `components/inventario/`, `components/ventas/`, `components/shared/`. No crear archivos aún. | B0-02 |
| B0-08 | Verificar gate de salida del Bloque 0 | Ejecutar `npm run dev` desde `web/`. Confirmar que el servidor levanta en `localhost:3000` y la página de bienvenida Next.js carga sin errores en consola. | B0-03 a B0-07 |

**Criterio de avance:** B0-08 en verde. Si `npm run dev` falla, resolver antes de continuar con Bloque 1.

---

### Bloque 1 — Fundamentos: Tipos, Datos y Servicios

> **Propósito:** Construir la infraestructura de datos del mockup: contratos de tipos TypeScript, datos ficticios en JSON y la capa de servicios que los expone a los componentes. Es la capa más crítica porque define los contratos que el resto del código consume.
>
> **Verificación de salida (gate):** `npx tsc --noEmit` desde `web/` pasa sin errores. Todos los servicios retornan datos tipados correctamente al ser importados en un archivo de prueba temporal.
>
> **Orden de ejecución:** Las tareas B1-01 a B1-08 son secuenciales por dependencias de datos. Las tareas B1-09 a B1-14 (servicios) son secuenciales por dependencias de tipos.

#### 1.1 Tipos TypeScript

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B1-01 | Crear `usr.types.ts` | Interfaces `Venta`, `InventarioItem`, `Producto`, `Sede` espejando exactamente las columnas de `usr_ventas`, `usr_inventario`, `usr_productos`, `usr_sedes` de `docs/database/schema.sql`. Sin `created_at` ni `updated_at` (no son campos de negocio). Sin `any`. Ver definición exacta en SPEC §3. | B0-08 | `src/types/usr.types.ts` |
| B1-02 | Crear `gold.types.ts` | Tipos `ClaseABC`, `ClasificacionABC`, `MetricaInventario`, `TipoAlerta`, `SeveridadAlerta`, `Alerta`, `DatosGold`, `EstadoStock`. Función pura `getEstadoStock` va en `gold.service.ts`, no aquí — solo el tipo. Ver SPEC §4. | B1-01 | `src/types/gold.types.ts` |

#### 1.2 Datos Ficticios (JSON)

> Las tareas B1-03 a B1-08 deben construirse con coherencia interna. El orden es obligatorio: primero las tablas maestras (`sedes`, `productos`), luego las transaccionales (`ventas`, `inventario`) que referencian a las maestras, y finalmente los derivados (`gold`, `alertas`) que referencian a todos los anteriores.

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B1-03 | Crear `mock_sedes.json` | Array de exactamente 7 objetos `Sede`. Datos exactos: id_sede 1–7, ciudades Bogotá (×2), Medellín, Cali (×2), Cartagena, Cúcuta. Nombres de sede según tabla de SPEC §7.5. | B1-01 | `src/data/mock_sedes.json` |
| B1-04 | Crear `mock_productos.json` | Array de ~100 objetos `Producto`. Formato SKU: `MTD-XXXXX`. Mínimo 5 familias, 15 categorías, 30 subcategorías. Nombres de productos colombianos de abarrotes/consumo masivo (marcas genéricas). Revisar ejemplos de jerarquía en SPEC §7.4. | B1-03 | `src/data/mock_productos.json` |
| B1-05 | Crear `mock_ventas.json` | Array de mínimo 500 objetos `Venta`. Fechas en UTC, ventana 13:00–22:59. Rango: `2026-03-11` a `2026-03-24` (14 días: 7 período actual + 7 período anterior para variaciones). Los 7 `id_sede` deben tener ventas. Mínimo 80 SKUs distintos. `costo` presente en ~80%. Ver distribución detallada en SPEC §7.2. | B1-03, B1-04 | `src/data/mock_ventas.json` |
| B1-06 | Crear `mock_inventario.json` | Array de objetos `InventarioItem`. Cubre todos los combos sku×sede con ventas en el período. Exactamente 5 SKUs con `stock_fisico = 0`. Al menos 10 SKUs con `dias_cobertura < 3` (calculado manualmente para validar coherencia con `mock_gold.json`). Ver distribución en SPEC §7.3. | B1-03, B1-04 | `src/data/mock_inventario.json` |
| B1-07 | Crear `mock_gold.json` | Objeto `DatosGold` con dos arrays. `clasificacion_abc`: un registro por SKU, distribución 20/30/50 (A/B/C). `metricas_inventario`: un registro por combo sku×sede, `dias_cobertura` coherente con `mock_inventario.json` (los 5 SKUs con `stock_fisico = 0` tienen `dias_cobertura = 0`). Los SKUs con mayores ventas en `mock_ventas.json` son Clase A. | B1-04, B1-05, B1-06 | `src/data/mock_gold.json` |
| B1-08 | Crear `mock_alertas.json` | Array de exactamente 12 objetos `Alerta`, uno por código `ALT_*`. Los SKUs y `id_sede` referenciados deben existir en `mock_productos.json` y `mock_sedes.json`. Las alertas negativas de tipo `critico` son `ALT_NEG_004` (desabastecimiento) y al menos una instancia de `ALT_NEG_001`. Las positivas con `severidad: 'medio'` por convención. Ver tabla completa en SPEC §7.7. | B1-03 a B1-07 | `src/data/mock_alertas.json` |

**Verificación de coherencia inter-JSON (obligatoria antes de B1-09):**
- Todo `sku` en `mock_ventas.json` existe en `mock_productos.json`.
- Todo `sku` en `mock_inventario.json` existe en `mock_productos.json`.
- Todo `id_sede` en `mock_ventas.json` existe en `mock_sedes.json`.
- Todo `id_sede` en `mock_inventario.json` existe en `mock_sedes.json`.
- Los 5 SKUs con `stock_fisico = 0` en `mock_inventario.json` tienen `dias_cobertura = 0` en `mock_gold.json`.
- Los SKUs en `mock_alertas.json` (campo `sku`) existen en `mock_productos.json`.
- Los `id_sede` en `mock_alertas.json` (campo `id_sede`) existen en `mock_sedes.json`.

#### 1.3 Servicios

> Los servicios implementan el patrón definido en SPEC §5.1: importan JSON solo dentro del servicio y exponen funciones `async` tipadas. Los componentes NUNCA importan JSON directamente.

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B1-09 | Implementar `sedes.service.ts` | Funciones: `getSedes(): Promise<Sede[]>`, `getSedeById(id_sede: number): Promise<Sede \| null>`. Importa `mock_sedes.json`. Ver SPEC §5.5. | B1-01, B1-03 | `src/services/sedes.service.ts` |
| B1-10 | Implementar `productos.service.ts` | Funciones: `getProductos(): Promise<Producto[]>`, `getProductoBySku(sku): Promise<Producto \| null>`, `getProductosByCategoria(categoria): Promise<Producto[]>`. Ver SPEC §5.4. | B1-01, B1-04 | `src/services/productos.service.ts` |
| B1-11 | Implementar `ventas.service.ts` | Funciones: `getVentas()`, `getVentasPorSede(id_sede?)`, `getTendencia7d()`, `getResumenPorSede()`. Tipos auxiliares `TendenciaDia` y `ResumenSede` definidos en el mismo archivo (SPEC §5.8). `getTendencia7d()` agrupa por fecha los 7 días más recientes. `getResumenPorSede()` agrega por sede con variación vs período anterior y margen estimado. | B1-01, B1-05 | `src/services/ventas.service.ts` |
| B1-12 | Implementar `inventario.service.ts` | Funciones: `getInventario()`, `getInventarioPorSede(id_sede?)`, `getInventarioPorClase(clase)`, `getStockCritico()`. `getInventarioPorClase` requiere cruzar con `mock_gold.json` (clasificación ABC). Ver SPEC §5.3. | B1-01, B1-02, B1-06, B1-07 | `src/services/inventario.service.ts` |
| B1-13 | Implementar `gold.service.ts` | Funciones: `getClasificacionABC()`, `getClasePorSku(sku)`, `getMetricasInventario()`, `getMetricasBySku(sku)`. Función pura `getEstadoStock(dias_cobertura): EstadoStock` (sin async — clasificación determinística según umbrales de SPEC §4). Ver implementación exacta en SPEC §5.7. | B1-02, B1-07 | `src/services/gold.service.ts` |
| B1-14 | Implementar `alertas.service.ts` | Funciones: `getAlertas()`, `getAlertasNegativas()`, `getAlertasPositivas()`, `getAlertasCriticas()`, `contarPorSeveridad()`. Tipo auxiliar `ConteoSeveridad` en el mismo archivo. `getAlertas()` retorna negativas primero (ordenadas critico→alto→medio) luego positivas. Ver SPEC §5.6. | B1-02, B1-08 | `src/services/alertas.service.ts` |

**Criterio de avance:** `npx tsc --noEmit` desde `web/` pasa sin errores. Los 6 servicios existen y compilan. Ningún servicio tiene `any`. Ningún componente (aún no existen) importa desde `@/data/`.

---

### Bloque 2 — Layout Base: Shell del Dashboard

> **Propósito:** Construir el esqueleto navegable del dashboard: banner de prototipo, header, sidebar y root layout. Al finalizar este bloque, el desarrollador puede navegar entre rutas y ver el shell completo en modo claro y oscuro — sin contenido de datos aún.
>
> **Prerequisito de inicio:** Bloque 1 completado (`npx tsc --noEmit` en verde).
>
> **Verificación de salida (gate):** `npm run dev` muestra el shell completo (banner ámbar + header + sidebar + área de contenido vacía) en modo claro y oscuro. El toggle de modo cambia el tema de inmediato y la recarga mantiene la preferencia.

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B2-01 | Crear `useTheme.ts` | Hook custom que lee/escribe en `localStorage` la clave `theme`. Aplica y remueve la clase `dark` en `document.documentElement`. Expone `{ theme, toggleTheme }`. Comportamiento: al montar, lee `localStorage`; si no hay valor, usa preferencia del sistema (`prefers-color-scheme`). | B0-08 | `src/hooks/useTheme.ts` |
| B2-02 | Crear `BannerPrototipo.tsx` | Componente sin props. Barra de ancho completo, `fixed top-0 z-50`, fondo `bg-amber-400 dark:bg-amber-500`, texto `"PROTOTIPO — Datos ficticios para validación de diseño"` en `text-amber-900 font-semibold text-sm text-center`. Ver SPEC §8.1 y §12.1. | B0-08 | `src/components/layout/BannerPrototipo.tsx` |
| B2-03 | Crear `ThemeToggle.tsx` | Botón que invoca `toggleTheme()` del hook `useTheme`. Icono `Sun` (modo claro) o `Moon` (modo oscuro) de `lucide-react`, tamaño `w-4 h-4`. Clases: `p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800`. | B2-01 | `src/components/layout/ThemeToggle.tsx` |
| B2-04 | Crear `Header.tsx` | Barra superior del área de contenido. Contiene: nombre del dashboard (`"Dashboard MultiTodo"`, `font-semibold text-lg`), banner T-1 (`"Datos al cierre de: 24/03/2026"`, fondo `bg-blue-50 dark:bg-blue-950`, texto `text-blue-700 dark:text-blue-300`, `text-xs`), y `ThemeToggle` alineado a la derecha. Clases de contenedor: `bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-700 px-6 py-3`. | B2-03 | `src/components/layout/Header.tsx` |
| B2-05 | Crear `Sidebar.tsx` | Sidebar lateral fijo izquierdo, `w-56`, altura completa. Estructura: logo/nombre del proyecto en la parte superior, ítems de navegación agrupados por secciones etiquetadas (`ANÁLISIS`, `ALERTAS`), perfil de usuario al pie. Usa `lucide-react` iconos outline: `LayoutDashboard`, `BarChart2`, `Package`, `Bell`, `TrendingUp`. Estado activo/inactivo según la ruta actual (usar `usePathname` de Next.js). Dark mode completo. Ver especificación exacta de clases en SPEC §12.2. | B2-01 | `src/components/layout/Sidebar.tsx` |
| B2-06 | Crear `globals.css` | Directivas Tailwind (`@tailwind base`, `@tailwind components`, `@tailwind utilities`) + regla global `html { @apply bg-gray-50 dark:bg-gray-950 }`. Sin CSS custom adicional — solo Tailwind. | B0-05 | `src/app/globals.css` |
| B2-07 | Crear `layout.tsx` (root layout) | Root layout de Next.js App Router. Aplica fuente Inter via `next/font/google`. Importa `globals.css`. Monta `BannerPrototipo` fijo en el top. Monta `Sidebar` en el lateral izquierdo. Monta `Header` en la parte superior del área de contenido. El `{children}` ocupa el área de contenido (`ml-56 mt-[banner+header] bg-gray-50 dark:bg-gray-950 min-h-screen p-6`). La clase `dark` se gestiona en `document.documentElement` via `useTheme`. | B2-02 a B2-06 | `src/app/layout.tsx` |
| B2-08 | Verificar gate de salida del Bloque 2 | Ejecutar `npm run dev`. Verificar visualmente: (a) banner ámbar visible en la parte superior, (b) sidebar visible con ítems de navegación, (c) header visible con nombre y banner T-1 azul, (d) toggle Sun/Moon funcional, (e) al hacer clic en toggle, el fondo cambia entre claro y oscuro, (f) al recargar, el modo persiste. | B2-07 | — |

**Criterio de avance:** B2-08 aprobado visualmente. El shell es navegable y el dark mode funciona con persistencia. No hay errores de compilación.

**Nota de paralelismo:** Los Bloques 1 y 2 comparten el prerequisito B0-08 pero son independientes entre sí. En una sesión de trabajo con múltiples desarrolladores, se pueden avanzar en paralelo. Con un solo desarrollador, el orden recomendado es B1 primero (base de datos) y luego B2 (shell visual), porque B2-05 (Sidebar) usa `getSedes()` indirectamente en el futuro, pero para el shell básico no lo requiere aún.

---

### Bloque 3 — Componentes Reutilizables

> **Propósito:** Construir todos los componentes React que las vistas ensamblarán. Cada componente recibe datos ya procesados como props — nunca llama a servicios directamente. Los servicios son invocados únicamente desde las vistas (`app/`).
>
> **Prerequisito de inicio:** Bloques 1 y 2 completados.
>
> **Verificación de salida (gate):** `npx tsc --noEmit` pasa sin errores. Todos los componentes compilados correctamente con sus props tipadas. Ningún componente importa desde `@/data/`.

#### 3.1 Componentes Compartidos (`shared/`)

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B3-01 | Crear `KpiCard.tsx` | Tarjeta de KPI con props: `titulo: string`, `valor: string \| number`, `variacion?: number` (porcentaje, positivo/negativo), `tendencia?: 'up' \| 'down' \| 'neutral'`, `icono: React.ReactNode`. Fondo: `bg-white dark:bg-gray-900`, borde sutil, sombra ligera. Valor en `text-2xl font-bold`. Variación con color verde (positivo) o rojo (negativo) y flecha ↑↓. Dark mode completo. | B2-07 | `src/components/shared/KpiCard.tsx` |
| B3-02 | Crear `TendenciaChart.tsx` | Gráfico de área o barras de 7 días con Recharts (`AreaChart` o `BarChart`). Props: `datos: TendenciaDia[]` (tipo importado de `ventas.service.ts`). Colores dinámicos según modo claro/oscuro (usar `useTheme`). Ejes con fechas en formato `DD/MM`. Tooltip con monto en COP. `ResponsiveContainer` para ajuste automático. | B1-11, B2-01 | `src/components/shared/TendenciaChart.tsx` |
| B3-03 | Crear `TopSkuRiesgo.tsx` | Tabla compacta con los top 5 SKUs de menor `dias_cobertura`. Props: `items: Array<{ sku: string, nombre: string, dias_cobertura: number, id_sede: number, nombre_sede: string }>`. Columnas: SKU (monoespaciado), nombre (truncado), días cobertura (resaltado en rojo si < 3), sede. Dark mode completo. | B2-07 | `src/components/shared/TopSkuRiesgo.tsx` |

#### 3.2 Componentes de Alertas (`alertas/`)

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B3-04 | Crear `SeveridadBadge.tsx` | Badge visual de severidad. Props: `severidad: SeveridadAlerta`. Colores: `critico` → `bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400`, `alto` → naranja, `medio` → amarillo. Texto en mayúsculas, `text-xs font-semibold`, `rounded-full px-2 py-0.5`. | B1-02 | `src/components/alertas/SeveridadBadge.tsx` |
| B3-05 | Crear `AlertaCard.tsx` | Tarjeta individual de alerta. Props: `alerta: Alerta`, `nombreSede: string \| null`. Muestra: código (monoespaciado, `text-xs`), `SeveridadBadge`, mensaje (texto completo), nombre de sede o `"Todas las sedes"` si `id_sede = null`, fecha en formato `DD/MM/YYYY`. Fondo blanco/gris oscuro, borde izquierdo de color según severidad. Dark mode. | B3-04, B1-02 | `src/components/alertas/AlertaCard.tsx` |
| B3-06 | Crear `AlertaList.tsx` | Lista contenedora de alertas. Props: `negativas: Alerta[]`, `positivas: Alerta[]`, `sedes: Sede[]`. Renderiza sección `"Alertas Activas"` con las negativas y sección `"Oportunidades del Día"` con las positivas. Usa `AlertaCard` para cada ítem, resolviendo el nombre de sede del `id_sede`. Ver layout de SPEC §6.2. | B3-05, B1-01 | `src/components/alertas/AlertaList.tsx` |

#### 3.3 Componentes de Inventario (`inventario/`)

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B3-07 | Crear `StockBadge.tsx` | Badge de estado de stock. Props: `estado: EstadoStock`. Colores según SPEC §6.3: `critico` → rojo, `bajo` → naranja, `normal` → amarillo, `optimo` → verde. Misma estructura visual que `SeveridadBadge`. | B1-02 | `src/components/inventario/StockBadge.tsx` |
| B3-08 | Crear `FiltrosInventario.tsx` | Dos dropdowns de filtro. Props: `sedes: Sede[]`, `sedeFiltro: number \| null`, `claseFiltro: ClaseABC \| null`, `onSedeCambio: (id: number \| null) => void`, `onClaseCambio: (clase: ClaseABC \| null) => void`. Opción "Todas las sedes" / "Todas las clases" como valor nulo. Estado gestionado en la vista padre — este componente es controlado. | B1-01, B1-02 | `src/components/inventario/FiltrosInventario.tsx` |
| B3-09 | Crear `TablaInventario.tsx` | Tabla filtrable. Props: `items: InventarioItem[]`, `productos: Producto[]`, `clasificaciones: ClasificacionABC[]`, `metricas: MetricaInventario[]`. Columnas según SPEC §6.3: SKU, nombre (join con `productos`), clase (join con `clasificaciones`), stock actual, días cobertura (1 decimal), `StockBadge`. Dark mode completo. Si no hay datos con los filtros activos, muestra mensaje vacío. | B3-07, B1-01, B1-02 | `src/components/inventario/TablaInventario.tsx` |

#### 3.4 Componentes de Ventas (`ventas/`)

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B3-10 | Crear `GraficoVentasSedes.tsx` | Gráfico de barras horizontal Recharts (`BarChart`). Props: `datos: ResumenSede[]`. Eje Y: nombres de sedes. Eje X: monto total de ventas (formato COP). Barras coloreadas por ranking (verde para top 1, naranja para última). `ResponsiveContainer`. Colores dinámicos con `useTheme`. | B1-11, B2-01 | `src/components/ventas/GraficoVentasSedes.tsx` |
| B3-11 | Crear `TablaResumenSedes.tsx` | Tabla de resumen por sede. Props: `datos: ResumenSede[]`. Columnas según SPEC §6.4: ranking (con ícono medalla para top 3), sede, ciudad, ventas período (COP con separador de miles), variación % (flecha ↑↓ con color), margen estimado %. Dark mode completo. | B1-11 | `src/components/ventas/TablaResumenSedes.tsx` |

**Criterio de avance:** `npx tsc --noEmit` en verde. 11 componentes creados. Ninguno importa desde `@/data/`. `npm run lint` no reporta errores de `no-restricted-imports`.

---

### Bloque 4 — Vistas

> **Propósito:** Ensamblar los componentes en las 4 vistas del dashboard. Las vistas son el único punto donde se llama a los servicios y se pasan los datos como props a los componentes.
>
> **Prerequisito de inicio:** Bloques 1, 2 y 3 completados.
>
> **Verificación de salida (gate):** Las 4 vistas cargan en el navegador con datos visibles y sin errores en consola. El Sidebar marca correctamente la vista activa.

| ID | Tarea | Descripción | Prerequisito | Archivo |
|---|---|---|---|---|
| B4-01 | Crear `page.tsx` (Resumen General — `/`) | Vista de inicio. Llama a: `getVentas()`, `getAlertasCriticas()`, `getSedes()`, `getClasificacionABC()`, `getInventario()`, `getMetricasInventario()`, `getTendencia7d()`, `contarPorSeveridad()`. Renderiza: 4 `KpiCard` (ventas totales, SKUs en alerta crítica, sedes activas, SKUs Clase A sin stock), `TendenciaChart`, `TopSkuRiesgo` (top 5 menor `dias_cobertura`), mini-panel de conteo de alertas con enlace a `/alertas`. Ver layout en SPEC §6.1. | B3-01, B3-02, B3-03, B1-11, B1-13, B1-14 | `src/app/page.tsx` |
| B4-02 | Crear `alertas/page.tsx` (Vista Alertas — `/alertas`) | Vista dedicada a alertas. Llama a: `getAlertasNegativas()`, `getAlertasPositivas()`, `getSedes()`. Renderiza: título de sección, `AlertaList` con las 12 alertas. | B3-06, B1-14, B1-09 | `src/app/alertas/page.tsx` |
| B4-03 | Crear `inventarios/page.tsx` (Vista Inventarios — `/inventarios`) | Vista operativa. Estado local React: `sedeFiltro: number \| null`, `claseFiltro: ClaseABC \| null`. Llama a: `getSedes()`, `getInventario()`, `getProductos()`, `getClasificacionABC()`, `getMetricasInventario()`. Aplica filtros en el cliente (sin nueva llamada al servicio). Renderiza: `FiltrosInventario`, `TablaInventario` con datos filtrados. | B3-08, B3-09, B1-09 a B1-13 | `src/app/inventarios/page.tsx` |
| B4-04 | Crear `ventas/page.tsx` (Vista Ventas — `/ventas`) | Vista estratégica. Llama a: `getResumenPorSede()`, `getSedes()`. Renderiza: título de sección, `GraficoVentasSedes`, `TablaResumenSedes`. | B3-10, B3-11, B1-09, B1-11 | `src/app/ventas/page.tsx` |

**Criterio de avance:** Las 4 vistas cargan con datos. La navegación entre vistas no recarga la página. El sidebar muestra el ítem activo correctamente en cada vista.

---

### Bloque 5 — Validación y Cierre

> **Propósito:** Verificar que el mockup cumple todos los criterios de aceptación técnicos de SPEC §9 antes de presentarlo al cliente. Este bloque es el gate de cierre de la etapa — ninguna tarea es opcional.

#### 5.1 Verificación de Compilación y Calidad

| ID | Tarea | Descripción | Prerequisito |
|---|---|---|---|
| B5-01 | Verificar `npx tsc --noEmit` | Ejecutar desde `web/`. Debe pasar con 0 errores y 0 instancias de `any`. Corresponde a SPEC §9.1. | B4-04 |
| B5-02 | Verificar `npm run lint` | Ejecutar desde `web/`. Debe pasar sin errores de `no-restricted-imports`. Confirmar que ningún componente ni vista importa desde `@/data/`. Corresponde a SPEC §9.2. | B4-04 |
| B5-03 | Verificar `npm run build` | Ejecutar desde `web/`. Debe completar sin errores de TypeScript ni de Next.js. Corresponde a SPEC §9.1. | B5-01, B5-02 |

#### 5.2 Verificación de Principio de Migración Cero

| ID | Tarea | Descripción | Prerequisito |
|---|---|---|---|
| B5-04 | Auditar imports en `src/components/` | Revisar que ningún archivo en `src/components/` contiene `import ... from '@/data/mock_*.json'`. Corresponde a SPEC §9.2. | B5-02 |
| B5-05 | Auditar imports en `src/app/` | Revisar que ningún archivo en `src/app/` contiene `import ... from '@/data/mock_*.json'`. Corresponde a SPEC §9.2. | B5-02 |

#### 5.3 Verificación Funcional

| ID | Tarea | Descripción | Prerequisito |
|---|---|---|---|
| B5-06 | Probar las 4 vistas | Navegar a `/`, `/alertas`, `/inventarios`, `/ventas`. Verificar que cada vista carga datos sin errores en consola. Verificar que la navegación entre vistas no recarga la página (App Router). Corresponde a SPEC §9.3. | B5-03 |
| B5-07 | Probar filtros de Inventarios | En `/inventarios`: aplicar filtro por sede, verificar que la tabla se actualiza. Aplicar filtro por clase ABC, verificar. Aplicar ambos filtros simultáneamente, verificar acumulación. Corresponde a SPEC §9.4. | B5-06 |
| B5-08 | Verificar exactitud de alertas | En `/alertas`: contar que hay exactamente 6 alertas negativas y 6 positivas. Verificar que las negativas están ordenadas: `ALT_NEG_004` (critico) primero. Corresponde a SPEC §9.4. | B5-06 |
| B5-09 | Probar dark/light mode | Desde cualquier vista: clic en toggle → modo cambia de inmediato. Recargar la página → modo persiste. Revisar que sidebar, header, tarjetas KPI, tablas, gráficos, badges y banners son legibles en modo oscuro. Corresponde a SPEC §9.7. | B5-06 |
| B5-10 | Verificar banners | Confirmar que el banner ámbar (`"PROTOTIPO..."`) y el banner azul (`"Datos al cierre de: 24/03/2026"`) están visibles en las 4 vistas y no obstruyen el contenido. Corresponde a SPEC §9.5. | B5-06 |

#### 5.4 Verificación de Datos

| ID | Tarea | Descripción | Prerequisito |
|---|---|---|---|
| B5-11 | Verificar exactitud de datos maestros | Confirmar: `mock_sedes.json` tiene 7 registros, `mock_alertas.json` tiene 12 registros, distribución ABC ~20/30/50 en `mock_gold.json`. Corresponde a SPEC §9.6. | B5-06 |
| B5-12 | Verificar gráficos Recharts | Verificar que `TendenciaChart` en `/` y `GraficoVentasSedes` en `/ventas` renderizan correctamente (barras o áreas visibles, ejes con etiquetas). En modo oscuro los gráficos no presentan colores ilegibles. Corresponde a SPEC §9.4 y §9.7. | B5-06, B5-09 |

#### 5.5 Verificación de Rendimiento y Responsivo

| ID | Tarea | Descripción | Prerequisito |
|---|---|---|---|
| B5-13 | Verificar tiempo de carga | Abrir `localhost:3000` por primera vez tras `npm run dev`. En la pestaña Network de DevTools: verificar que el tiempo de carga total es menor a 2 segundos. Corresponde a SPEC §9.8 y `[MET-03]`. | B5-06 |
| B5-14 | Verificar responsive en 1366×768 | Usando DevTools, cambiar viewport a 1366×768. Navegar por las 4 vistas. Verificar que ninguna tabla o gráfico se corta o vuelve ilegible. Corresponde a SPEC §9.8 y `[REQ-09]`. | B5-06 |

#### 5.6 Cierre y Entrega

| ID | Tarea | Descripción | Prerequisito |
|---|---|---|---|
| B5-15 | Commit en rama `feat/etapa-2-1` | Stagear todos los archivos de `web/`. Excluir: `web/node_modules/`, `web/.next/`, archivos de entorno. Commit con mensaje descriptivo en español: `feat: mockup interactivo etapa 2.1 — 4 vistas, 6 JSON, 6 servicios, 11 componentes`. | B5-01 a B5-14 |
| B5-16 | Preparar demo para sesión de validación | Verificar que `npm run dev` levanta sin errores en el ambiente del desarrollador. Preparar recorrido de demostración: iniciar en `/` (Resumen General), navegar a `/alertas` (mostrar las 12 alertas), navegar a `/inventarios` (demostrar filtros), navegar a `/ventas` (mostrar gráfico y tabla comparativa). Activar dark mode al final. | B5-15 |
| B5-17 | Presentar mockup al cliente y registrar aprobación | Ejecutar sesión de validación. Si el cliente aprueba: registrar aprobación en `PROJECT_handoff.md` con frase literal de aprobación y fecha. Si el cliente solicita cambios: registrar observaciones, evaluar si requieren CC y proceder según el flujo de CC de CLAUDE.md §1. Corresponde a `[MET-01]`. | B5-16 |

**Criterio de avance de etapa:** B5-17 con aprobación registrada. Sin aprobación del cliente, la etapa no se cierra aunque todos los criterios técnicos pasen.

---

## 3. Mapa de Dependencias

```
B0 (Entorno)
└── B1-01 (usr.types.ts)
    └── B1-02 (gold.types.ts)
        └── B1-03 (mock_sedes.json)
            └── B1-04 (mock_productos.json)
                └── B1-05 (mock_ventas.json) ───────────────────┐
                └── B1-06 (mock_inventario.json) ─────────────┐ │
                    └── B1-07 (mock_gold.json) ─────────────┐ │ │
                        └── B1-08 (mock_alertas.json) ────┐ │ │ │
                            └── B1-09 (sedes.service)     │ │ │ │
                            └── B1-10 (productos.service) │ │ │ │
                            └── B1-11 (ventas.service) ───┘ │ │ │
                            └── B1-12 (inventario.service) ─┘ │ │
                            └── B1-13 (gold.service) ─────────┘ │
                            └── B1-14 (alertas.service) ────────┘

B0 (Entorno) → B2-01 (useTheme)
    └── B2-02 (BannerPrototipo)
    └── B2-03 (ThemeToggle)
        └── B2-04 (Header)
    └── B2-05 (Sidebar)
    └── B2-06 (globals.css)
    └── B2-07 (layout.tsx) ← requiere B2-02..B2-06
        └── [gate B2]

[gate B1] + [gate B2]
└── B3 (Componentes — 11 archivos)
    └── B4 (Vistas — 4 archivos)
        └── B5 (Validación — 17 verificaciones)
```

---

## 4. Tabla de Artefactos

| Bloque | Tipo | Cantidad | Artefactos |
|---|---|---|---|
| B0 | Config/Setup | 8 tareas | Rama Git, proyecto Next.js, tsconfig, dependencias, Tailwind, ESLint, carpetas, verificación |
| B1 | Tipos | 2 archivos | `usr.types.ts`, `gold.types.ts` |
| B1 | JSON | 6 archivos | `mock_sedes`, `mock_productos`, `mock_ventas`, `mock_inventario`, `mock_gold`, `mock_alertas` |
| B1 | Servicios | 6 archivos | `sedes`, `productos`, `ventas`, `inventario`, `gold`, `alertas` |
| B2 | Hook | 1 archivo | `useTheme.ts` |
| B2 | Componentes Layout | 4 archivos | `BannerPrototipo`, `ThemeToggle`, `Header`, `Sidebar` |
| B2 | App | 2 archivos | `globals.css`, `layout.tsx` |
| B3 | Componentes Shared | 3 archivos | `KpiCard`, `TendenciaChart`, `TopSkuRiesgo` |
| B3 | Componentes Alertas | 3 archivos | `SeveridadBadge`, `AlertaCard`, `AlertaList` |
| B3 | Componentes Inventario | 3 archivos | `StockBadge`, `FiltrosInventario`, `TablaInventario` |
| B3 | Componentes Ventas | 2 archivos | `GraficoVentasSedes`, `TablaResumenSedes` |
| B4 | Vistas | 4 archivos | `/`, `/alertas`, `/inventarios`, `/ventas` |
| B5 | Verificaciones | 17 tareas | Compilación, calidad, funcional, datos, rendimiento, responsivo, cierre |
| **Total** | | **~47 artefactos** | |

---

## 5. Protocolo ante Bloqueadores

| Bloqueador | Protocolo de resolución |
|---|---|
| `npm install` falla por conflictos de versión en `recharts` + Next.js 14 | Probar `recharts@^2.x` explícito. Si persiste: revisar compatibilidad con React 18. No usar alternativas (Chart.js, nivo) sin CC aprobado. |
| `npx tsc --noEmit` falla por error en un tipo | Corregir el tipo antes de continuar. Prohibido usar `any` como solución provisional. |
| Un componente requiere datos que no existen en ningún servicio | DETENER. Evaluar si el servicio faltante está en la SPEC. Si está en la SPEC, implementarlo antes de continuar. Si no está, abrir CC. |
| Los datos ficticios no son coherentes (SKU en alertas no existe en productos) | Volver a B1-08 y corregir el JSON. La coherencia es prerequisito de los servicios. |
| El cliente solicita cambios estructurales durante la demo (nueva vista, nueva métrica no planificada) | Registrar observación. Si el cambio es menor (texto, color): ajustar en mockup. Si el cambio es estructural: abrir CC antes de implementar. |
| `npm run dev` tiene errores de hidratación en SSR | Verificar que los componentes que usan `localStorage` (useTheme) tienen `'use client'` y están protegidos con `mounted` state para evitar mismatch de hidratación. |

---

## 6. Criterios de Definición de "Hecho" (DoD)

La Etapa 2.1 se considera completada cuando:

1. Los 17 criterios de aceptación técnicos de SPEC §9 pasan en verde.
2. `npx tsc --noEmit` sin errores, cero `any`, cero violaciones de `no-restricted-imports`.
3. Las 4 vistas son navegables con datos de los JSON ficticios.
4. El dark mode funciona y persiste en recarga.
5. Los filtros de Inventarios son acumulables.
6. El cliente aprueba el mockup explícitamente en sesión de validación.
7. La aprobación está registrada en `PROJECT_handoff.md`.
8. El código está commiteado en `feat/etapa-2-1`.
9. `docs/executives/f02_01_executive.md` generado (prerequisito para Etapa 2.2).

---

*Documento generado con `/sdd-doc` (Modo C — Arquitecto de Ejecución). Siguiente documento: `docs/tasks/f02_01_task.md`.*
*Origen: `CC_00002` (incorporación de Mockup Interactivo) y `CC_00003` (reubicación como Etapa 2.1).*
