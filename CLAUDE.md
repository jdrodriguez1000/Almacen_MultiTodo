# CLAUDE.md - Constitución del Proyecto Dashboard MultiTodo

Este archivo define las leyes, límites y terreno de juego para cualquier Agente de IA que interactúe con este repositorio. Es de lectura obligatoria y cumplimiento dogmático.

Desarrollado por **Sabbia Solutions & Services (Triple S)** para el cliente **Almacén MultiTodo**.

---

## 1. Comportamiento del Agente (Reglas de Oro) 🛡️

*   **Límites de Autonomía:**
    *   **Prohibido avanzar** autónomamente a una nueva fase o etapa del proyecto sin una orden explícita ("Procede", "Siguiente", "Avanza").
    *   **Prohibido escribir o generar archivos** (código, documentos o configuraciones) sin una petición o confirmación explícita del usuario.
    *   La proactividad se limita exclusivamente al análisis y sugerencias en el chat.
    *   **Mandato SDD (Spec-Driven):** El desarrollo se rige por una jerarquía documental de 4 niveles:
        1. **`docs/reqs/f[F]_[E]_prd.md`** — Qué construir y por qué. Fuente de verdad de negocio.
        2. **`docs/specs/f[F]_[E]_spec.md`** — Cómo construirlo. Contratos de datos, interfaces y comportamiento técnico esperado.
        3. **`docs/plans/f[F]_[E]_plan.md`** — Orden y estrategia de ejecución de la fase/etapa.
        4. **`docs/tasks/f[F]_[E]_task.md`** — Lista atómica de tareas ejecutables de la fase/etapa.

        **Regla de oro:** El código es un reflejo sumiso de estos documentos. Si durante la implementación se requiere un cambio no contemplado, **DETENER** y solicitar la actualización del documento correspondiente antes de continuar. Ante discrepancia entre documentos, la jerarquía PRD → SPEC → Plan → Tareas define quién manda.

*   **Mandato de Control de Cambios (CC):** El agente debe **detener toda implementación** y ejecutar `/change-control` obligatoriamente en dos escenarios:
    1. **Cambio en etapa activa:** Se detecta que algo necesario no está contemplado en ninguno de los 4 documentos SDD de la etapa en curso. Prohibido improvisar o "resolver rápido" — primero el CC.
    2. **Cambio en etapa cerrada:** Cualquier modificación a código, configuración o documentos de una etapa ya completada.
    *   **Flujo obligatorio:** Informar la necesidad → usuario aprueba → crear `docs/changes/CC_XXXXX.md` en estado `Pendiente` → usuario confirma → estado `Aprobado` → ejecutar cambios → informar cierre. Si el usuario rechaza, estado `No Aprobado` y no se toca nada.

*   **Gate de Avance de Etapa:** **Prohibido proponer o ejecutar trabajo de una nueva etapa** si el documento `docs/executives/f[F]_[E]_executive.md` de la etapa anterior no existe. El Resumen Ejecutivo es un prerequisito de avance, no un opcional.

*   **Protocolo de Inicio de Sesión (orden obligatorio):**
    1. Leer `CLAUDE.md` — Reglas globales e invariantes del proyecto.
    2. Leer `PROJECT_index.md` — Entender en qué fase/etapa está el proyecto y qué documentos SDD gobiernan el trabajo actual.
    3. Leer `PROJECT_handoff.md` — Retomar el estado táctico exacto: archivos activos, bloqueador pendiente y próxima acción.
    4. Leer `docs/lessons/lessons-learned.md` — **Solo la sección de la etapa activa.** Internalizar errores pasados y decisiones validadas para no repetirlos.
    5. Leer `docs/changes/` — **Solo los CCs en estado `✅ Aprobado`.** Ignorar Pendientes y No Aprobados.
    *   Solo después de completar los 5 pasos el agente está autorizado a escribir código o ejecutar acciones.

