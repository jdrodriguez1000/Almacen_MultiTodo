# Statement of Work (SOW)
## Dashboard MultiTodo — Sistema de Inteligencia de Negocio para Almacenes

**Cliente:** Almacén MultiTodo
**Elaborado por:** Sabbia Solutions & Services (Triple S)
**Fecha:** 2026-03-24
**Versión:** 1.0
**Estado:** ✅ Aprobado — 2026-03-24

### Perspectivas recogidas
| Rol | Entrevistado | Fecha |
|---|---|---|
| Gerente General | Almacén MultiTodo | 2026-03-24 |
| Gerente de Ventas | Almacén MultiTodo | 2026-03-24 |
| Gerente Financiero | Almacén MultiTodo | 2026-03-24 |
| Gerente de Operaciones | Almacén MultiTodo | 2026-03-24 |

> **Nota metodológica:** Este SOW fue construido de forma retrospectiva (el proyecto ya se encontraba en Etapa 1.2 al momento de su elaboración). La información fue consolidada a partir del documento de constitución del proyecto (CLAUDE.md), los documentos SDD de la Fase 1 y las decisiones de diseño registradas en sesiones anteriores. Refleja el acuerdo de alcance vigente al cierre de la Etapa 1.1.

---

## 1. Contexto y Antecedentes

Almacén MultiTodo es una cadena de comercio minorista con presencia en las principales ciudades de Colombia. Opera **siete sedes activas** distribuidas en Bogotá, Medellín, Cali, Cartagena y Cúcuta, con un horario de atención uniforme de 8:00 AM a 6:00 PM todos los días del año. Su catálogo activo supera los 100 referencias (SKUs), organizados en una jerarquía de familia, categoría y subcategoría.

El negocio genera un volumen importante de transacciones de venta e inventario diariamente en cada sede. Sin embargo, esta información ha permanecido dispersa y sin un mecanismo centralizado que permita a los gerentes de la organización analizarla de forma integrada, comparar el desempeño entre sedes, o detectar oportunidades y riesgos antes de que se conviertan en problemas operativos o financieros.

La organización cuenta con Supabase como plataforma de base de datos donde el cliente carga la información transaccional diariamente. Triple S fue contratada para construir sobre esa infraestructura una solución que convierta esos datos en decisiones estratégicas. Este proyecto es el primer paso hacia una operación basada en datos para Almacén MultiTodo.

---

## 2. Problema u Oportunidad

Hoy, los cuatro gerentes de Almacén MultiTodo (General, Ventas, Financiero y Operaciones) toman decisiones sobre inventario, reabastecimiento y estrategia comercial sin información consolidada ni oportuna. Cada gerente accede a los datos de forma fragmentada — o directamente no los accede — lo que genera decisiones reactivas: se descubren los quiebres de stock cuando ya hay pérdida de ventas, los productos con baja rotación se acumulan sin que nadie los detecte a tiempo, y las sedes con mejor desempeño no son identificadas como referente para el resto de la red.

El problema tiene tres dimensiones que afectan al negocio de formas distintas. Desde la perspectiva operativa, no hay visibilidad de stock en tiempo real que permita anticipar el reabastecimiento antes de llegar a cero. Desde la perspectiva comercial, no existe una clasificación sistemática de qué productos generan la mayor parte del ingreso (análisis ABC/Pareto), lo que impide priorizar los esfuerzos de gestión donde más impactan. Desde la perspectiva financiera, los márgenes por producto y por sede no se monitorean rutinariamente, dejando expuesta la rentabilidad ante variaciones de costo que no se detectan a tiempo.

La oportunidad que este proyecto representa es transformar los datos transaccionales que el cliente ya genera y carga diariamente en una fuente de inteligencia de negocio accesible para todos los gerentes, sin necesidad de conocimientos técnicos, y disponible cada mañana antes de que el almacén abra sus puertas.

---

## 3. Objetivo del Proyecto

El objetivo de este proyecto es construir un dashboard de inteligencia de negocio que transforme los datos de ventas e inventarios de Almacén MultiTodo en información accionable para la gerencia, de manera que se puedan identificar riesgos y oportunidades de forma sistemática, anticipada y sin dependencia de análisis manuales.

### Objetivos específicos:
- Centralizar y validar la información transaccional diaria de las 7 sedes en una sola plataforma analítica.
- Proveer a los gerentes de una vista consolidada del desempeño de ventas, inventarios y márgenes, filtrable por sede y categoría.
- Clasificar automáticamente los productos según su contribución al ingreso (análisis ABC/Pareto) y actualizar esa clasificación semanalmente.
- Generar alertas automáticas diarias en lenguaje natural que señalen los productos en riesgo de quiebre de stock, los de baja rotación, las caídas anómalas de ventas y las oportunidades de crecimiento detectadas.
- Garantizar que la información en el dashboard siempre corresponde a jornadas completas y cerradas (datos del día anterior), eliminando la ambigüedad de días parciales.
- Establecer un contrato formal de datos entre el cliente y Triple S que defina qué información debe entregarse, en qué formato y con qué frecuencia, como condición de funcionamiento de todo el sistema.

