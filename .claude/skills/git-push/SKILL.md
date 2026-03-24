---
name: git-push
description: "Sube el repositorio a GitHub respetando el Git Flow del proyecto (feat/* → dev → test → prod). Maneja tanto la configuración inicial del remoto como pushes de ramas individuales. USAR cuando el usuario quiera subir código a GitHub, configurar el remoto por primera vez, o seguir el flujo de ramas definido en CLAUDE.md §6. Disparar ante frases como 'sube a GitHub', 'push', 'subir al repositorio', 'configura el remoto', 'publicar rama'."
invocation: user
triggers:
  - git push
  - push
  - subir a github
  - sube a github
  - subir al repositorio
  - publicar rama
  - configurar remoto
  - setup github
  - desde cero
---

# Skill: /git-push

Gestiona el push al repositorio GitHub respetando estrictamente el **Git Flow de Triple S** definido en `CLAUDE.md §6`.

---

## Reglas de Oro (leer antes de ejecutar cualquier paso)

```
main   → Rama de GOBERNANZA. Solo docs SDD, ejecutivos, CLAUDE.md.
         NUNCA código ejecutable. NUNCA merge desde feat/dev/test/prod.

prod   → Rama de código en PRODUCCIÓN visible para el cliente.
         Solo recibe merges desde dev (después del ciclo test → dev → prod).

test   → Rama de pruebas. NUNCA hace merge directo a prod.
         Flujo obligatorio: test → dev → prod.

dev    → Rama de integración. Recibe feat/* y arreglos de test.

feat/* → Ramas de desarrollo individual. Merge hacia dev únicamente.
```

**Flujo único permitido:** `feat/*` → `dev` → `test` → `dev` (sincronizar arreglos) → `prod`

---

## Paso 1 — Diagnóstico del repositorio

Ejecuta los siguientes comandos para entender el estado actual:

```bash
git remote -v
git branch -a
git status
git log --oneline -5
```

Con base en los resultados, determina:

- **¿Existe el remoto `origin`?** → Si no existe, ir a **Paso 2A**. Si existe, ir a **Paso 2B**.
- **¿Qué rama está activa?** → Validar contra las reglas de oro antes de cualquier push.
- **¿Hay cambios sin commitear?** → Si los hay, alertar al usuario y detenerse. No hacer push con working tree sucio.

---

## Paso 2A — Configuración inicial (remoto no existe)

> Usar cuando el repositorio nunca ha sido subido a GitHub.

**2A.1 — Solicitar URL del repositorio:**

Pregunta al usuario:
```
¿Cuál es la URL del repositorio GitHub?
Ejemplo: https://github.com/usuario/nombre-repo.git
```

**2A.2 — Agregar el remoto:**

```bash
git remote add origin [URL_PROPORCIONADA]
```

**2A.3 — Verificar y crear ramas requeridas:**

El proyecto necesita 4 ramas permanentes. Verifica cuáles existen localmente y crea las que falten:

```bash
# Verificar ramas existentes
git branch

# Crear rama dev si no existe (basada en main)
git checkout -b dev

# Crear rama test si no existe (basada en dev)
git checkout -b test

# Crear rama prod si no existe (basada en dev)
git checkout -b prod

# Volver a main
git checkout main
```

> Solo crear las ramas que realmente no existan. No recrear las que ya están.

**2A.4 — Push inicial de todas las ramas:**

Solicita confirmación explícita antes de cada push:

```
Estoy por subir las siguientes ramas a GitHub origin:
  → main  (gobernanza: CLAUDE.md, docs SDD, ejecutivos)
  → dev   (integración)
  → test  (pruebas)
  → prod  (producción cliente)

¿Confirmas?
```

Si confirma, ejecutar en orden:

```bash
git push -u origin main
git push -u origin dev
git push -u origin test
git push -u origin prod
```

---

## Paso 2B — Push a repositorio ya configurado

> Usar cuando `origin` ya existe.

**2B.1 — Identificar la rama activa y validar el flujo:**

| Rama activa | Acción permitida | Advertencia |
|---|---|---|
| `main` | Push directo | Solo si los cambios son documentación/gobernanza |
| `feat/*` | Push a `feat/*` remota | Normal — rama de trabajo |
| `dev` | Push a `dev` remota | Normal — integración |
| `test` | Push a `test` remota | Normal — pruebas |
| `prod` | Push a `prod` remota | **ALERTA:** Verificar que `dev` está sincronizado primero |

**2B.2 — Caso especial: push hacia `prod`**

Si la rama activa es `prod` o el usuario quiere mergear `test → prod`, ejecutar el flujo obligatorio:

```
⚠️  FLUJO OBLIGATORIO ANTES DE ACTUALIZAR PROD:

Paso A: Sincronizar arreglos de test hacia dev
  git checkout dev
  git merge test
  git push origin dev

Paso B: Actualizar prod desde dev (NUNCA desde test directamente)
  git checkout prod
  git merge dev
  git push origin prod
```

Mostrar este flujo al usuario y pedir confirmación en cada paso.

**2B.3 — Ejecutar el push:**

```bash
git push origin [rama-activa]
```

Si la rama no tiene upstream configurado, usar:

```bash
git push -u origin [rama-activa]
```

---

## Paso 3 — Verificación post-push

Después de cada push exitoso, ejecutar:

```bash
git log --oneline origin/[rama] -3
git remote show origin
```

Confirmar al usuario:
```
✅ Push completado.
   Rama: [nombre]
   Último commit en remoto: [hash] [mensaje]
   URL: [url del remoto]
```

---

## Paso 4 — Errores comunes y resolución

| Error | Causa | Solución |
|---|---|---|
| `rejected — non-fast-forward` | El remoto tiene commits que no tienes localmente | Ejecutar `git pull origin [rama] --rebase` primero. **Nunca usar `--force` sin confirmar con el usuario.** |
| `fatal: remote origin already exists` | El remoto ya está configurado | Verificar con `git remote -v` y usar la URL existente |
| `error: src refspec [rama] does not match any` | La rama no existe localmente | Crear la rama con `git checkout -b [rama]` primero |
| `Permission denied (publickey)` | Autenticación SSH fallida | Verificar que la clave SSH está configurada en GitHub, o usar HTTPS |

---

## Restricciones absolutas

- **PROHIBIDO** usar `git push --force` o `git push -f` hacia `main`, `prod` o `test` sin aprobación explícita del usuario con advertencia clara del riesgo.
- **PROHIBIDO** hacer merge de `test → prod` directamente. Siempre `test → dev → prod`.
- **PROHIBIDO** pushear a `main` código ejecutable (Python, JS, etc.). Solo gobernanza.
- Si el usuario pide saltarse el flujo, mostrar la advertencia y esperar confirmación antes de proceder.