*   **Protocolo de Cierre de Sesión:**
    *   Cuando el usuario diga **"Terminamos"** o señale el fin de la sesión, es **OBLIGACIÓN** del agente reescribir `PROJECT_handoff.md` con el estado exacto al momento del cierre: archivos modificados, contexto inmediato, último error/bloqueador y próxima acción concreta.

*   **Idioma:**
    *   **Código/Archivos/Carpetas:** Inglés (snake_case para archivos, CamelCase para clases).
    *   **Documentación/Comentarios/Commits:** Español.
    *   **Interfaz/Output al Usuario (Dashboard):** Español (audiencia colombiana).

---

## 2. Identidad y Contexto del Proyecto 🏗️

*   **Nombre del Proyecto:** Dashboard MultiTodo
*   **Desarrollador:** Sabbia Solutions & Services — Triple S (empresa consultora)
*   **Cliente:** Almacén MultiTodo
*   **Propósito:** Transformar los datos transaccionales de ventas e inventarios en decisiones estratégicas mediante el análisis de tendencias, clasificación de productos (ABC/Pareto) y alertas automáticas de abastecimiento, permitiendo una gestión multi-sede y multi-región sin abrumar al usuario final.
*   **Naturaleza del Sistema:** BI Dashboard puro. Sin modelos de machine learning ni pronósticos estadísticos. Las alertas son reglas determinísticas basadas en umbrales y comparaciones históricas.
*   **Usuarios Finales:**
    *   Gerente General
    *   Gerente de Ventas
    *   Gerente Financiero
    *   Gerente de Operaciones
    *   **Acceso:** Todos los roles ven exactamente la misma información. No hay restricciones por rol (sin RBAC). El dashboard es único y no diferencia vistas por perfil de usuario.
*   **Reglas de Negocio Críticas:**
    *   **Responsabilidad de Datos:** El cliente es el único responsable de subir la información transaccional a Supabase diariamente. Triple S consume esa data pero no la origina.
    *   **Data Contract Obligatorio:** Existe un contrato formal (definido en Etapa 1.3) que especifica el formato, frecuencia, integridad y validaciones que el cliente debe cumplir al entregar datos. Sin cumplimiento del contrato, el pipeline de Triple S rechaza los datos.
    *   **Retraso Intencional de 24 Horas:** El dashboard siempre muestra datos del día anterior completo (T-1). El día en curso (T+0) no existe en el sistema hasta el día siguiente. Esto previene días parciales y garantiza métricas sobre jornadas cerradas. El dashboard debe indicar explícitamente **"Datos al cierre de: [fecha de ayer]"**.
    *   **Zona Horaria:** El almacén opera en horario Colombia (UTC-5 / `America/Bogota`). Supabase almacena timestamps en UTC. **Toda consulta y visualización debe convertir UTC → COT**. Una venta con `fecha_hora = 2024-03-23 02:00:00+00` equivale a `2024-03-22 21:00:00 COT` y pertenece al día 22 de marzo.
    *   **Ventana Operativa:** El almacén abre de **8:00 AM a 6:00 PM COT** todos los días. Ninguna transacción puede tener `fecha_hora` fuera de ese rango (equivalente a `13:00–23:00 UTC`). Si el pipeline detecta transacciones fuera de ventana, deben marcarse como anómalas (`ERR_MTD_001`) y reportarse como violación del Data Contract.

---

## 3. Stack Tecnológico Exacto 💻

*   **Pipeline de Datos:** Python 3.12+ (ambiente virtual `venv`).
    *   *Librerías:* `supabase-py`, `pandera`, `pandas`, `python-dotenv`, `pydantic`, `pytz`.
*   **Dashboard (Web):** Next.js + TypeScript (App Router).
    *   *Estilo:* Tailwind CSS.
    *   *Gráficos:* Recharts o Chart.js (a definir en Etapa 3.3).
    *   *Tipado:* Strict Type Safety sincronizado con Supabase.
