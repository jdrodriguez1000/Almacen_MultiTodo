---
name: session-close
description: "Ejecuta el protocolo de cierre de sesión reescribiendo PROJECT_handoff.md con el estado táctico exacto del momento. USAR SIEMPRE que el usuario indique fin de sesión, ya sea explícitamente ('Terminamos', 'Cerramos', 'Hasta luego', 'Eso es todo', 'Listo por hoy', 'Done', 'Bye', 'That's it') o implícitamente (despedida, resumen de lo que se hizo, pregunta sobre qué falta). No esperar a que el usuario diga la palabra exacta — ante cualquier señal de cierre, ejecutar este protocolo de inmediato."
invocation: user
triggers:
  - terminamos
  - cerramos
  - hasta luego
  - fin de sesión
  - eso es todo
  - listo por hoy
  - done for today
  - that's it
  - bye
  - nos vemos
  - PROJECT_handoff
  - handoff
---

# Skill: /session-close

Tu objetivo es reescribir `PROJECT_handoff.md` en la raíz del proyecto con el estado táctico exacto del momento en que se cierra la sesión. Este archivo es la **LUPA MICRO** del proyecto: define qué estaba pasando justo antes de cerrar, para que la próxima sesión arranque con precisión láser sin preguntas.

---

## Paso 1 — Identificar Fase y Etapa actual

Lee `PROJECT_index.md` para extraer la **Fase y Etapa activa** (ej. `Fase 1 — Etapa 1.1`).
Si el archivo no existe o no tiene la fase definida, escribe `Por definir`.

---

## Paso 2 — Reconstruir el estado de la sesión

Analiza la conversación completa de esta sesión para extraer:

- **Archivos tocados:** ¿Qué archivos se leyeron, crearon o modificaron durante esta sesión?
- **Contexto inmediato:** ¿Qué lógica, función o problema se estaba trabajando en los últimos mensajes?
- **Último error o bloqueador:** ¿Hubo algún error de consola, test fallido, o decisión abierta sin resolver? Clasifícalo en una de tres categorías:
  - *Error activo:* pegar el mensaje exacto.
  - *Decisión pendiente:* describir qué quedó abierto y las opciones disponibles.
  - *Cierre limpio:* no hubo bloqueador.
- **Próxima acción:** La tarea atómica más pequeña y concreta que debe ejecutarse al inicio de la próxima sesión. Debe ser tan específica que un agente pueda ejecutarla sin preguntar nada.

---

## Paso 3 — Mostrar resumen y escribir el archivo

Muestra un resumen breve en el chat:

```
Cerrando sesión:
- Fase/Etapa: [fase y etapa]
- Archivos activos: [lista]
- Contexto: [1-2 líneas]
- Bloqueador: [descripción o "Ninguno"]
- Próxima acción: [tarea concreta]
```

**Si el usuario ya dio una señal clara de cierre (despedida, "terminamos", "listo"), escribe `PROJECT_handoff.md` de inmediato sin esperar confirmación adicional.**
Solo pide confirmación si hay ambigüedad real sobre el estado del trabajo.

Usa exactamente la siguiente estructura:

```markdown
# PROJECT_handoff — Bitácora de Cambio de Sesión

> **MANDATO IA:** Este es el estado mental exacto donde se pausó el trabajo. Léelo en el Paso 3 del Protocolo de Inicio de Sesión para retomar la acción táctica de inmediato.

---

## Punto de Guardado

- **Última actualización:** [Fecha completa, hora aproximada]
- **Fase / Etapa:** `Fase [N] — Etapa [N.N]`

---

## Archivos en el Escritorio (Working Set)

- `[ruta/archivo_1]` — [qué se hizo o por qué es relevante]
- `[ruta/archivo_2]` — [qué se hizo o por qué es relevante]

---

## Contexto Inmediato

[2-4 líneas describiendo exactamente qué se estaba pensando, construyendo o discutiendo al momento del cierre. Suficiente detalle para que un agente retome sin preguntas.]

---

## Bloqueador / Último Error

[Una de estas tres opciones según aplique:]
- Error activo: pegar el mensaje exacto de consola o describir el bug.
- Decisión pendiente: describir qué decisión quedó abierta y qué opciones hay.
- Ninguno — la sesión cerró en estado limpio.

---

## Proxima Accion Inmediata

1. [Acción atómica y concreta — suficientemente específica para ejecutarla sin preguntar]
2. [Segunda acción si aplica]
3. [Tercera acción si aplica]
```

---

## Paso 4 — Actualizar Lecciones Aprendidas

Tras escribir `PROJECT_handoff.md`, actualiza `docs/lessons/lessons-learned.md`:

1. Lee el archivo de lecciones. Si no existe, créalo con la estructura base del proyecto.
2. Localiza la sección de la **Fase y Etapa activa** (ej. `## Fase 1 — Etapa 1.1`). Si no existe la sección, créala.
3. Añade una nueva entrada de sesión con esta estructura:

```markdown
### Sesión: [fecha actual]

**✅ Lo que funcionó bien:**
- [Extrae de la conversación qué decisiones, herramientas o enfoques resultaron positivos]

**⚠️ Lo que no funcionó / fricción encontrada:**
- [Errores, malentendidos, pasos que hubo que repetir, decisiones que se revirtieron]

**💡 Decisiones clave tomadas:**
- [Decisiones de diseño, arquitectura o gobernanza que no estaban documentadas previamente]
```

4. Si la sesión cierra una etapa completa (todas las tareas en `[x]`), añade también:

```markdown
### 📋 Resumen de la Etapa
**Lecciones más valiosas:**
1. [Lección 1 — la más importante para etapas futuras]
2. [Lección 2]
3. [Lección 3]
```

---

## Paso 5 — Confirmación final

Tras completar ambos pasos:
1. Confirma: "`PROJECT_handoff.md` y `lessons-learned.md` actualizados."
2. Muestra en una línea la Próxima Acción registrada para que el usuario la tenga visible al cerrar.
