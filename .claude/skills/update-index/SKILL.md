---
name: update-index
description: "Crea o actualiza PROJECT_index.md con el estado macro del proyecto (fase activa, hitos, rutas críticas e índice SDD). USAR SIEMPRE que el usuario quiera registrar avance, inicializar el índice, o pregunte en qué etapa está el proyecto. También disparar ante frases como '¿en qué fase estamos?', 'actualiza el mapa', 'cerramos la etapa', 'registra el avance', 'update the index', 'where are we in the project', o cualquier señal de que el usuario quiere ubicar o actualizar el estado macro del proyecto."
invocation: user
triggers:
  - PROJECT_index
  - project index
  - estado del proyecto
  - en qué etapa estamos
  - en qué fase estamos
  - actualiza el mapa
  - registra el avance
  - cerramos la etapa
  - inicializa el índice
  - update the index
  - where are we
---

# Skill: /update-index

Tu objetivo es crear o actualizar el archivo `PROJECT_index.md` en la raíz del proyecto. Este archivo es el **MAPA MACRO** del proyecto: define dónde estamos a gran escala y actúa como índice de los documentos SDD gobernantes.

---

## Paso 1 — Leer contexto base

Lee los siguientes archivos en este orden:
1. `CLAUDE.md` — para entender las fases, etapas, convención de nombres SDD y estructura del proyecto.
2. `PROJECT_index.md` — si existe, léelo completo para entender el estado actual antes de modificarlo.

---

## Paso 2 — Explorar el estado real del repositorio

Ejecuta las siguientes exploraciones **en paralelo**:
- Lista los archivos en `docs/reqs/`, `docs/specs/`, `docs/plans/` y `docs/tasks/` para identificar qué documentos SDD ya existen.
- Lista la estructura de carpetas raíz para confirmar qué componentes (`pipeline/`, `web/`, etc.) ya han sido creados.
- Revisa el historial git reciente (`git log --oneline -10`) para inferir qué trabajo se ha completado.

**Inferencia de fase activa:** Si `PROJECT_index.md` no existe o no tiene la fase definida, infiere la fase/etapa activa a partir de los documentos SDD encontrados. El documento SDD más reciente o de mayor numeración indica la etapa en curso. Menciona tu inferencia al usuario para que confirme.

---

## Paso 3 — Preguntar al usuario (máximo 3 preguntas)

Con base en lo que encontraste, pregúntale al usuario **solo lo que no puedas inferir con confianza**:

1. **Fase y etapa activa:** Solo pregunta si no puedes inferirla de los docs SDD existentes o del historial git.
2. **Hitos completados:** Muéstrale la lista de hitos de la fase actual (según CLAUDE.md) y pídele que confirme cuáles están ✅ y cuáles ⬜. No preguntes desde cero — deja que corrija tu propuesta.
3. **Notas o decisiones:** "¿Hay alguna decisión o contexto importante que deba quedar registrado?"

Si puedes inferir algo con confianza, hazlo y preséntalo como propuesta — no como pregunta.

---

## Paso 4 — Mostrar preview y escribir PROJECT_index.md

Muestra al usuario un resumen breve de lo que vas a escribir:
- Si es **creación nueva:** "Voy a crear `PROJECT_index.md` con Fase [X] Etapa [Y] activa."
- Si es **actualización:** "Voy a actualizar `PROJECT_index.md`. Cambios: [lista concisa]."

**Si el usuario invocó esta skill explícitamente (`/update-index` o equivalente), escribe el archivo de inmediato sin esperar confirmación adicional.**
Solo pide confirmación si hay ambigüedad real sobre la fase activa o los hitos.

Usa exactamente la siguiente estructura:

```markdown
# 🗺️ PROJECT_index — Dashboard MultiTodo

> **MANDATO IA:** Lee este archivo en el Paso 2 del Protocolo de Inicio de Sesión. Úsalo para ubicar los documentos SDD activos y entender el estado macro del proyecto. Actualiza el checklist de hitos SOLO cuando el usuario apruebe el cierre de una tarea mayor.

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase [N] — [Nombre de la Fase]`
- **Etapa Activa:** `Etapa [N.N] — [Nombre de la Etapa]`
- **Capa Medallón Activa:** `[Bronze / Silver / Gold / N/A]`
- **Documentos SDD Gobernantes:** Leer obligatoriamente antes de tomar decisiones arquitectónicas:
  - PRD:    `docs/reqs/f[F]_[E]_prd.md`
  - SPEC:   `docs/specs/f[F]_[E]_spec.md`
  - Plan:   `docs/plans/f[F]_[E]_plan.md`
  - Tareas: `docs/tasks/f[F]_[E]_task.md`

---

## 🏁 2. Hitos de la Fase Actual

<!-- Marca ✅ solo cuando el usuario apruebe explícitamente el cierre del hito -->
- [✅ / ⬜] [N.N] [Descripción del hito]
- [✅ / ⬜] [N.N] [Descripción del hito]
- [✅ / ⬜] [N.N] [Descripción del hito]

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Orquestador Pipeline | `pipeline/main.py` | [Existe / Pendiente] |
| Configuración Global | `pipeline/config.yaml` | [Existe / Pendiente] |
| Pipelines | `pipeline/pipelines/` | [Existe / Pendiente] |
| Lógica Atómica (src) | `pipeline/src/` | [Existe / Pendiente] |
| Dashboard Web | `web/` | [En progreso / Pendiente] |
| Requerimientos (reqs) | `docs/reqs/` | [Existe / Pendiente] |
| Especificaciones (specs) | `docs/specs/` | [Existe / Pendiente] |
| Planes (plans) | `docs/plans/` | [Existe / Pendiente] |
| Tareas (tasks) | `docs/tasks/` | [Existe / Pendiente] |

---

## 📚 4. Índice de Documentos SDD

<!-- Lista todos los documentos SDD que existen en docs/reqs/, docs/specs/, docs/plans/ y docs/tasks/, agrupados por fase/etapa -->

### Fase 1 — Gobernanza y Cimientos
| Documento | Ruta | Estado |
|---|---|---|
| PRD Etapa 1.1 | `docs/reqs/f01_01_prd.md` | [Existe / Pendiente] |
| SPEC Etapa 1.1 | `docs/specs/f01_01_spec.md` | [Existe / Pendiente] |
| Plan Etapa 1.1 | `docs/plans/f01_01_plan.md` | [Existe / Pendiente] |
| Tareas Etapa 1.1 | `docs/tasks/f01_01_task.md` | [Existe / Pendiente] |

<!-- Repite el bloque para cada fase/etapa que tenga documentos existentes o en progreso -->

---

## 📝 5. Notas y Decisiones Registradas

<!-- Decisiones de arquitectura, cambios de rumbo o contexto importante que no está en el código -->
- [Fecha] [Nota o decisión]
```

---

## Paso 5 — Confirmación final

Tras escribir el archivo:
1. Confirma: "`PROJECT_index.md` [creado / actualizado] correctamente."
2. Muestra las coordenadas actuales (Fase, Etapa) en una línea para confirmación visual rápida.
3. **No** actualices `PROJECT_handoff.md` — ese archivo es responsabilidad exclusiva del Protocolo de Cierre de Sesión.