*   **Infraestructura:**
    *   *Base de Datos:* Supabase (PostgreSQL). Tablas del cliente: prefijo `usr_`. Tablas internas Triple S: prefijo `tss_`.
    *   *Almacenamiento:* Supabase S3 / DVC para artefactos pesados.
    *   *CI/CD:* GitHub Actions.

---

## 4. Arquitectura y Estructura de Carpetas 📂

*   **`PROJECT_index.md`** *(El Mapa — Macro):* Estado del proyecto a gran escala. Contiene: fase/etapa activa, punteros a documentos SDD gobernantes, checklist de hitos y mapa de arquitectura.
    *   Secciones obligatorias: `Coordenadas Actuales` | `Hitos de la Fase Actual` | `Mapa de Arquitectura (Rutas Clave)` | `Índice de Documentos SDD`.
*   **`PROJECT_handoff.md`** *(La Lupa — Micro):* Memoria a corto plazo de la sesión. Se reescribe al cerrar cada sesión.
    *   Secciones obligatorias: `Punto de Guardado` | `Archivos en el Escritorio (Working Set)` | `Contexto Inmediato` | `Bloqueador / Último Error` | `Próxima Acción Inmediata`.
*   **`pipeline/`**: Procesos de datos (Python). Equivalente al `engine/` en proyectos con IA.
    *   `main.py`: Gateway/Switcher para modos `validate`, `etl`, `alerts`.
    *   `pipelines/`: Orquestadores que definen el orden de los pasos.
    *   `src/`: Lógica atómica (validadores, transformaciones, calculadores de métricas, generadores de alertas).
    *   `tests/`: Pruebas unitarias e integrales.
*   **`web/`**: Interfaz de Usuario (Next.js).
    *   `components/`: Componentes UI, gráficos y tarjetas de alerta.
    *   `app/`: Rutas del dashboard (App Router).
    *   `tests/`: Pruebas de componentes y E2E.
*   **`docs/`**: Documentación técnica y gobernanza SDD.
    *   Convención de nombres SDD: `f[fase]_[etapa]_[tipo].md` (ej. Fase 1, Etapa 2 → `f01_02_*.md`).
    *   `reqs/f[F]_[E]_prd.md`: Product Requirements Document (fuente de verdad de negocio).
    *   `specs/f[F]_[E]_spec.md`: Technical Specification (contratos de datos e interfaces).
    *   `plans/f[F]_[E]_plan.md`: Plan de implementación de la fase/etapa.
    *   `tasks/f[F]_[E]_task.md`: Documento de tareas atómicas de la fase/etapa.
    *   `database/schema.sql`: DDL completo sincronizado con Supabase. Es la fuente de verdad técnica de la BD. Actualizar inmediatamente después de cada `CREATE TABLE`, `ALTER TABLE` o nuevo trigger.
    *   `lessons/lessons-learned.md`: Registro acumulativo de lecciones aprendidas por etapa.
    *   `executives/f[F]_[E]_executive.md`: Resumen ejecutivo en lenguaje de negocio al cerrar cada etapa. **Prerequisito obligatorio para avanzar a la siguiente etapa.**
    *   `changes/CC_XXXXX.md`: Documentos de Control de Cambios. Numeración secuencial. Estados: `Pendiente` → `Aprobado` / `No Aprobado`.
*   **Skills de Claude Code** (`.claude/skills/`):
    *   `/update-index`: Crea o actualiza `PROJECT_index.md`.
    *   `/session-close`: Cierra la sesión actualizando `PROJECT_handoff.md` y `docs/lessons/lessons-learned.md`.
    *   `/sdd-doc`: Crea o actualiza cualquiera de los 4 documentos SDD (PRD/SPEC/Plan/Tasks).
    *   `/close-stage`: Cierra formalmente una etapa generando `docs/executives/f[F]_[E]_executive.md`.
    *   `/change-control`: Gestiona el ciclo de vida completo de un Control de Cambios.

---

