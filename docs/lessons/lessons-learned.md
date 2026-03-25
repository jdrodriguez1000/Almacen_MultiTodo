# Lecciones Aprendidas — Dashboard MultiTodo

> Registro acumulativo por etapa. Solo leer la sección de la etapa activa al iniciar sesión.
> Actualizado automáticamente por el skill `/session-close` al cierre de cada sesión.

---

## Fase 1 — Gobernanza y Cimientos

### Etapa 1.1 — Constitución del Proyecto

#### Sesión: 2026-03-23

**✅ Lo que funcionó bien:**
- El flujo de bloques (B1→B2→B3→B4→B5) resultó natural y sin fricciones — cada bloque tenía dependencias claras del anterior.
- Las verificaciones intermedias (git status, ls, python main.py) dieron confianza inmediata en cada paso sin overhead.
- Separar `contexto.md` y `temp.md` del repositorio via `.gitignore` antes del primer commit evitó ruido en el historial.
- El spec §2.1 tenía el `.gitignore` exacto listo para copiar — cero decisiones ad-hoc.

**⚠️ Lo que no funcionó / fricción encontrada:**
- El repositorio no estaba inicializado con Git al comenzar la sesión — TSK-1-01 pasó de verificación a inicialización. El task file asumía que ya existía.
- La rama se llamó `master` por defecto (comportamiento de Git en Windows sin configuración global). Se renombró a `main` antes del commit — sin consecuencias pero requirió un paso no documentado.
- Advertencias de LF→CRLF en el commit en Windows. Cosmético, pero puede confundir en futuras sesiones si no se documenta.

**💡 Decisiones clave tomadas:**
- `contexto.md` y `temp.md` excluidos del repositorio por decisión explícita del usuario — no pertenecen al proyecto.
- Git inicializado y configurado en la misma sesión en lugar de asumir existencia previa.
- Rama renombrada de `master` a `main` antes del primer commit para cumplir el workflow del CLAUDE.md §6.

---

### 📋 Resumen de la Etapa 1.1

**Lecciones más valiosas:**
1. **Verificar prerequisitos antes de tareas de verificación:** TSK-1-01 era "verificar que Git está inicializado" pero en realidad fue "inicializar Git". Los task files deben asumir el estado mínimo real del entorno, no el estado ideal.
2. **Configurar `core.autocrlf` en Windows:** Para evitar ruido de LF→CRLF en cada commit en entornos Windows, considerar agregar `.gitattributes` con `* text=auto` en la Etapa 1.2 o un CC.
3. **El spec como fuente de copy-paste:** Tener el contenido exacto de archivos (`.gitignore`, `config.yaml`, `main.py`) en el spec §2.x eliminó toda decisión de implementación — el agente copió, no inventó. Este patrón debe mantenerse en todas las etapas.

---

#### Sesión: 2026-03-23 (continuación)

**✅ Lo que funcionó bien:**
- Verificación estructural paralela (docs/, pipeline/, raíz) en un solo comando `ls` — eficiente y sin fricciones.
- El `.gitignore` protegió correctamente `temp.md`, `contexto.md` y `.env` — ningún archivo sensible llegó al remote.
- Primer push a GitHub sin conflictos: rama `main` configurada como upstream desde el inicio.

**⚠️ Lo que no funcionó / fricción encontrada:**
- El Protocolo de Inicio de Sesión fue omitido por instrucción del usuario — no es un problema técnico pero es una desviación del CLAUDE.md §1 que debe normalizarse en futuras sesiones.

**💡 Decisiones clave tomadas:**
- `.env` creado con placeholders vacíos como punto de entrada documentado — el usuario llena las credenciales reales sin riesgo de exposición.
- `temp.md` eliminado del working directory al confirmar que no era un archivo del proyecto.
- Push a `main` realizado directamente (rama de gobernanza): correcto para Etapa 1.1 que es pura documentación; en Etapa 1.2 el código irá a `feat/*`.

---

### Etapa 1.2 — Validación de Infraestructura

#### Sesión: 2026-03-24

**✅ Lo que funcionó bien:**
- El flujo A→B→C→D del skill `/sdd-doc` fue completamente fluido — cada documento dependió del anterior sin retrocesos.
- Construir el PRD en una sesión separada (el usuario pidió "solo el PRD primero") antes de la SPEC, el Plan y las Tasks fue una buena práctica — permitió revisar el alcance antes de comprometerse con decisiones técnicas.
- La SPEC incluyó DDL completo de las tablas `tss_*` directamente en el documento, eliminando decisiones ad-hoc en el momento de implementar.
- El Plan incluyó protocolos de bloqueador explícitos para `[RSK-01]` y `[RSK-03]` — si ocurren, el agente sabe exactamente qué hacer sin improvisar.
- Separar commits de código (`feat/etapa-1-2`) y documentos SDD (`main`) quedó documentado tanto en el Plan como en las Tasks — cero ambigüedad en el momento de commitear.