---

## 4. Entregables del Proyecto

### Entregable 1: Pipeline de validación y procesamiento de datos

Un proceso automatizado que se ejecuta diariamente a las 3:30 AM hora Colombia (antes de la apertura del almacén) y que recorre tres etapas: validación, transformación y cálculo de indicadores. Este proceso toma los datos cargados por el cliente en la base de datos, verifica que cumplen el contrato de datos acordado, los limpia y estandariza, y calcula todas las métricas que el dashboard necesita mostrar. Si algún dato no cumple el contrato, el proceso lo registra, lo separa del flujo principal y notifica al equipo de Triple S y al cliente con el detalle del problema. El cliente recibirá en su plataforma datos siempre confiables o una alerta clara de por qué no los hay.

### Entregable 2: Contrato de Datos Cliente–Triple S

Un documento técnico y operativo que especifica con precisión qué tablas debe mantener el cliente, qué campos debe incluir cada registro, qué restricciones de integridad deben cumplirse y en qué ventana horaria deben estar disponibles los datos. Este contrato es el fundamento de toda la cadena de valor: sin datos que cumplan el contrato, el pipeline rechaza la información y el dashboard no se actualiza. El documento incluye también el protocolo de qué pasa cuando hay una violación: qué se registra, quién recibe la alerta y cuál es el proceso de corrección y reentrega.

### Entregable 3: Dashboard web de inteligencia de negocio

Una aplicación web accesible desde cualquier navegador que muestra, cada mañana, el estado consolidado del negocio con datos del día anterior. El encabezado siempre indica la fecha exacta a la que corresponden los datos ("Datos al cierre de: DD/MM/YYYY"). Los gerentes podrán filtrar la información por sede y categoría, ver el ranking de productos por ventas, identificar los artículos clasificados como A, B o C según su contribución al ingreso, y leer las alertas del día en lenguaje natural y sin tecnicismos. La aplicación carga en menos de 2 segundos y los filtros responden en menos de medio segundo.

### Entregable 4: Sistema de alertas inteligentes

Un conjunto de 12 reglas de alerta (6 de riesgo y 6 de oportunidad) que se calculan automáticamente cada día y se presentan en el dashboard en lenguaje natural. Las alertas de riesgo cubren situaciones como stock crítico, productos sin stock de clase A o B, caídas anómalas de ventas, baja rotación de productos importantes, productos sin movimiento en 30 días y márgenes por debajo del umbral mínimo. Las alertas de oportunidad señalan productos con ventas aceleradas, categorías en crecimiento, reabastecimientos exitosos, productos estrella y sedes de alto rendimiento. Cada alerta incluye el nombre del producto o sede afectada, el dato que la disparó y una recomendación de acción concreta.

---

## 5. Información y Visualización

Los cuatro gerentes de Almacén MultiTodo tienen acceso exactamente a la misma información. No hay restricciones por rol: todos ven el mismo dashboard sin diferenciación de vistas. Esta decisión fue tomada intencionalmente para simplificar la solución y porque la información es estratégica para todos los perfiles de la gerencia por igual.

La información que el dashboard presenta está organizada en torno a tres preguntas de negocio: ¿qué vendimos ayer y cómo se compara con el histórico? ¿Qué tenemos en inventario y dónde hay riesgo? ¿Qué alertas requieren acción hoy? Los gerentes pueden filtrar toda la información por sede y por categoría de producto. La clasificación ABC permite priorizar: siempre se puede saber cuáles son los 20% de productos que generan el 80% del ingreso.

El dashboard se actualiza una vez al día — no en tiempo real — porque el modelo de negocio opera sobre jornadas cerradas. Un gerente que entra a las 7:00 AM encontrará la información completa del día anterior lista para revisar antes de que el almacén abra. Esto es por diseño, no una limitación: garantiza que nunca se toman decisiones sobre datos de un día a medio completar.

---

## 6. Perfiles de Usuario