## 5. Estándares y Convenciones de Código 📏

*   **Arquitectura Medallion:** Los datos fluyen por capas en Supabase:
    *   **Bronze** (`tss_bronze_*`): Raw data copiada sin modificar desde tablas `usr_*` del cliente.
    *   **Silver** (`tss_silver_*`): Datos limpios, validados y con timezone convertido a COT.
    *   **Gold** (`tss_gold_*`): Métricas derivadas, clasificación ABC, indicadores para alertas.
*   **Validación Mandatoria:** Uso obligatorio de esquemas **Pandera** para validar datos en capas Silver y Gold. Los esquemas deben reflejar exactamente las restricciones del Data Contract.
*   **Gestión de Errores:** Prohibido usar `pass`. Los errores se mapean a códigos con prefijo `ERR_MTD_XXX` y se registran en logs locales y en tabla `tss_error_log` de Supabase.
    *   `ERR_MTD_001` — Transacción fuera de ventana operativa (8 AM–6 PM COT).
    *   `ERR_MTD_002` — SKU no registrado en `usr_productos`.
    *   `ERR_MTD_003` — `id_sede` no registrada en `usr_sedes`.
    *   `ERR_MTD_004` — Registro con fecha del día en curso (T+0) — carga anticipada.
    *   `ERR_MTD_005` — Violación de constraint numérico (precio, costo, cantidad, stock).
*   **Seguridad:** Cero hardcoding. Secretos en `.env` (no trackeado), rutas y nombres de tablas en `config.yaml`.
*   **Consistencia Temporal:** Toda conversión UTC → COT se realiza con `pytz` usando `America/Bogota`. **Prohibido usar offsets manuales como `-5`** para evitar errores en horario de verano de zonas externas.
*   **Separación de Responsabilidades:** Prohibido escribir lógica de transformación en `main.py` o en los orquestadores de `pipelines/`. Toda la lógica de negocio debe estar en `src/`.
*   **Triple Persistencia de Estado:** El éxito o fallo de cada proceso crítico debe registrarse en 3 canales obligatorios: (1) archivo local `latest`, (2) log detallado con timestamp, (3) tabla `tss_pipeline_log` en Supabase.
*   **DVC Obligatorio:** Prohibido subir datasets o artefactos pesados al repositorio Git.
*   **SQL-First:** Las transformaciones pesadas de datos deben ejecutarse en SQL (Supabase) siempre que sea posible.
*   **TDD Obligatorio:** Todo archivo Python creado debe seguir el ciclo Test-Driven Development:
    1. Escribir el test primero.
    2. Implementar el código mínimo para que pase.
    3. Refactorizar.
    *   Los tests viven en `pipeline/tests/` con estructura de subcarpetas que espeja `pipeline/src/`.
    *   **Estándar para conectores:** Integration tests contra Supabase real. No mockear la BD en tests de conectores.
    *   Ningún módulo Python se considera "hecho" sin al menos un test de integración.
*   **Prefijos de Tablas en Supabase:**
    *   `usr_*` — Propiedad del cliente (solo lectura para Triple S). No alterar DDL sin CC aprobado.
    *   `tss_*` — Propiedad de Triple S (Bronze, Silver, Gold, logs, alertas, cuarentena).

---

## 6. Flujos de Trabajo (Workflow y Git) 🔄

*   **Git Flow:** `feat/*` ➔ `dev` ➔ `test` ➔ `prod`.
    *   `main` es la rama de **gobernanza permanente** (SDD, resúmenes ejecutivos, CLAUDE.md). No es rama de desarrollo.
    *   `prod` es la rama de código en producción visible para el cliente.
    *   *Paso Crítico (orden obligatorio):* Al finalizar pruebas en `test`, sincronizar arreglos a `dev` **primero**, luego `dev → prod`. Nunca `test → prod` directamente.
