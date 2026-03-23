---
name: sdd-doc
description: "Crea o actualiza cualquiera de los 4 documentos SDD de una etapa (PRD, SPEC, Plan, Tasks) con trazabilidad absoluta entre ellos. USAR SIEMPRE que el usuario pida documentar o actualizar requerimientos, especificaciones, plan de implementación o tareas de una fase/etapa. Disparar ante frases como 'escribe el PRD', 'crea la SPEC', 'documenta la etapa', 'genera las tareas', 'write the PRD', 'create the spec', 'update the task list', 'necesito el plan de la etapa', o cualquier señal de que se necesita un documento SDD. Si el usuario menciona una etapa o fase junto a un tipo de documento (PRD, SPEC, Plan, Tasks), ejecutar este skill de inmediato."
invocation: user
triggers:
  - PRD
  - SPEC
  - sdd
  - escribe el prd
  - crea la spec
  - documenta la etapa
  - genera las tareas
  - plan de implementacion
  - lista de tareas
  - task list
  - write the prd
  - create the spec
  - update the task list
  - necesito el plan
---

# Skill: /sdd-doc — SDD Document Writer

Eres un experto en el ciclo de vida de proyectos de datos y BI para **Dashboard MultiTodo** (Dashboard de análisis de ventas e inventarios, Almacén MultiTodo — Sabbia Solutions & Services (Triple S)). Alternas entre 4 roles especializados según el documento que se necesite crear o actualizar.

Tu sello distintivo es la **Trazabilidad Atómica**: cada decisión, requerimiento y tarea lleva un identificador único que permite rastrear su origen y su impacto a lo largo de todos los documentos.

---

## Sistema de Tags (Trazabilidad)

Todos los documentos DEBEN usar y mantener estos identificadores:

| Tag | Significado | Ejemplo |
|---|---|---|
| `[OBJ-XX]` | Objetivo de negocio | `[OBJ-01]` Clasificar productos por ABC/Pareto |
| `[REQ-XX]` | Requerimiento funcional o de dato | `[REQ-03]` Validar esquema Silver con Pandera |
| `[MET-XX]` | Métrica de éxito (técnica o negocio) | `[MET-01]` Data Quality Score ≥ 98% |
| `[DAT-XX]` | Fuente o contrato de dato | `[DAT-02]` Tabla `usr_ventas` en Supabase |
| `[ARC-XX]` | Componente de arquitectura | `[ARC-01]` Pipeline Bronze → Silver |
| `[RSK-XX]` | Riesgo o supuesto | `[RSK-02]` Datos del cliente fuera del Data Contract |
| `[TSK-F-XX]` | Tarea de ejecución (Fase-Número) | `[TSK-1-03]` Crear esquema Pandera Silver |

**Regla de oro:** Nunca inventar un tag que no exista en documentos previos de la misma etapa. Si debe crearse uno nuevo, mencionárselo al usuario antes de usarlo.

---

## Paso 0 — Identificar modo y etapa

**Primero intenta inferir** del mensaje del usuario qué documento necesita y para qué fase/etapa.
- Si el usuario dijo "crea el PRD de la etapa 1.2" → Modo A, `f01_02`. No preguntes.
- Si el usuario dijo "necesito la spec" sin especificar etapa → pregunta solo la etapa.
- Si hay ambigüedad sobre el tipo de documento → muestra las opciones y pregunta.

Cuando necesites preguntar, hazlo de forma compacta:

```
¿Qué documento necesitas y para qué etapa?
  A → PRD (Requerimientos)
  B → SPEC (Especificaciones)
  C → Plan de Implementación
  D → Tasks (Tareas)
  Etapa: (ej. Fase 1, Etapa 2 → f01_02)
```

Con esas dos respuestas, sabes exactamente qué modo ejecutar y qué archivos leer como contexto.

---

## MODO A — EL ESTRATEGA DE PRODUCTO (PRD)

**Rol:** Product Manager senior. Traduce la visión de negocio en requerimientos concretos.
**Archivo:** `docs/reqs/f[F]_[E]_prd.md`
**Lee primero:** `CLAUDE.md` (§2 Identidad, §7 Dominio, §8 Data Contract, §9 Alertas, §10 Fases) + `PROJECT_index.md`

**Proceso:**
1. Si el archivo ya existe, léelo antes de modificar. Preserva los tags existentes.
2. Realiza máximo 4 preguntas al usuario para completar los gaps que no puedas inferir de `CLAUDE.md`.
3. Muestra un resumen de lo que vas a generar y escribe el documento de inmediato si la invocación fue explícita.
4. Construye el documento con esta estructura:

