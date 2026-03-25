# Sistema Visual — prototype-ui-ux

Guía de diseño visual para prototipos. Aplica a cualquier proyecto que use este skill.
Los valores específicos (nombres de secciones del sidebar, KPIs del home, etc.) se obtienen
de la SPEC del proyecto activo.

---

## 1. Layout General

El patrón estándar es **sidebar fijo + área de contenido**:

```
┌──────────────────────────────────────────────────────────────┐
│ BANNER PROTOTIPO (sticky top, ámbar, z-50)                   │
├──────────────┬───────────────────────────────────────────────┤
│              │ HEADER (nombre app + banner T-1 / subtítulo)  │
│   SIDEBAR    ├───────────────────────────────────────────────┤
│   w-56       │                                               │
│   fixed      │   ÁREA DE CONTENIDO (bg-gray-50)              │
│   left-0     │   ml-56, padding top = altura header          │
│   h-full     │                                               │
└──────────────┴───────────────────────────────────────────────┘
```

**Clases base de cada zona (claro + oscuro):**

| Zona | Clases Tailwind |
|---|---|
| Banner prototipo | `fixed top-0 w-full z-50 bg-amber-400 dark:bg-amber-500 text-amber-900 font-semibold text-sm text-center py-1` |
| Sidebar | `fixed left-0 top-0 h-full w-56 bg-white dark:bg-gray-900 border-r border-gray-100 dark:border-gray-700 flex flex-col pt-[banner-height]` |
| Header | `bg-white dark:bg-gray-900 border-b border-gray-100 dark:border-gray-700 px-6 py-4 ml-56` |
| Área de contenido | `ml-56 bg-gray-50 dark:bg-gray-950 min-h-screen p-6 pt-[header-height]` |

---

## 2. Sidebar con Secciones Etiquetadas

El sidebar sigue el patrón de **menú principal + submenús bajo etiquetas de sección**,
inspirado en dashboards de gestión empresarial modernos.

### Estructura del componente

```tsx
// Sidebar.tsx — estructura lógica
<aside className="sidebar-base">
  {/* Logo / nombre del proyecto */}
  <div className="logo-zone">
    <span className="text-sm font-semibold text-gray-900 dark:text-gray-50">Nombre App</span>
    <span className="text-xs text-gray-400">subtítulo</span>
  </div>

  <nav className="flex-1 px-3 py-4 space-y-1">
    {/* Items sin sección */}
    <NavItem href="/" icon={LayoutDashboard} label="Dashboard" />

    {/* Sección etiquetada */}
    <SectionLabel label="ANÁLISIS" />
    <NavItem href="/ventas" icon={BarChart2} label="Ventas" />
    <NavItem href="/inventarios" icon={Package} label="Inventarios" />

    <SectionLabel label="ALERTAS" />
    <NavItem href="/alertas" icon={Bell} label="Alertas Activas" />
  </nav>

  {/* Perfil al pie */}
  <div className="profile-zone border-t border-gray-100 dark:border-gray-700 p-3">
    <Avatar initials="AM" />
    <div>
      <p className="text-sm font-medium text-gray-900 dark:text-gray-50">Nombre Cliente</p>
      <p className="text-xs text-gray-400">subtítulo rol</p>
    </div>
  </div>
</aside>
```

### Clases por estado de NavItem

| Estado | Clases |
|---|---|
| Activo | `bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 font-medium` |
| Inactivo | `text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800` |
| Base (ambos) | `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors w-full` |

### Etiqueta de sección (SectionLabel)

```tsx
<p className="text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500 px-3 mt-4 mb-1">
  {label}
</p>
```

**Clave:** las etiquetas de sección del sidebar y los labels de KPI usan el mismo estilo
`text-xs uppercase tracking-wider` — esto crea coherencia visual entre el sidebar y el
contenido principal.

### Detectar ruta activa

Usar `usePathname()` de `next/navigation`:
```tsx
const pathname = usePathname()
const isActive = pathname === href || (href !== '/' && pathname.startsWith(href))
```

---

## 3. Paleta de Colores — Tokens Duales

Cada token tiene variante para modo claro y modo oscuro. Nunca usar un color sin su `dark:`.

| Token | Modo Claro | Modo Oscuro | Uso principal |
|---|---|---|---|
| Primary | `green-600` | `green-500` | Acento, ítem activo, botones |
| Primary light | `green-50` | `green-900/30` | Fondo ítem activo sidebar |
| Background | `gray-50` | `gray-950` | Área de contenido |
| Surface | `white` | `gray-900` | Tarjetas, sidebar, header |
| Surface elevated | `gray-100` | `gray-800` | Fondos de tabla, inputs |
| Border | `gray-100` | `gray-700` | Bordes de tarjetas y separadores |
| Text primary | `gray-900` | `gray-50` | Títulos, valores KPI |
| Text secondary | `gray-500` | `gray-400` | Labels, metadatos |
| Text muted | `gray-400` | `gray-500` | Etiquetas de sección, texto terciario |
| Danger | `red-600` | `red-400` | Alertas críticas |
| Warning | `orange-500` | `orange-400` | Alertas alto |
| Caution | `yellow-500` | `yellow-400` | Alertas medio |
| Success | `green-500` | `green-400` | Alertas positivas, stock óptimo |
| Info | `blue-600` | `blue-400` | Información neutral, banner T-1 |
| Prototype | `amber-400` | `amber-500` | Banner de prototipo |