*   **Reglas de Commits:** Commits atómicos, en **español**, con prefijos:
    *   `feat:` — Nueva funcionalidad
    *   `fix:` — Corrección de errores
    *   `docs:` — Documentación
    *   `refactor:` — Cambios que no corrigen ni añaden funcionalidad
*   **GitHub Actions (implementar en Etapa 2.1):**
    *   **CI Quality Gate:** Corre en cada push/PR. Ejecuta en paralelo: (a) tests del pipeline con `pytest` en `pipeline/tests/`, (b) tests del dashboard con `npm test` en `web/`. Secrets requeridos: `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_ROLE_KEY`. Escucha en PRs hacia `dev`, `test` y `prod` (no hacia `main`).
    *   **`release-please`:** Genera versiones semánticas automáticas al mergear a `prod`.
    *   **Protección de ramas:** `prod` (aprobación humana obligatoria), `test` y `dev` (CI Quality Gate debe pasar), `feat/*` (libre).
*   **Comandos Recurrentes:**
    *   *Pipeline:* `python pipeline/main.py --mode [validate|etl|alerts]`
    *   *Web:* `npm run dev`
    *   *Tests:* `pytest pipeline/tests` | `npm test`

---

## 7. Conocimiento de Dominio (Almacén MultiTodo) 🏪

*   **Operación:**
    *   Horario oficial: **8:00 AM – 6:00 PM COT** (`America/Bogota`). Abierto todos los días del año, en todas las sedes.
    *   Toda transacción fuera de esta ventana es una anomalía (`ERR_MTD_001`).
    *   Equivalencia UTC: la ventana operativa corresponde a `13:00–23:00 UTC`.
*   **Cobertura Geográfica:**
    *   País: Colombia
    *   Distribución de sedes:

    | Ciudad | Sedes |
    |---|---|
    | Bogotá y Medellín | 3 (total entre ambas) |
    | Cali | 2 |
    | Cartagena | 1 |
    | Cúcuta | 1 |
    | **Total** | **7 sedes activas** |

*   **Catálogo de Productos:**
    *   ~100 SKUs activos.
    *   Organizados en jerarquía: `familia → categoría → subcategoría`.
    *   Maestro en tabla `usr_productos` (mantenida y actualizada por el cliente).
*   **Retraso Intencional de Datos (24 Horas):**
    *   El dashboard solo muestra datos de **jornadas completas y cerradas**.
    *   El dato más reciente disponible siempre corresponde al día anterior (T-1).
    *   El encabezado del dashboard debe mostrar: **"Datos al cierre de: [DD/MM/YYYY]"**.
    *   El pipeline valida que no existan registros del día actual (T+0). Si los hay, se quarentinan en `tss_quarantine` con código `ERR_MTD_004` hasta el día siguiente.
*   **Ventana de Actualización Diaria (Pipeline Schedule):**
    *   `05:30 UTC (00:30 COT)` — El cliente completa la carga de datos en tablas `usr_*`.
    *   `08:30 UTC (03:30 COT)` — El pipeline de Triple S ejecuta validación → ETL → cálculo de alertas y actualiza el dashboard.
    *   El dashboard está disponible con datos frescos **4.5 horas antes** de la apertura del almacén (8:00 AM COT).
    *   Si a las `09:00 UTC (04:00 COT)` el pipeline no completó exitosamente, se activa alerta interna de Triple S.
*   **Responsabilidades de Datos:**
    *   El cliente es el único responsable de la calidad, puntualidad e integridad de los datos en tablas `usr_*`.
    *   Triple S garantiza la correcta ingestión, transformación y visualización de los datos entregados conforme al Data Contract.
    *   Los problemas originados en datos incorrectos del cliente se documentan en `tss_error_log` y se notifican formalmente al cliente.

---

## 8. Data Contract (Contrato de Datos Cliente–Triple S) 📋

