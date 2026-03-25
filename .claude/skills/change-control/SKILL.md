---
name: change-control
description: "Gestiona el ciclo de vida completo de Controles de Cambio (CC). USAR SIEMPRE que: (1) se detecte algo necesario no contemplado en los documentos SDD de la etapa activa, o (2) se requiera modificar algo de una etapa ya cerrada. Disparar ante frases como 'esto no está en el spec', 'necesito cambiar algo de la etapa anterior', 'hay un cambio no contemplado', 'change control', 'CC', 'modificar etapa cerrada', o cuando el agente detecte autonomamente que debe hacer algo fuera del alcance documentado."
invocation: user
triggers:
  - control de cambios
  - change control
  - CC
  - cambio no contemplado
  - modificar etapa cerrada
  - esto no esta en el spec
  - no esta documentado
  - necesito cambiar algo de la etapa
---

# Skill: /change-control — Control de Cambios

Eres el guardián de la integridad documental del proyecto **Dashboard MultiTodo**. Tu función es garantizar que ningún cambio no planificado se ejecute sin registro, trazabilidad y aprobación explícita.

> Mandato, triggers y flujo de aprobación de CC: ver **CLAUDE.md §1**.

**Principio rector:** Un cambio sin CC es deuda técnica invisible. Un CC rechazado es igualmente valioso — documenta por qué NO se hizo algo.

---

## Sistema de Estados

```
CREAR  →  [Pendiente]  →  Usuario aprueba  →  [Aprobado]  →  Ejecutar cambios
                      →  Usuario rechaza  →  [No Aprobado]  →  No tocar nada
```

---

## Paso 0 — Identificar el modo

Infiere del contexto qué modo se necesita:

| Modo | Cuándo usarlo |
|---|---|
| `CREATE` | Se detecta un cambio necesario no documentado |
| `APPROVE` | El usuario aprueba un CC en estado Pendiente |
| `REJECT` | El usuario rechaza un CC en estado Pendiente |
| `LIST` | El usuario quiere ver todos los CCs y sus estados |

Si no es claro, pregunta: `¿Qué deseas hacer? CREATE / APPROVE / REJECT / LIST`

---

## MODO CREATE — Registrar un nuevo CC

**Trigger:** El agente detecta que necesita hacer algo fuera del alcance SDD, o el usuario solicita un cambio.

### Paso 1 — Informar la necesidad

Presenta en el chat **antes de crear nada**:

```
🔄 Control de Cambio Requerido

📋 Cambio detectado: [Descripción clara de qué se necesita cambiar]
📍 Tipo: [Cambio en etapa activa / Cambio en etapa cerrada (f[F]_[E])]
🎯 Razón: [Por qué es necesario este cambio]

📂 Documentos afectados:
- [doc 1]: [qué debe cambiar]
- [doc 2]: [qué debe cambiar]

⚠️ Implicaciones:
- [Impacto 1]
- [Impacto 2]

¿Apruebas la creación del Control de Cambio? (sí / no)
```

**Espera respuesta del usuario. No crear el documento hasta recibir confirmación.**

### Paso 2 — Determinar número de CC

Revisa `docs/changes/` para encontrar el último CC creado:
- Si no hay ninguno: el nuevo es `CC_00001`
- Si el último es `CC_00003`: el nuevo es `CC_00004`

### Paso 3 — Crear el documento CC

**Archivo:** `docs/changes/CC_XXXXX.md`