---

## 4. Tipografía — Inter

**Configurar en `layout.tsx`:**
```typescript
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'] })
// Aplicar: <html lang="es" className={`${inter.className}`}>
```

**Escala tipográfica del proyecto:**

| Elemento | Clase Tailwind |
|---|---|
| Título principal de vista | `text-2xl font-semibold text-gray-900 dark:text-gray-50` |
| Subtítulo de vista | `text-sm text-gray-500 dark:text-gray-400` |
| **Label KPI** (encima del valor) | `text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400` |
| **Valor KPI** (número grande) | `text-2xl font-bold text-gray-900 dark:text-gray-50` |
| Tendencia positiva | `text-xs font-medium text-green-600 dark:text-green-400` |
| Tendencia negativa | `text-xs font-medium text-red-500 dark:text-red-400` |
| Ítem de menú | `text-sm` |
| **Etiqueta de sección sidebar** | `text-xs font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-500` |
| Encabezado columna tabla | `text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400` |
| Contenido celda tabla | `text-sm text-gray-700 dark:text-gray-300` |
| Texto auxiliar / fecha / ID | `text-xs text-gray-400 dark:text-gray-500` |

---

## 5. KPI Cards (`KpiCard.tsx`)

Estructura visual de una tarjeta de KPI:

```
┌─────────────────────────────────┐
│ LABEL KPI               [ícono] │  ← text-xs uppercase tracking-wider gray-500
│                                 │
│ Valor Principal                 │  ← text-2xl font-bold gray-900
│ ↑ 8.3% vs período anterior      │  ← text-xs green-600 o red-500
└─────────────────────────────────┘
```

**Props interface:**
```typescript
interface KpiCardProps {
  titulo: string                          // label uppercase
  valor: string                           // ya formateado: "COP 4.2M", "7", "3 SKUs"
  variacion?: string                      // ej: "+8.3%" o "-2.1%"
  tendencia?: 'up' | 'down' | 'neutral'
  icono: React.ReactNode                  // componente Lucide
}
```

**Clases del card:**
```
bg-white dark:bg-gray-900
border border-gray-100 dark:border-gray-700
rounded-xl p-5 shadow-sm
```

---

## 6. Gráficos con Recharts

Recharts no lee clases Tailwind — los colores se pasan como props. Usar el hook `useTheme`
para calcular la paleta dinámica.

**Patrón estándar:**
```typescript
const { isDark } = useTheme()

const chartColors = {
  primary:  isDark ? '#22c55e' : '#16a34a',   // green-400 / green-600
  grid:     isDark ? '#374151' : '#e5e7eb',   // gray-700 / gray-200
  text:     isDark ? '#9ca3af' : '#6b7280',   // gray-400 / gray-500
  tooltip:  isDark ? '#1f2937' : '#ffffff',   // gray-800 / white
  area:     isDark ? '#16a34a33' : '#16a34a1a', // verde ~20% opacidad
}
```

**AreaChart (tendencia temporal):**
- Área rellena con gradiente: color primario al 20% de opacidad
- Línea sólida: color primario al 100%
- Grid horizontal con `chartColors.grid`
- Eje X e Y con `chartColors.text`

**BarChart (comparativo por categoría/sede):**
- Barras verticales con `chartColors.primary`
- Sin border-radius excesivo — `radius={[4, 4, 0, 0]}`
- Tooltip con fondo `chartColors.tooltip`

---

## 7. Dark Mode — Hook `useTheme`

**`src/hooks/useTheme.ts`:**
```typescript
import { useState, useEffect } from 'react'

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

**`ThemeToggle.tsx` — botón en el header:**
```tsx
import { Sun, Moon } from 'lucide-react'
import { useTheme } from '@/hooks/useTheme'

export function ThemeToggle() {
  const { isDark, toggle } = useTheme()
  return (
    <button
      onClick={toggle}
      className="p-2 rounded-full text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
      aria-label="Cambiar modo de color"
    >
      {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
    </button>
  )
}
```

**Regla:** `ThemeToggle` vive en el `Header`. El `Sidebar` también puede consumir `useTheme`
para pasar `isDark` a los gráficos que estén en vistas. Las vistas obtienen `isDark` directamente.

---

## 8. Íconos — Guía rápida Lucide

Todos los íconos son de `lucide-react`, estilo **outline** (por defecto), tamaño `w-4 h-4`
en sidebar y `w-5 h-5` en KPI cards y encabezados.

| Uso típico | Ícono Lucide |
|---|---|
| Dashboard / Home | `LayoutDashboard` |
| Alertas / Notificaciones | `Bell` |
| Inventario / Productos | `Package` |
| Ventas / Gráficos | `BarChart2` |
| Tendencia positiva | `TrendingUp` |
| Tendencia negativa | `TrendingDown` |
| Usuarios / Clientes | `Users` |
| Configuración | `Settings` |
| Modo oscuro | `Moon` |
| Modo claro | `Sun` |
| Filtros | `Filter` |
| Exportar | `Download` |
| Ver más | `ChevronRight` |
| Crítico / Error | `AlertCircle` |
| Éxito | `CheckCircle2` |