*   **Definición:** Acuerdo técnico y operativo que especifica qué datos debe entregar el cliente, en qué formato, con qué frecuencia y bajo qué restricciones de integridad. Es el **prerrequisito técnico de toda la cadena de valor de Triple S**. Definido formalmente en `docs/specs/f01_03_spec.md`.

*   **Tablas bajo contrato (propiedad del cliente):**

    | Tabla | Propósito | Frecuencia de actualización |
    |---|---|---|
    | `usr_ventas` | Transacciones de venta | Diaria — datos completos del día anterior |
    | `usr_inventario` | Stock físico por SKU/sede | Diaria — estado al cierre del día anterior |
    | `usr_productos` | Maestro de productos (SKU, nombre, jerarquía) | Cuando haya altas, bajas o modificaciones |
    | `usr_sedes` | Maestro de sedes (ciudad, nombre) | Cuando haya cambios |

*   **Esquema Oficial (DDL completo en `docs/database/schema.sql`):**

    ```sql
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
      constraint usr_inventario_pkey                  primary key (sku, id_sede),
      constraint usr_inventario_id_sede_fkey          foreign key (id_sede) references usr_sedes (id_sede),
      constraint usr_inventario_sku_fkey              foreign key (sku)     references usr_productos (sku),
      constraint usr_inventario_stock_fisico_check    check (stock_fisico >= 0),
      constraint usr_inventario_costo_reposicion_check check (costo_reposicion > 0)
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
    ```

*   **Validaciones Obligatorias del Pipeline (ejecutadas antes de Bronze):**
    1. `fecha_hora` en `usr_ventas` dentro de ventana operativa: `13:00–23:00 UTC`.
    2. No se aceptan registros con `fecha_hora` del día en curso (T+0).
    3. Todos los `sku` de `usr_ventas` e `usr_inventario` deben existir en `usr_productos`.
    4. Todos los `id_sede` deben existir en `usr_sedes`.
    5. `stock_fisico >= 0`, `cantidad > 0`, `precio > 0`, `costo > 0` (si no es null).

*   **Protocolo ante Violación del Contrato:**
    1. El pipeline registra el error con código `ERR_MTD_XXX` en `tss_error_log`.
    2. Los registros inválidos van a cuarentena en tabla `tss_quarantine`.
    3. Se genera alerta interna para el equipo Triple S.
    4. Se notifica formalmente al cliente con detalle del error y registros afectados.
    5. Los datos no pasan a Bronze hasta que el cliente corrija y reentregue.

---

## 9. Sistema de Alertas 🔔

*   **Principio:** Las alertas son mensajes en lenguaje natural (español) generados por reglas determinísticas. No son pronósticos. Se calculan sobre datos de capa Gold (T-1) y se muestran en el dashboard al inicio de cada jornada.
*   **Clasificación ABC/Pareto** (recalculada cada lunes sobre los últimos 90 días):
    *   **Clase A:** Top 20% de SKUs por valor de ventas acumuladas → ~80% del revenue.
    *   **Clase B:** Siguientes 30% de SKUs → ~15% del revenue.
    *   **Clase C:** Restantes 50% de SKUs → ~5% del revenue.
*   **Ventana de Análisis por Defecto:** 7 días completos cerrados (T-1 a T-7).

### Alertas Negativas (Riesgos) 🔴