**⚠️ Lo que no funcionó / fricción encontrada:**
- Ninguna fricción técnica en esta sesión. Solo documentación — sin ejecución de código ni conexión a Supabase.
- El usuario tuvo que solicitar explícitamente "solo el PRD" antes de que se procediera con ese documento solo — en futuras sesiones de SDD, preguntar si se quiere uno a uno o todos de golpe.

**💡 Decisiones clave tomadas:**
- `supabase_client.py` diseñado como módulo funcional (no clase) — sin estado compartido entre funciones.
- Las tablas `tss_error_log`, `tss_pipeline_log` y `tss_quarantine` se crean en Etapa 1.2 (infraestructura base), no en Fase 2 — decisión de arquitectura con impacto en todas las etapas siguientes.
- `create_tss_tables()` diseñada como idempotente (`CREATE TABLE IF NOT EXISTS`) — el script de infraestructura puede re-ejecutarse sin consecuencias.
- TDD estricto en B2: los 12 tests se escriben todos juntos primero (fase RED), luego implementación función por función (fase GREEN) — mandato documentado en las tareas.

---

#### Sesión: 2026-03-24 (implementación)

**✅ Lo que funcionó bien:**
- El flujo de agentes especializados (python-dev → db-agent) funcionó perfectamente: el python-dev escribió tests e implementó el módulo; el db-agent creó las tablas en Supabase. División de responsabilidades clara y sin solapamiento.
- Los 12 tests de integración contra Supabase real pasaron al 100% en la ejecución final — el ciclo RED→GREEN fue preciso.
- `verify_table_schema()` usando la OpenAPI spec de PostgREST (`/rest/v1/`) fue la solución correcta para consultar columnas sin depender de `information_schema` (no expuesta por PostgREST por defecto).
- La separación de commits por tipo (código a `feat/etapa-1-2`, documentos a `main`) se ejecutó sin fricciones — el working directory limpio al final confirmó que nada quedó sin commitear.
- El usuario detectó proactivamente que los cambios se hacían en `main` — la aclaración fue rápida porque nada estaba commiteado aún.

**⚠️ Lo que no funcionó / fricción encontrada:**
- `create_tss_tables()` vía Management API de Supabase (`api.supabase.com/v1/projects/{ref}/database/query`) respondía con error 544 (timeout). La función no puede crear DDL directamente desde `supabase-py` — requiere el agente db-agent o acceso directo a PostgreSQL.
- `SUPABASE_PROJECT_ID` en `.env` apuntaba al proyecto inactivo `Demo_Bunuelos` en lugar de `Demo_Dashboard`. El error fue silencioso hasta que el db-agent hizo la inspección — no fue detectado por los tests de conectividad porque las credenciales (URL y KEY) ya eran correctas.
- Los tests CRUD limpian (DELETE) después de sí mismos, lo que hace que `tss_pipeline_log` quede vacío al final. La verificación de Triple Persistencia debió ajustar la expectativa: count=0 es correcto en cierre de etapa, no en producción.

**💡 Decisiones clave tomadas:**
- `verify_table_exists()` implementada con captura de `APIError` código `PGRST205` (intentar SELECT en tabla inexistente) en lugar de consultar `information_schema` — más robusto con PostgREST.
- Las tablas `tss_*` deben crearse vía db-agent (MCP de Supabase) en todas las etapas futuras. No intentar DDL desde `supabase-py` — no es el canal correcto.
- Agentes especializados creados y operativos: `db-agent` para Supabase/PostgreSQL, `python-dev` para TDD Python, `project-manager` para gobernanza documental.

### 📋 Resumen de la Etapa 1.2

**Lecciones más valiosas:**
1. **El agente db-agent es el canal correcto para DDL en Supabase:** `supabase-py` no soporta DDL vía PostgREST. Todo `CREATE TABLE`, `ALTER TABLE` o cambio estructural debe ir por db-agent (MCP). Documentar esto en la SPEC de cada etapa que involucre cambios de esquema.
2. **Verificar SUPABASE_PROJECT_ID además de URL y KEY:** El `.env` puede tener las credenciales correctas pero el identificador de proyecto incorrecto. Agregar una verificación explícita del project ID al inicio de sesión cuando el agente db-agent entre en acción.
3. **PostgREST no expone `information_schema` por defecto:** Las consultas de introspección de esquema deben usar la OpenAPI spec de PostgREST (`/rest/v1/`) o captura de errores `PGRST205`, no `information_schema.tables/columns` directamente.