| Perfil | Descripción | Necesidad principal | Cómo usarán el resultado |
|---|---|---|---|
| Gerente General | Máxima autoridad de la organización. Supervisa el desempeño global de todas las sedes. | Visión consolidada del negocio para decisiones estratégicas y de asignación de recursos. | Revisión matutina del desempeño de ayer, comparación inter-sede, seguimiento de alertas críticas. |
| Gerente de Ventas | Responsable del rendimiento comercial de la red de sedes. | Identificar qué productos y sedes están creciendo o decayendo, y actuar antes de perder ventas. | Análisis de rotación, alertas de caída de ventas, clasificación ABC para foco comercial. |
| Gerente Financiero | Responsable de la rentabilidad y salud financiera del negocio. | Control de márgenes por producto y sede, y visibilidad del capital inmovilizado en inventario. | Seguimiento de márgenes, alertas de margen comprimido, análisis de productos obsoletos. |
| Gerente de Operaciones | Responsable de la eficiencia logística y disponibilidad de producto. | Anticipar quiebres de stock y planificar reabastecimiento antes de que afecte las ventas. | Alertas de stock crítico y desabastecimiento, indicadores de días de cobertura por SKU y sede. |

---

## 7. Criterios de Éxito

El proyecto se considera exitoso cuando los gerentes de Almacén MultiTodo pueden, cada mañana antes de la apertura del almacén, tomar decisiones de reabastecimiento, gestión comercial y control financiero basadas en el dashboard — sin necesidad de solicitar reportes adicionales ni hacer análisis manuales. El indicador más importante de éxito técnico es que el 98% o más de los registros diarios pasen todas las validaciones del contrato de datos sin intervención manual (`Data Quality Score ≥ 98%`).

### Indicadores de éxito:
| Indicador | Situación actual | Situación esperada |
|---|---|---|
| Visibilidad de desempeño de ventas | Fragmentada o inexistente | Dashboard consolidado disponible cada mañana antes de las 8:00 AM COT |
| Detección de quiebres de stock | Reactiva (cuando ya ocurrió) | Anticipada: alerta con ≥3 días de antelación según stock actual y ritmo de ventas |
| Clasificación de productos por importancia | No existe / manual | Clasificación ABC automática recalculada cada lunes sobre los últimos 90 días |
| Tiempo para identificar los 5 SKUs en mayor riesgo | Desconocido / alto | Menos de 1 minuto en el dashboard |
| Reducción de desabastecimiento no planeado | Baseline actual | Reducción del 40% vs. baseline al cierre del proyecto |
| Reducción de productos obsoletos (sin venta >30 días) | Baseline actual | Reducción del 25% vs. baseline al cierre del proyecto |
| Satisfacción de los gerentes con la herramienta | No aplica | Calificación ≥ 4.0/5.0 en encuesta post-implementación |
| Velocidad de carga del dashboard | No aplica | Menos de 2 segundos (P95) |
| Disponibilidad de datos frescos | No aplica | Datos del día anterior disponibles antes de las 8:00 AM COT todos los días |

---

## 8. Alcance

### Qué incluye este proyecto:
- Pipeline de datos automatizado con tres modos de operación: validación, transformación (ETL) y cálculo de alertas.
- Validación formal de los datos del cliente contra un contrato de datos antes de procesarlos.
- Transformación y almacenamiento de datos en tres capas: Bronze (datos crudos), Silver (datos limpios con zona horaria Colombia) y Gold (métricas e indicadores derivados).
- Clasificación ABC/Pareto automática de productos, recalculada cada lunes sobre los últimos 90 días.
- 12 reglas de alerta determinísticas (6 negativas + 6 positivas) en lenguaje natural, calculadas diariamente.
- Dashboard web accesible desde navegador con filtros por sede y categoría.
- Monitoreo de márgenes por producto y sede.
- Cobertura de las 7 sedes activas de Almacén MultiTodo en Colombia.
- Gestión de un catálogo de ~100 SKUs con jerarquía familia–categoría–subcategoría.
- Pipeline programado para ejecutarse automáticamente a las 3:30 AM COT todos los días.
- Documentación técnica completa (SDD: PRD, SPEC, Plan, Tareas) por cada etapa del proyecto.
- Registro de errores y cuarentena de datos inválidos con notificación formal al cliente.
- Infraestructura de CI/CD en GitHub Actions para garantizar la calidad del código en cada cambio.

### Qué NO incluye este proyecto:
- Modelos de machine learning, pronósticos estadísticos ni predicciones de demanda. Las alertas son reglas determinísticas basadas en umbrales, no inteligencia artificial.
- Captura o generación de datos transaccionales. El cliente es el único responsable de cargar la información en Supabase. Triple S solo consume y procesa los datos entregados.
- Restricciones de acceso por rol de usuario (sin RBAC). Todos los gerentes ven exactamente la misma información.
- Datos del día en curso (T+0). El sistema opera exclusivamente con jornadas cerradas (datos de T-1 hacia atrás).
- Integración con sistemas ERP, POS o cualquier sistema externo del cliente. La única fuente de datos es Supabase.
- Aplicación móvil nativa. El dashboard es una aplicación web responsiva.
- Modificación de las tablas del cliente (`usr_*`). Triple S opera en modo lectura sobre esas tablas.
- Análisis de rentabilidad con datos externos de mercado o benchmarks de industria.