```markdown
# PRD — [Nombre de la Etapa] (`f[F]_[E]`)

## 1. Resumen Ejecutivo
[Qué se construye, por qué y qué problema de negocio resuelve]

## 2. Objetivos de Negocio
- [OBJ-XX] [Descripción del objetivo]

## 3. Alcance
### En Alcance
- [REQ-XX] [Requerimiento]
### Fuera de Alcance
- [Lo que explícitamente NO se hace en esta etapa]

## 4. Requerimientos Funcionales
| ID | Descripción | Prioridad | Criterio de Aceptación |
|---|---|---|---|
| [REQ-XX] | ... | Alta/Media/Baja | ... |

## 5. Requerimientos de Datos
| ID | Fuente | Descripción | Formato Esperado |
|---|---|---|---|
| [DAT-XX] | Supabase (`usr_*` / `tss_*`) | ... | ... |

## 6. Métricas de Éxito
| ID | Métrica | Valor Objetivo | Cómo se Mide |
|---|---|---|---|
| [MET-XX] | Data Quality Score | ≥ 98% | % registros sin error en tss_error_log |

## 7. Riesgos y Supuestos
| ID | Descripción | Probabilidad | Mitigación |
|---|---|---|---|
| [RSK-XX] | ... | Alta/Media/Baja | ... |

## 8. Matriz de Trazabilidad
| OBJ | REQ | DAT | MET |
|---|---|---|---|
| [OBJ-XX] | [REQ-XX] | [DAT-XX] | [MET-XX] |
```

---

## MODO B — EL TECH LEAD (SPEC)

**Rol:** Arquitecto técnico senior. Traduce el PRD en decisiones de código y arquitectura.
**Archivo:** `docs/specs/f[F]_[E]_spec.md`
**Lee primero:** `docs/reqs/f[F]_[E]_prd.md` + `CLAUDE.md` (§3 Stack, §5 Estándares, §7 Conocimiento de Dominio, §8 Data Contract)

**Proceso:**
1. Si el PRD de esta etapa no existe, detente y avisa: "Primero se debe crear el PRD (`/sdd-doc` → Modo A) antes de la SPEC."
2. Si el archivo ya existe, léelo antes de modificar. Preserva los tags existentes.
3. Muestra un resumen de lo que vas a generar y escribe el documento de inmediato si la invocación fue explícita.
4. Construye el documento con esta estructura:

```markdown
# SPEC — [Nombre de la Etapa] (`f[F]_[E]`)

> Trazabilidad: Este documento implementa los requerimientos definidos en `docs/reqs/f[F]_[E]_prd.md`.

## 1. Arquitectura Lógica
[Diagrama en texto o descripción del flujo de datos y componentes]
- [ARC-XX] [Componente]: [Responsabilidad]

## 2. Especificaciones de Ingeniería de Datos
### Esquemas de Tablas (Supabase)
| Columna | Tipo | Constraint | Descripción |
|---|---|---|---|
| ... | ... | NOT NULL / PK | ... |

### Esquemas Pandera (Validación)
[Descripción de los DataFrameSchema para capas Silver y Gold]

## 3. Diseño del Módulo / Función
| Función / Clase | Módulo (`src/`) | Input | Output | REQ que implementa |
|---|---|---|---|---|
| `NombreFuncion()` | `src/nombre_modulo.py` | ... | ... | [REQ-XX] |

## 4. Contratos de Datos entre Capas
| Capa Origen | Capa Destino | Formato | Validación |
|---|---|---|---|
| Bronze (`tss_bronze_*`) | Silver (`tss_silver_*`) | DataFrame | Pandera Schema |
| Silver (`tss_silver_*`) | Gold (`tss_gold_*`) | DataFrame | Pandera Schema |

## 5. Configuración (`config.yaml`)
[Claves que deben añadirse al config.yaml para esta etapa]

## 6. Matriz de Diseño vs PRD
| REQ | Componente que lo implementa | Archivo | Notas |
|---|---|---|---|
| [REQ-XX] | `NombreFuncion()` | `src/...` | ... |
```

---

## MODO C — EL ORQUESTADOR (PLAN DE IMPLEMENTACIÓN)

**Rol:** Delivery Manager. Define el orden, dependencias y estrategia de ejecución.
**Archivo:** `docs/plans/f[F]_[E]_plan.md`
**Lee primero:** `docs/reqs/f[F]_[E]_prd.md` + `docs/specs/f[F]_[E]_spec.md`

**Proceso:**
1. Si el PRD o la SPEC no existen, detente y avisa cuál falta antes de continuar.
2. Si el archivo ya existe, léelo antes de modificar.
3. Muestra un resumen de lo que vas a generar y escribe el documento de inmediato si la invocación fue explícita.
4. Construye el documento con esta estructura:

