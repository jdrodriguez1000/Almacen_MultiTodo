---
name: prototype-ui-ux
description: >
  Construye prototipos/mockups interactivos navegables con Next.js 14 + TypeScript strict +
  Tailwind CSS + datos ficticios JSON. Cubre el ciclo completo: generación de mock data,
  Service Layer (Principio de Migración Cero), componentes React, vistas navegables,
  dark/light mode y validación final contra criterios de aceptación.

  Usar SIEMPRE que el usuario pida: construir un mockup o prototipo, implementar un bloque
  de prototipado ("Bloque 0", "Bloque 1"...), ejecutar tareas de frontend ("TSK-X-XXX a
  TSK-X-XXX"), crear componentes React con datos ficticios, o cualquier trabajo de UI/UX
  sobre un prototipo navegable. También disparar ante: "crea el componente", "implementa
  la vista", "genera el JSON de datos", "construye el sidebar", "agrega dark mode".

  NO usar para código que conecte a bases de datos reales, APIs externas, lógica de negocio
  de producción ni pipelines de datos. Este skill es exclusivamente de prototipado.
---

# prototype-ui-ux — Skill de Prototipado Interactivo

## 1. Por qué existe este skill

Un prototipo bien construido permite que el cliente apruebe el diseño **antes** de invertir en
backend, pipelines y lógica de producción. El riesgo que evita: descubrir que el layout o la
información mostrada no sirven cuando ya están integrados con datos reales.

El principio central es la **Migración Cero**: el Service Layer es la única barrera entre los
datos ficticios de hoy y Supabase de mañana. Todo lo que esté por encima — componentes, vistas,
tipos TypeScript — no cambia al conectar la base de datos real. Construir con esto en mente desde
el inicio hace que el prototipo sea directamente la base del producto final.

---

## 2. Leer los documentos SDD antes de escribir código

Antes de tocar un archivo, leer en este orden:

1. `docs/tasks/f[F]_[E]_task.md` — identificar qué tareas específicas ejecutar
2. `docs/specs/f[F]_[E]_spec.md` — arquitectura, tipos, contratos de servicio y sistema visual
3. `docs/reqs/f[F]_[E]_prd.md` — requerimientos funcionales y datos esperados
4. `docs/plans/f[F]_[E]_plan.md` — orden y dependencias entre bloques

Si el usuario pide "Bloque X", buscar ese bloque en el plan y extraer las tareas correspondientes
del task document. Si pide "TSK-X-X-XXX a TSK-X-X-XXX", leer cada tarea en el task document y
ejecutarlas en secuencia respetando las dependencias.

---

## 3. Cómo interpretar la solicitud

### "Construye el Bloque N"
1. Leer el plan para identificar qué tareas componen ese bloque
2. Leer cada tarea en el task document
3. Verificar que las dependencias del bloque anterior estén satisfechas
4. Ejecutar las tareas en el orden definido
5. Al terminar, verificar el gate de salida del bloque (indicado en el plan)

### "Implementa TSK-X-X-XXX a TSK-X-X-XXX"
1. Leer el task document y extraer esas tareas específicas
2. Verificar que no hay dependencias no satisfechas
3. Ejecutar cada tarea en secuencia
4. Reportar al usuario qué se completó y qué sigue

### Solicitud libre ("crea el sidebar", "genera el mock de ventas")
1. Identificar a qué tarea del task document corresponde
2. Leer la SPEC para encontrar la especificación técnica de ese artefacto
3. Construirlo siguiendo las reglas de este skill
4. Confirmar que no viola ninguna de las Reglas de Oro (§4)

---

## 4. Reglas de Oro (no negociables)

Estas reglas protegen el Principio de Migración Cero. Violarlas hace que el prototipo
sea difícil de migrar a producción:

**RG-01 — Separación de capas:**
Ningún componente React ni vista puede importar directamente desde `src/data/mock_*.json`.
Todo dato llega a través de funciones del Service Layer (`src/services/`).
Verificar con ESLint `no-restricted-imports` — debe estar configurado desde el Bloque 0.

**RG-02 — TypeScript strict, cero `any`:**
`tsconfig.json` debe tener `strict: true`. No usar `any` en ningún archivo de `src/`.
Correr `npx tsc --noEmit` antes de reportar una tarea como completada.

**RG-03 — Dark mode en cada componente:**
Cada clase Tailwind que define color, fondo o borde debe tener su variante `dark:`.
No existe componente "pendiente de dark mode para después" — se hace en el mismo momento.

**RG-04 — Mock data espeja esquemas reales:**
Los JSON de datos ficticios usan exactamente los mismos nombres de campo y tipos que las
tablas de la base de datos real. Sin campos inventados en los archivos que espejean `usr_*`.
Los campos derivados (métricas Gold) van en un JSON separado.

**RG-05 — Íconos outline únicamente:**
Usar `lucide-react` para todos los íconos. Estilo outline (por defecto en Lucide). No mezclar
con otras librerías de íconos (heroicons, react-icons, etc.) en el mismo proyecto.

**RG-06 — Sin lógica de negocio en componentes:**
Los componentes reciben props tipadas y renderizan. Las transformaciones, filtros y cálculos
viven en los servicios o en funciones auxiliares de los servicios. Un componente que hace
`ventas.filter(...).reduce(...)` directamente está violando esta regla.

---

## 5. Fases de construcción (orden obligatorio)

Las fases siguen las dependencias naturales del código. Saltarse el orden genera errores
de TypeScript en cascada.

```
Fase 1 — Entorno      → proyecto Next.js configurado, dependencias, ESLint
Fase 2 — Contratos    → tipos TypeScript (usr.types.ts, gold.types.ts)
Fase 3 — Datos        → JSON de mock data en el orden correcto (maestros → transaccionales → derivados)
Fase 4 — Servicios    → Service Layer (la única capa que importa JSON)
Fase 5 — Layout       → hook useTheme, BannerPrototipo, Header, ThemeToggle, Sidebar, layout.tsx
Fase 6 — Componentes  → shared → alertas → inventario → ventas (en ese orden)
Fase 7 — Vistas       → ensamblar componentes en páginas App Router
Fase 8 — Validación   → criterios de aceptación, tsc, lint, build, demo
```

Ver `references/data-architecture.md` para el detalle de Fases 2-4.
Ver `references/visual-system.md` para el detalle de Fases 5-6.
Ver `references/checklist.md` para el detalle de Fase 8.

---

## 6. Stack exacto del prototipo

| Tecnología | Versión | Configuración clave |
|---|---|---|
| Next.js | 14+ App Router | Sin `src/pages/` — solo `src/app/` |
| TypeScript | 5+ | `strict: true`, path alias `@/*` → `./src/*` |
| Tailwind CSS | 3+ | `darkMode: 'class'` obligatorio |
| `lucide-react` | latest | Íconos outline para toda la UI |
| `recharts` | 2+ | Gráficos con colores dinámicos (no hardcodeados) |
| `next/font/google` | built-in | Fuente Inter — no instalar nada extra |

**Dependencias `package.json`:**
```json
"recharts": "^2.x",
"lucide-react": "^0.x"
```
`next/font/google` viene incluido en Next.js — no instalar por separado.

---

## 7. Estructura de carpetas del prototipo

```
web/
└── src/
    ├── app/                    # App Router — vistas
    │   ├── layout.tsx          # Root layout: fuente, banners, sidebar, área de contenido
    │   ├── page.tsx            # Vista principal (Resumen / Home)
    │   └── globals.css         # Tailwind directives + dark background en html
    ├── components/
    │   ├── layout/             # Header, Sidebar, BannerPrototipo, ThemeToggle
    │   └── shared/             # KpiCard, gráficos, tablas genéricas
    ├── services/               # ÚNICA capa que importa de data/
    ├── types/                  # usr.types.ts + gold.types.ts
    ├── data/                   # mock_*.json — solo accesibles desde services/
    └── hooks/                  # useTheme.ts
```

Cada proyecto añade subcarpetas bajo `components/` según sus dominios de negocio
(ej: `alertas/`, `inventario/`, `ventas/`). La estructura base siempre es la misma.

---

## 8. Configuración inicial obligatoria (Bloque 0)

Al inicializar el proyecto, estos tres archivos deben quedar configurados antes de escribir
cualquier componente:

**`tailwind.config.ts` — dark mode por clase:**
```typescript
import type { Config } from 'tailwindcss'
const config: Config = {
  darkMode: 'class',
  content: ['./src/**/*.{ts,tsx}'],
  theme: { extend: {} },
  plugins: [],
}
export default config
```

**`src/app/globals.css` — fondo oscuro en html:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    @apply bg-gray-50 dark:bg-gray-950;
  }
}
```

**`.eslintrc.json` — proteger la separación de capas:**
```json
{
  "extends": "next/core-web-vitals",
  "rules": {
    "no-restricted-imports": ["error", {
      "patterns": [{
        "group": ["@/data/*", "../data/*", "./data/*"],
        "message": "Importar datos solo desde src/services/. Los componentes no acceden a mock data directamente."
      }]
    }]
  }
}
```

---

## 9. Referencias detalladas

Leer los archivos de referencia cuando se necesite detalle específico:

| Archivo | Cuándo leerlo |
|---|---|
| `references/visual-system.md` | Al construir Sidebar, Header, KpiCard, gráficos o cualquier componente visual |
| `references/data-architecture.md` | Al crear tipos TypeScript, JSON de mock data o servicios |
| `references/checklist.md` | Al ejecutar la fase de validación (Bloque 5 o equivalente) |
