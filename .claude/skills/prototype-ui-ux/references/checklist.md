# Checklist de Validación — prototype-ui-ux

Lista de verificación para la fase final de un prototipo. Adaptar los ítems específicos
del dominio (nombres de vistas, cantidad de alertas, etc.) según el proyecto activo.
Los criterios de aceptación definitivos están en la SPEC del proyecto (`docs/specs/`).

---

## Grupo 1 — Compilación y arranque

- [ ] `npm install` completa sin errores ni conflictos
- [ ] `npx tsc --noEmit` pasa — cero errores de TypeScript, cero `any` en `src/`
- [ ] `npm run lint` pasa — incluyendo la regla `no-restricted-imports`
- [ ] `npm run build` completa sin errores
- [ ] `npm run dev` levanta en `localhost:3000` sin errores en consola del navegador

**Por qué importa:** Si el build falla, el prototipo no puede presentarse al cliente. El
`tsc` y el `lint` son la garantía de que el Principio de Migración Cero está intacto.

---

## Grupo 2 — Principio de Migración Cero

- [ ] Ningún archivo en `src/components/` importa directamente de `src/data/`
- [ ] Ningún archivo en `src/app/` importa directamente de `src/data/`
- [ ] La regla ESLint `no-restricted-imports` está activa y detecta violaciones
- [ ] Todos los servicios retornan `Promise<T>` (no `T` directamente)
- [ ] Los tipos en `usr.types.ts` compilan sin errores contra los datos de los JSON

**Cómo verificar:** `npm run lint` detecta importaciones directas. Para verificar manualmente:
```bash
# No debe retornar resultados
grep -r "from '@/data/" src/components/
grep -r "from '@/data/" src/app/
```

---

## Grupo 3 — Vistas y navegación

- [ ] Todas las vistas definidas en el proyecto cargan y muestran datos sin errores
- [ ] La navegación entre vistas es fluida — sin recarga completa de página (SPA)
- [ ] El sidebar marca correctamente la ruta activa en cada vista
- [ ] Los links del sidebar llevan a la vista correcta

---

## Grupo 4 — Funcionalidad específica del proyecto

> Completar con los criterios de la SPEC del proyecto activo (sección de criterios de aceptación).
> Ejemplos genéricos:

- [ ] Los filtros de tabla funcionan sin recarga de página
- [ ] Los filtros son acumulables (múltiples filtros simultáneos)
- [ ] Los gráficos renderizan correctamente con datos reales del JSON
- [ ] Las listas/tablas muestran el conteo correcto de registros
- [ ] Las tarjetas de alerta muestran código, mensaje, entidad afectada y fecha

---

## Grupo 5 — Dark Mode / Light Mode

- [ ] El toggle está visible en el header en todas las vistas
- [ ] Al hacer clic, el modo cambia visualmente de inmediato (sin parpadeo)
- [ ] Al recargar la página, el modo seleccionado se mantiene (`localStorage`)
- [ ] Sidebar es legible en modo oscuro
- [ ] Header es legible en modo oscuro
- [ ] Tarjetas KPI son legibles en modo oscuro
- [ ] Tablas son legibles en modo oscuro (texto, fondos alternados si los hay)
- [ ] Gráficos Recharts usan `chartColors` dinámicos — no se ven blancos sobre blanco ni negros sobre negro
- [ ] Badges de estado/severidad son legibles en modo oscuro
- [ ] Los banners (prototipo + subtítulo) son legibles en modo oscuro

---

## Grupo 6 — Banners del prototipo

- [ ] El banner de prototipo está visible en **todas** las vistas (ámbar, sticky top)
- [ ] El banner de contexto temporal (T-1 o equivalente) está visible en todas las vistas
- [ ] Los banners no obstruyen el contenido principal (el contenido no queda detrás de ellos)
- [ ] El texto de los banners es legible y claro

---

## Grupo 7 — Coherencia de datos ficticios

- [ ] Los archivos maestros tienen el conteo exacto de registros definido en la SPEC
- [ ] Todos los IDs/claves foráneas en JSON transaccionales existen en los maestros
- [ ] Las métricas derivadas son coherentes con los datos transaccionales
  (ej: si stock = 0, días de cobertura = 0)
- [ ] Las entidades referenciadas en alertas existen en sus respectivos JSON
- [ ] Los gráficos muestran variaciones visibles (no todos los valores iguales)

---

## Grupo 8 — Responsivo

- [ ] El mockup es legible y funcional en resolución **1920×1080**
- [ ] El mockup es legible y funcional en resolución **1366×768**
- [ ] Ninguna tabla o gráfico se corta o vuelve ilegible en la resolución menor
- [ ] El sidebar no colapsa ni obstruye el contenido en ninguna de las dos resoluciones

---

## Grupo 9 — Rendimiento

- [ ] Tiempo de carga inicial (primera carga, `npm run dev`) menor a **2 segundos**
- [ ] Los filtros y la navegación responden en menos de **500ms**

---

## Grupo 10 — Cierre y aprobación del cliente

- [ ] Commit del código en la rama correcta (feat/* según Git Flow del proyecto)
- [ ] Demo preparada: flujo de navegación planeado, datos representativos visibles
- [ ] Sesión de validación realizada con al menos un decisor del cliente
- [ ] Aprobación explícita registrada en `PROJECT_handoff.md` con fecha y frase del cliente
- [ ] Sin aprobación registrada → la etapa **no se cierra**, independientemente del estado técnico

---

## Cómo reportar al usuario

Al completar la validación, reportar en este formato:

```
✅ Grupo 1 — Compilación: 5/5
✅ Grupo 2 — Migración Cero: 4/4
✅ Grupo 3 — Navegación: 4/4
✅ Grupo 4 — Funcionalidad: X/X
✅ Grupo 5 — Dark Mode: 10/10
✅ Grupo 6 — Banners: 4/4
✅ Grupo 7 — Datos: 5/5
✅ Grupo 8 — Responsivo: 4/4
✅ Grupo 9 — Rendimiento: 2/2
⬜ Grupo 10 — Cierre: 3/5 (pendiente demo con cliente)

Total: XX/XX criterios — Listo para presentación al cliente
```