---

## 9. Supuestos y Restricciones

### Supuestos:
- El cliente tiene acceso a Supabase y puede cargar datos en las tablas `usr_ventas`, `usr_inventario`, `usr_productos` y `usr_sedes` diariamente antes de las 5:30 AM UTC (12:30 AM COT).
- Los datos que el cliente carga corresponden a transacciones reales del almacén, sin duplicados ni manipulaciones externas al sistema del cliente.
- El cliente se compromete a cumplir el contrato de datos definido en la Etapa 1.3 del proyecto como condición de operación del sistema.
- Los cuatro gerentes tienen acceso a internet y a un navegador web moderno para usar el dashboard.
- Las 7 sedes operan bajo el mismo horario (8:00 AM – 6:00 PM COT) sin excepciones relevantes que requieran tratamiento diferenciado en el pipeline.
- El catálogo de productos (~100 SKUs) tiene una tasa de cambio baja y el cliente notifica a Triple S cuando hay altas, bajas o modificaciones significativas.
- El proyecto sigue el modelo de desarrollo por fases y etapas definido en CLAUDE.md, con avance controlado y aprobación explícita del cliente en cada gate.

### Restricciones conocidas:
- **Retraso intencional de 24 horas:** Por diseño del sistema, el dashboard nunca muestra datos del día en curso. Solo jornadas completamente cerradas (T-1). Esta restricción es inamovible y protege la integridad de las métricas.
- **Zona horaria Colombia (UTC-5):** Todo el sistema opera en `America/Bogota`. Las conversiones de UTC a COT son obligatorias en cada capa. No se usan offsets manuales.
- **Tecnología fija:** Python 3.12+ para el pipeline, Next.js + TypeScript para el dashboard, Supabase (PostgreSQL) como base de datos. No está en el alcance evaluar o cambiar el stack tecnológico.
- **Prefijos de tablas no negociables:** Tablas del cliente con prefijo `usr_*` (solo lectura para Triple S); tablas internas con prefijo `tss_*` (propiedad y responsabilidad de Triple S).
- **Sin predicciones:** El sistema no incluirá ningún componente de machine learning ni pronóstico estadístico en ninguna de sus fases.
- **Git Flow obligatorio:** Todo el código sigue el flujo `feat/*` → `dev` → `test` → `prod`. La rama `main` es exclusiva de gobernanza documental.

---

## 10. Puntos Pendientes de Definir

| Punto | Quién debe responder | Impacto si no se resuelve |
|---|---|---|
| Biblioteca de gráficos del dashboard: Recharts vs. Chart.js | Triple S (decisión técnica a tomar en Etapa 3.3) | Cosmético — no afecta funcionalidad ni datos. Debe definirse antes de iniciar la Etapa 3.3. |
| Presupuesto total y cronograma de fases | Cliente (Almacén MultiTodo) y Triple S | Sin definir no se puede comprometer fecha de entrega de Fases 2, 3 y 4. |
| Canal de notificación de alertas internas Triple S | Triple S (decisión operativa) | Si el pipeline falla y no hay canal definido, el equipo no se entera oportunamente. Debe resolverse antes de Etapa 4.1 (producción). |

---

## 11. Próximos Pasos

Este documento es la base acordada del proyecto Dashboard MultiTodo. Al momento de su elaboración, el proyecto se encuentra en **Fase 1 — Etapa 1.2 (Validación de Infraestructura)**, con la Etapa 1.1 (Constitución del Proyecto) completada y el SDD de la Etapa 1.2 aprobado y listo para ejecución.

El camino restante está organizado en cuatro fases y doce etapas:
- **Fase 1 (Gobernanza y Cimientos):** Completar la Etapa 1.2 (infraestructura Supabase) y la Etapa 1.3 (Contrato de Datos).
- **Fase 2 (Ingeniería de Datos):** Construir el pipeline completo desde validación hasta la capa Gold con todas las métricas derivadas.
- **Fase 3 (Analítica y Alertas):** Implementar el análisis exploratorio, el motor de alertas y el dashboard web MVP.
- **Fase 4 (Operación y Mejora Continua):** Desplegar en producción, monitorear y mejorar iterativamente.

Cada etapa requiere orden explícita del cliente para iniciar y produce un Resumen Ejecutivo al cerrar que sirve de gate de avance a la siguiente.

> **Nota:** Este SOW fue elaborado retrospectivamente el 2026-03-24, una vez iniciada la Fase 1. Representa el entendimiento acordado del proyecto en su estado actual. Cualquier cambio de alcance posterior a esta fecha debe documentarse mediante un Control de Cambios (CC) siguiendo el protocolo definido en CLAUDE.md §1.