| Código | Nombre | Condición de activación | Mensaje al usuario |
|---|---|---|---|
| `ALT_NEG_001` | Stock Crítico | `stock_físico < promedio_venta_7d × 3` | "SKU [X] en [Sede]: Stock crítico. Quedan aproximadamente [N] días de venta. Se recomienda reposición urgente." |
| `ALT_NEG_002` | Rotación Lenta (Clase A/B) | SKU Clase A o B con ventas en últimos 7d < 30% del promedio de su categoría | "SKU [X] (Clase [A/B]) en [Sede]: Rotación por debajo del promedio de su categoría. Evaluar estrategia comercial." |
| `ALT_NEG_003` | Caída Anómala de Ventas | Ventas del último día < 50% del promedio del mismo día de semana en las últimas 4 semanas | "Categoría [X] en [Sede]: Ventas cayeron [N]% vs el histórico de este día de semana. Verificar si hubo problema operativo." |
| `ALT_NEG_004` | Desabastecimiento | `stock_físico = 0` en SKU Clase A o B | "CRÍTICO: SKU [X] (Clase [A/B]) sin stock en [Sede]. Impacto inmediato en ingresos. Acción requerida hoy." |
| `ALT_NEG_005` | Producto Obsoleto | Sin ventas en los últimos 30 días con `stock_físico > 0` | "SKU [X]: Sin movimiento en 30+ días. Stock actual: [N] unidades. Evaluar liquidación o descontinuación." |
| `ALT_NEG_006` | Margen Comprimido (Clase A) | `(precio - costo) / precio < 15%` en SKU Clase A | "SKU [X] (Clase A): Margen del [N]% está por debajo del umbral mínimo. Revisar estructura de costos o precio de venta." |

### Alertas Positivas (Oportunidades) 🟢

| Código | Nombre | Condición de activación | Mensaje al usuario |
|---|---|---|---|
| `ALT_POS_001` | Alta Rotación | Ventas últimos 7d > 150% del promedio histórico del SKU | "SKU [X] en [Sede]: Ventas aceleradas ([N]% sobre el promedio). Anticipar reabastecimiento para no perder ventas." |
| `ALT_POS_002` | Categoría en Crecimiento | Ventas de categoría en últimos 7d > 20% vs mismo período del mes anterior | "Categoría [X]: Crecimiento del [N]% esta semana. Asegurar disponibilidad para mantener el impulso." |
| `ALT_POS_003` | Reabastecimiento Exitoso | SKU pasó de stock crítico (<3 días) a saludable (>7 días) en las últimas 24h | "SKU [X] en [Sede]: Stock recuperado satisfactoriamente. Nivel actual: [N] unidades ([D] días de venta)." |
| `ALT_POS_004` | Producto Estratégico | Clase A + margen > 35% + rotación dentro del promedio | "SKU [X]: Producto estrella. Alta rotación y margen saludable. Priorizar disponibilidad permanente." |
| `ALT_POS_005` | Sede de Alto Rendimiento | Margen operativo de sede > promedio general en 15% | "Sede [X]: Margen del [N]%, superando el promedio en [M]%. Analizar sus prácticas para replicar en otras sedes." |
| `ALT_POS_006` | Equilibrio Óptimo | Clase A + margen > 35% + stock entre 7 y 14 días | "SKU [X]: Gestión óptima. Rotación, margen y disponibilidad en equilibrio perfecto. Mantener estrategia actual." |

*   **Reglas de Presentación en el Dashboard:**
    *   Alertas negativas primero, ordenadas por severidad: Crítico (`ALT_NEG_004`) → Alto (`ALT_NEG_001`) → Medio (resto).
    *   Alertas positivas en sección separada "Oportunidades del Día".
    *   Cada alerta incluye: código, ícono de severidad, mensaje en lenguaje natural, sede afectada y fecha de cálculo.
    *   Vista resumen: máximo 10 alertas negativas + 5 positivas. Resto en vista detallada con filtros.

---

## 10. Fases y Etapas del Proyecto 🗺️

> **Mandato:** El avance entre fases y etapas requiere orden explícita del usuario. Cada etapa tiene su propio conjunto de documentos SDD (`f[F]_[E]_prd.md`, `_spec.md`, `_plan.md`, `_task.md`).

> **Dashboard Transversal:** La construcción del `web/` no es exclusiva de ninguna fase. A medida que cada etapa produce datos o contratos verificables, se desarrolla el componente de dashboard correspondiente en paralelo.