```markdown
# Control de Cambio — CC_XXXXX
**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Estado:** 🟡 Pendiente
**Fecha de creación:** [fecha actual]
**Fecha de resolución:** —
**Solicitado por:** Usuario / Agente IA (detección autónoma)

---

## 1. Descripción del Cambio

[Qué se necesita cambiar, con suficiente detalle para que sea reproducible]

---

## 2. Tipo de Cambio

- [ ] Cambio en etapa activa (algo no contemplado en los docs SDD actuales)
- [ ] Cambio en etapa cerrada (modificación retroactiva)

**Etapa(s) afectada(s):** `f[F]_[E]`

---

## 3. Alcance e Implicaciones

[Qué impacto tiene este cambio en el proyecto. Ser específico y honesto.]

### Riesgos de NO hacer el cambio:
- [Riesgo 1]

### Riesgos de SÍ hacer el cambio:
- [Riesgo 1]

---

## 4. Documentos Afectados

| Documento | Ruta | Cambio Requerido |
|---|---|---|
| [Tipo doc] | `ruta/archivo.md` | [Descripción del cambio] |

---

## 5. Decisión

**Estado:** 🟡 Pendiente aprobación del usuario

| Campo | Valor |
|---|---|
| Aprobado por | — |
| Fecha aprobación | — |
| Razón de rechazo | — |

---

## 6. Registro de Ejecución

> *Se completa únicamente si el CC es Aprobado.*

- [ ] Documentos SDD actualizados
- [ ] Cambios en código/configuración ejecutados
- [ ] Trazabilidad verificada (docs afectados referencian este CC)
- [ ] `/update-index` ejecutado para registrar el cambio
```

### Paso 4 — Confirmar creación

```
✅ CC_XXXXX creado en estado Pendiente: docs/changes/CC_XXXXX.md

Para proceder: ejecuta /change-control → APPROVE CC_XXXXX
Para rechazar: ejecuta /change-control → REJECT CC_XXXXX
```

---

## MODO APPROVE — Aprobar un CC

**Trigger:** Usuario dice "apruebo el CC_XXXXX" o similar.

1. Leer `docs/changes/CC_XXXXX.md`
2. Cambiar estado de `🟡 Pendiente` a `✅ Aprobado` y registrar fecha
3. Confirmar al usuario:
   ```
   ✅ CC_XXXXX aprobado. Procediendo con los cambios...
   ```
4. Ejecutar los cambios descritos en §4 del documento CC
5. En cada documento SDD afectado, añadir al final una nota de trazabilidad:
   ```markdown
   > **Control de Cambio:** Este documento fue modificado por `CC_XXXXX` (fecha).
   ```
6. Actualizar §6 del CC marcando las tareas completadas
7. Informar cierre:
   ```
   ✅ CC_XXXXX ejecutado completamente.
   Documentos actualizados: [lista]
   ```

---

## MODO REJECT — Rechazar un CC

**Trigger:** Usuario dice "rechazo el CC_XXXXX" o "no apruebo el cambio".

1. Leer `docs/changes/CC_XXXXX.md`
2. Cambiar estado a `❌ No Aprobado`
3. Registrar en §5 la razón del rechazo (preguntar al usuario si no la dio)
4. **No tocar ningún otro archivo**
5. Confirmar:
   ```
   ❌ CC_XXXXX marcado como No Aprobado. Ningún cambio fue ejecutado.
   Razón registrada: [razón]
   ```

---

## MODO LIST — Ver todos los CCs

**Trigger:** Usuario quiere ver el estado de los controles de cambio.

1. Escanear `docs/changes/` para todos los archivos `CC_*.md`
2. Leer el estado de cada uno
3. Presentar tabla:

```
📋 Controles de Cambio — Dashboard MultiTodo

| CC | Descripción breve | Estado | Fecha |
|---|---|---|---|
| CC_00001 | ... | ✅ Aprobado | 2026-03-21 |
| CC_00002 | ... | 🟡 Pendiente | 2026-03-22 |

Total: X CCs | Y Aprobados | Z Pendientes | W No Aprobados
```

Si no hay CCs: `No hay Controles de Cambio registrados en este proyecto.`

---

## Reglas de Calidad

1. **Nunca ejecutar sin CC aprobado:** Si el agente detecta autónomamente la necesidad de un cambio, SIEMPRE pausa y lanza el modo CREATE antes de tocar cualquier archivo.
2. **Trazabilidad bidireccional:** El CC referencia los docs afectados. Los docs afectados referencian el CC. Ambas direcciones son obligatorias.
3. **CCs rechazados son permanentes:** No se eliminan. Son registro histórico de decisiones.
4. **Un CC por cambio:** No agrupar cambios no relacionados en un solo CC. Si hay dos cambios independientes, crear dos CCs.
