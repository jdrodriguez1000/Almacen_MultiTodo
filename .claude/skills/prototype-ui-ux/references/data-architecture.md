# Arquitectura de Datos — prototype-ui-ux

Guía para construir el Service Layer, los tipos TypeScript y los archivos de mock data.

---

## 1. El Principio de Migración Cero

La razón de esta arquitectura es simple: el prototipo debe poder convertirse en el producto
final cambiando **solo la implementación interna de los servicios**. Si cada componente
importa datos directamente, migrar a producción requeriría modificar decenas de archivos.
Con el Service Layer como barrera única, es un cambio quirúrgico.

```
MOCKUP:       mock_*.json  →  services/  →  components/  →  views/
PRODUCCIÓN:   Supabase     →  services/  →  components/  →  views/
                                  ↑
                          Solo esto cambia
```

**Verificación:** Si `npm run lint` pasa sin errores con la regla `no-restricted-imports`
configurada, la separación está garantizada.

---

## 2. Tipos TypeScript — Dos archivos, dos propósitos

### `src/types/usr.types.ts`
Contiene interfaces que espejean **exactamente** las tablas de la base de datos real del cliente.
Mismos nombres de campo, mismos tipos. Si la BD tiene `fecha_hora: timestamp with time zone`,
aquí es `fecha_hora: string` (ISO 8601). Si tiene `costo: numeric(10,2) NULL`, aquí es
`costo: number | null`.

**Equivalencia PostgreSQL → TypeScript:**

| PostgreSQL | TypeScript |
|---|---|
| `bigserial` / `serial` / `integer` | `number` |
| `text` | `string` |
| `numeric(10, 2)` | `number` |
| `timestamp with time zone` | `string` (ISO 8601 UTC) |
| `NULL` permitido | `\| null` |
| `boolean` | `boolean` |

**Patrón del archivo:**
```typescript
// IMPORTANTE: Mantener sincronizado con el DDL de la base de datos.
// Cambios en el esquema requieren aprobación antes de modificar este archivo.

// Espeja tabla: [nombre_tabla]
export interface NombreEntidad {
  campo_pk: number           // tipo PK + comentario de constraint
  campo_fk: string           // FK -> tabla_referenciada.campo
  campo_valor: number        // constraint si aplica (> 0, >= 0)
  campo_nullable: number | null
}
```

### `src/types/gold.types.ts`
Contiene tipos para datos **derivados** que en producción vendrán de la capa Gold de la BD
(`tss_gold_*` en el caso de MultiTodo, o equivalente en otro proyecto). Estos campos NO existen
en las tablas del cliente — son métricas calculadas por el pipeline.

Incluye también los tipos para alertas y estados visuales.

**Tipos comunes en dashboards de este tipo:**
```typescript
export type ClaseABC = 'A' | 'B' | 'C'
export type EstadoStock = 'critico' | 'bajo' | 'normal' | 'optimo'
export type SeveridadAlerta = 'critico' | 'alto' | 'medio'
export type TipoAlerta = 'negativa' | 'positiva'

export interface ClasificacionABC {
  sku: string       // o el identificador de producto del proyecto
  clase_abc: ClaseABC
}

export interface Alerta {
  codigo: string
  tipo: TipoAlerta
  severidad: SeveridadAlerta
  // campos específicos del dominio del proyecto
  mensaje: string
  fecha_calculo: string  // ISO 8601
}
```

---

## 3. Mock Data — Reglas de construcción

### Regla fundamental
Los JSON que espejean tablas del cliente (`usr_*` o equivalente) deben tener exactamente
los mismos campos que esas tablas. Sin campos adicionales, sin renombres convenientes.

Los datos derivados (métricas Gold, clasificaciones) van en un JSON separado.

### Orden de creación (dependencias)
```
1. mock_[entidad_maestra_1].json  ← sin dependencias (ej: sedes, categorías)
2. mock_[entidad_maestra_2].json  ← sin dependencias (ej: productos, SKUs)
3. mock_[transacciones].json      ← referencia maestros (ej: ventas, movimientos)
4. mock_[stock_estado].json       ← referencia maestros (ej: inventario, stock)
5. mock_[gold_derivados].json     ← coherente con transacciones y stock
6. mock_[alertas].json            ← referencia entidades de los JSON anteriores
```

### Coherencia obligatoria entre JSON
- Todos los IDs/claves foráneas en JSON transaccionales deben existir en los maestros
- Las métricas Gold deben ser coherentes con los datos transaccionales
  (ej: si un SKU tiene `stock_fisico = 0`, su `dias_cobertura` debe ser `0`)
- Las alertas deben referenciar SKUs/sedes/entidades que existen en los otros JSON
- Verificar coherencia antes de implementar servicios — los servicios asumen que los datos son coherentes

### Volumen mínimo para que las agregaciones sean representativas
- Transacciones: mínimo 500 registros (para que promedios y tendencias sean visualmente ricos)
- Cobertura: todos los combos entidad×ubicación relevantes para el negocio
- Distribución realista: no todos los datos en el mismo rango — variedad hace el mockup creíble

### Fechas en JSON
Las fechas deben estar en UTC formato ISO 8601: `"2026-03-24T15:30:00Z"`
Si el negocio opera en otra zona horaria, las fechas siguen siendo UTC — la conversión
la hace el servicio o la UI al mostrar. Esto replica exactamente cómo funciona la BD real.

---

## 4. Services — Contratos y patrones

### Estructura estándar de un servicio
```typescript
// src/services/[entidad].service.ts
import type { TipoEntidad } from '@/types/[archivo].types'
import data from '@/data/mock_[entidad].json'

// Función base — retorna todos los registros
export async function getEntidades(): Promise<TipoEntidad[]> {
  return data as TipoEntidad[]
}

// Función filtrada — parámetro opcional
export async function getEntidadesByFiltro(
  filtro?: string | number
): Promise<TipoEntidad[]> {
  const all = await getEntidades()
  if (!filtro) return all
  return all.filter(item => item.campo === filtro)
}
```

**Por qué `async`:** Aunque hoy retornan JSON local (síncrono), el contrato `Promise<T>`
es el que tendrán en producción al hacer queries a Supabase. Las vistas llaman los servicios
con `await` desde el inicio, así no hay refactor cuando se cambie la implementación.

### Tipos auxiliares de servicio
Los tipos que son específicos de la presentación (no espejean tablas) se definen dentro del
archivo de servicio, no en `types/`. Ejemplo: `ResumenPorSede`, `TendenciaDia`.
Esto mantiene `types/` limpio y enfocado en contratos de datos persistentes.

### Función pura en servicios
Las funciones que clasifican o calculan sin I/O pueden ser síncronas y exportarse del mismo
servicio. Ejemplo: `getEstadoStock(dias: number): EstadoStock`. Son útiles porque los
componentes las pueden llamar directamente para calcular badges sin necesitar `await`.

---

## 5. Verificaciones antes de avanzar

Antes de pasar a construir componentes, verificar:

- [ ] `npx tsc --noEmit` pasa sin errores (tipos coherentes con JSON)
- [ ] Todos los IDs cruzados entre JSON son válidos (coherencia referencial)
- [ ] `npm run lint` pasa (no hay imports directos de `@/data/` fuera de `services/`)
- [ ] Los servicios retornan `Promise<T>` (no `T` directamente)
- [ ] No hay `any` en ningún archivo de `src/types/` ni `src/services/`