### Fase 1 — Gobernanza y Cimientos
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **1.1** | Constitución del proyecto: CLAUDE.md, PROJECT_index.md, estructura de carpetas y repositorio | `f01_01_*.md` |
| **1.2** | Validación de infraestructura: verificar tablas Supabase, triggers, índices, permisos y conectividad | `f01_02_*.md` |
| **1.3** | Data Contract: especificación formal del contrato de datos cliente–Triple S, validaciones y protocolo de rechazo | `f01_03_*.md` |

### Fase 2 — Ingeniería de Datos e Integración
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **2.1** | Pipeline de validación: verificar que los datos entrantes cumplen el Data Contract antes de la ingestión | `f02_01_*.md` |
| **2.2** | ETL Bronze → Silver: ingestión, limpieza, conversión UTC → COT y persistencia en capas de Supabase | `f02_02_*.md` |
| **2.3** | Capa Gold: cálculos derivados (consumo diario, rotación, clasificación ABC semanal, márgenes) | `f02_03_*.md` |

### Fase 3 — Analítica y Alertas
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **3.1** | EDA: análisis de patrones de venta, estacionalidad por ciudad/categoría y comportamiento por sede | `f03_01_*.md` |
| **3.2** | Motor de alertas: implementación de las 12 reglas (6 negativas + 6 positivas) con umbrales calibrados | `f03_02_*.md` |
| **3.3** | Dashboard MVP: visualización de ventas, inventarios, clasificación ABC y alertas (Next.js + Tailwind) | `f03_03_*.md` |

### Fase 4 — Operación y Mejora Continua
| Etapa | Descripción | Docs SDD |
|---|---|---|
| **4.1** | Publicación en producción: deploy, monitoreo de calidad de datos y disponibilidad del dashboard | `f04_01_*.md` |
| **4.2** | Reportería avanzada: análisis de escenarios, comparativas inter-sede e inter-categoría | `f04_02_*.md` |
| **4.3** | Mejora continua: feedback del cliente, ajuste de umbrales de alertas y nuevas métricas | `f04_03_*.md` |

---

## 11. Gobernanza Estratégica 📊

*   **Umbrales de Éxito del Proyecto:**

    **Funcionalidad (UX):**
    *   Dashboard carga en < 2 segundos (P95).
    *   Usuario identifica los 5 SKUs en mayor riesgo en < 1 minuto.
    *   Filtros por sede/categoría responden en < 500ms.
    *   Alertas accionables con < 5% de falsos positivos.

    **Integridad de Datos:**
    *   100% de transacciones diarias ingestadas correctamente (0 pérdidas).
    *   Datos procesados disponibles en el dashboard antes de las **08:30 UTC (03:30 COT)** — 4.5 horas antes de la apertura.
    *   Consistencia de stock: diferencia entre stock físico y calculado < 2%.
    *   Clasificación ABC recalculada sin errores cada lunes.

    **Impacto de Negocio:**
    *   Reducción de desabastecimiento no planeado en 40% vs baseline.
    *   Reducción de productos obsoletos (sin venta > 30 días) en 25%.
    *   Satisfacción de usuarios finales ≥ 4.0/5.0 (encuesta post-implementación).

*   **KPI Principal del Proyecto:** `Data Quality Score` — porcentaje de registros diarios que pasan todas las validaciones del Data Contract sin intervención manual. **Objetivo: ≥ 98%.**

*   **Indicador de Progreso del Proyecto:** Cada Resumen Ejecutivo incluye el porcentaje de avance global:
    *   Total: 4 fases × 3 etapas = **12 etapas**.
    *   **Peso de cada etapa** = `100% / 12 = 8.33%`.
    *   Una etapa cuenta como cerrada **únicamente** si existe su archivo `docs/executives/f[F]_[E]_executive.md`.
    *   Si se agregan etapas, el porcentaje puede bajar. El próximo ejecutivo cerrado debe incluir nota explicativa al cliente:
        > ⚠️ Nota de Alcance: El avance bajó de X% a Y% porque se incorporaron Z etapas nuevas. El trabajo completado no cambió — el alcance del proyecto creció.