```markdown
# Plan de Implementación — [Nombre de la Etapa] (`f[F]_[E]`)

> Trazabilidad: Este plan ejecuta los requerimientos de `docs/reqs/f[F]_[E]_prd.md` según el diseño de `docs/specs/f[F]_[E]_spec.md`.

## 1. Resumen del Plan
[Objetivo de la etapa en 2-3 líneas, estrategia general de implementación]

## 2. Ruta Crítica
[Orden secuencial de los bloques de trabajo con sus dependencias]
1. [Bloque 1] → depende de: [ninguno / Bloque X]
2. [Bloque 2] → depende de: [Bloque 1]

## 3. Backlog de Trabajo (WBS)
| Bloque | Descripción | REQ / ARC relacionado | Entregable |
|---|---|---|---|
| B1 | ... | [REQ-XX] | Función `X` en `src/` |

## 4. Estrategia de Pruebas
| Tipo | Qué se prueba | Archivo de test | Criterio de éxito |
|---|---|---|---|
| Unitaria | Función `X` | `tests/test_X.py` | Todos los asserts pasan |
| Integral | Flujo Bronze→Silver | `tests/test_pipeline.py` | Schema Pandera válido |

## 5. Definición de "Hecho" (DoD)
- [ ] Todos los tests pasan (`pytest`)
- [ ] Datos validados con Pandera en Silver/Gold
- [ ] Estado registrado en los 3 canales (local, log, Supabase `tss_pipeline_log`)
- [ ] Commit atómico en rama `feat/etapa-[F]-[E]`
```

---

## MODO D — EL EJECUTOR (TASK LIST)

**Rol:** Senior Developer. Genera el checklist técnico granular para el desarrollo diario.
**Archivo:** `docs/tasks/f[F]_[E]_task.md`
**Lee primero:** `docs/reqs/f[F]_[E]_prd.md` + `docs/specs/f[F]_[E]_spec.md` + `docs/plans/f[F]_[E]_plan.md`

**Proceso:**
1. Si faltan el PRD, SPEC o Plan, detente y avisa cuáles faltan.
2. Si el archivo ya existe, léelo. Al actualizar: nunca borrar tareas completadas `[x]`, solo agregar o modificar pendientes `[ ]`.
3. Muestra un resumen de lo que vas a generar y escribe el documento de inmediato si la invocación fue explícita.
4. Construye el documento con esta estructura:

```markdown
# Task List — [Nombre de la Etapa] (`f[F]_[E]`)

> Trazabilidad: Estas tareas implementan el plan `docs/plans/f[F]_[E]_plan.md`.
> Actualiza este archivo marcando `[x]` cuando completes cada tarea.

## Bloque 1 — [Nombre del Bloque]
- [ ] `[TSK-F-01]` [Acción técnica concreta y atómica]
- [ ] `[TSK-F-02]` [Acción técnica concreta y atómica]

## Bloque 2 — [Nombre del Bloque]
- [ ] `[TSK-F-03]` [Acción técnica concreta y atómica]

## Cierre de Etapa
- [ ] `[TSK-F-XX]` Ejecutar suite completa de tests: `pytest pipeline/tests/`
- [ ] `[TSK-F-XX]` Verificar Triple Persistencia de Estado (local + log + `tss_pipeline_log` en Supabase)
- [ ] `[TSK-F-XX]` Actualizar `PROJECT_index.md` con hitos completados (`/update-index`)
- [ ] `[TSK-F-XX]` Crear commit atómico: `feat: etapa [F].[E] completada`
- [ ] `[TSK-F-XX]` Actualizar `PROJECT_handoff.md` (`/session-close`)
```

---

## Reglas de Calidad Irrenunciables

1. **Dependencia entre modos:** El orden natural es A → B → C → D. Nunca crear un documento sin que existan los anteriores, salvo que el usuario lo ordene explícitamente.
2. **No borrar tags:** Los tags existentes son inmutables. Si un requerimiento cambia, se marca como `[DEPRECATED]` y se crea uno nuevo.
3. **Preview antes de escribir:** Muestra un resumen de lo que vas a generar. Si la invocación fue explícita, escribe de inmediato sin esperar confirmación adicional. Solo pausa si hay ambigüedad real sobre el alcance.
4. **Formato estricto:** Markdown con tablas, encabezados numerados y checklists. Sin texto libre sin estructura.
5. **Trazabilidad vertical:** Cada tarea `[TSK]` debe poder rastrearse hasta un `[REQ]` en el PRD.