---

### Etapa 1.3 — Data Contract

#### Sesión: 2026-03-24

**✅ Lo que funcionó bien:**
- El flujo A→B→C→D del skill `/sdd-doc` produjo documentos con trazabilidad atómica completa: cada `[REQ-XX]` del PRD tiene componente en la SPEC, bloque en el Plan y tarea en el Task file. La verificación cruzada B3 confirmó 7/7 sin gaps.
- La separación entre etapa de gobernanza (1.3 define) y etapa de implementación (2.1 implementa) evitó scope creep: la SPEC especifica contratos de interfaz, no código ejecutable.
- Combinar `/sdd-doc` (estructura y trazabilidad) con el agente `project-manager` (revisión de consistencia) produjo documentos de mayor calidad que usando solo uno de los dos.
- El agente `db-agent` habilitó RLS en las tablas `tss_*` sin fricción — acción correcta detectada proactivamente a partir del pedido del usuario.
- La verificación documental del Bloque 3 (TSK-1-06 a TSK-1-08) confirmó 16/16 claves de `config.yaml` y 5/5 códigos ERR_MTD completos — el proceso de verificación fue eficiente porque los documentos ya tenían la estructura canónica.

**⚠️ Lo que no funcionó / fricción encontrada:**
- Los primeros borradores de PRD y SPEC fueron generados por el agente `project-manager` sin invocar `/sdd-doc`, lo que produjo etiquetas `RNB-XX` en lugar del sistema estándar `[REQ-XX]`. Ambos documentos debieron reconstruirse. Costo: una iteración adicional sin impacto en el contenido técnico.
- El PRD y `CLAUDE.md §2` dicen "ventana operativa 13:00–23:00 UTC" pero la implementación correcta es `hora_utc ∈ [13, 22]`: la hora 23:00 UTC equivale exactamente a las 18:00 COT (cierre del almacén) y está **fuera** de la ventana. La SPEC tiene la definición precisa; el PRD y CLAUDE.md son una simplificación que puede inducir error al implementar. No se abrió CC porque no hay contradicción de negocio, pero sí hay riesgo de implementación incorrecta si el desarrollador solo lee el PRD.

**💡 Decisiones clave tomadas:**
- `data_contract:` en `config.yaml` como sección propia, separada de `tables:` y `pipeline:` — facilita que el pipeline de Etapa 2.1 cargue solo los parámetros del contrato sin acoplar otras configuraciones.
- `ERR_MTD_004` es el único código con `block_batch` — todos los demás son `quarantine_record`. Esta asimetría es intencional: un dato de T+0 contamina la jornada completa; un SKU inválido solo invalida ese registro.
- Umbral de fallo total fijado en 50%: si más de la mitad del lote es rechazado, es un problema sistémico (no un rechazo normal) y el pipeline escala a `status='failure'`.

---

### 📋 Resumen de la Etapa 1.3

**Lecciones más valiosas:**
1. **Invocar `/sdd-doc` desde el primer documento:** Los documentos generados directamente por el agente sin el skill pierden el sistema de tags estándar (`[REQ-XX]`, `[DAT-XX]`, etc.). Reconstruirlos tiene costo cero en contenido pero costo real en tiempo. La regla es simple: cualquier documento SDD debe pasar por `/sdd-doc`.
2. **La ventana operativa tiene dos definiciones:** El PRD/CLAUDE.md dicen "13:00–23:00 UTC" (simplificación de negocio). La SPEC dice `[13, 22]` (implementación correcta). Al implementar `ERR_MTD_001` en Etapa 2.1, usar la definición de la SPEC: `13 <= hora_utc <= 22`. Nunca usar `hora_utc < 23` — las 23:00 UTC (18:00 COT) ya están fuera de la ventana operativa.
3. **Las etapas de gobernanza pura tienen un artefacto de configuración como parte del DoD:** No solo documentos `.md` — la sección `data_contract:` en `config.yaml` es un entregable concreto y verificable de esta etapa. Incluir siempre la actualización de `config.yaml` en el DoD de etapas que definan contratos o parámetros de comportamiento.

---

## Fase 2 — Ingeniería de Datos e Integración
*(Pendiente de inicio.)*

---

## Fase 3 — Analítica y Alertas
*(Pendiente de inicio.)*

---

## Fase 4 — Operación y Mejora Continua
*(Pendiente de inicio.)*
