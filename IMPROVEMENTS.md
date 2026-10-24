# Mejoras implementadas en Hermespowers

Este archivo resume las mejoras hechas al plugin Superpowers para convertirlo en una versión exclusiva para Hermes Agent, resolviendo los warnings de la comunidad y optando por una arquitectura simplificada.

---

## Contexto

El plugin original `superpowers` fue bloqueado por la comunidad por múltiples warnings de escaneo estático. El encargo fue convertir el checkout en un plugin exclusivo para Hermes, eliminando compatibilidad con otros agentes (Claude, Codex, OpenCode, etc.) y corrigiendo los hallazgos reproducibles.

---

## Mejoras implementadas

### 1. Conversión a Hermes-only

#### 1.1 Eliminación de manifestos y hooks no-Hermes
- **Archivos eliminados**: `.antigravity-plugin`, `.claude-plugin`, `.codex-plugin`, `.cursor-plugin`, `.devin-plugin`, `.kimi-plugin`, `.muse-plugin`, `.opencode`, `.pi`
- **Hooks eliminados**: `hooks/*` (integración multi-harness)
- **Scripts eliminados**: `scripts/package-codex-plugin.sh`, `scripts/sync-to-codex-plugin.sh`, `scripts/render-antigravity-logo.sh`

#### 1.2 Eliminación de tests específicos por harness
- **Tests eliminados**: `tests/antigravity`, `tests/claude-code`, `tests/codex`, `tests/codex-plugin-sync`, `tests/devin`, `tests/kimi`, `tests/opencode`, `tests/pi`
- **Tests retenidos**: `tests/hermes` (suite completa) y `tests/brainstorm-server` (companion visual)

#### 1.3 Actualización de documentación multi-harness
- **Docs eliminados**: `docs/README.kimi.md`, `docs/README.opencode.md`, `docs/porting-to-a-new-harness.md`, `docs/windows/polyglot-hooks.md`
- **Docs retenidos**: `docs/superpowers/specs/` (historia técnica) y `docs/testing.md`
- **README reescrito**: Ahora solo documenta instalación para Hermes

#### 1.4 Actualización de tool mappings en skills
- `skills/using-superpowers/SKILL.md`: Referencias actualizadas a `references/hermes-tools.md`
- Eliminadas referencias a `claude-code-tools.md`, `codex-tools.md`, `pi-tools.md`, `antigravity-tools.md`, `muse-tools.md`

#### 1.5 Servidor visual Hermes-only
- `skills/brainstorming/scripts/server.cjs`: Versión leída de `.hermes-plugin/plugin.yaml`
- Eliminada compatibilidad con `.codex-plugin/plugin.json` y `package.json` como fallback

---

### 2. Hardening de seguridad

#### 2.1 Eliminación de `BRAINSTORM_OPEN_CMD`
- **Problema**:La variable de entorno permitía inyección de comandos shell
- **Solución**: Eliminada la validación y uso de `BRAINSTORM_OPEN_CMD`; el lanzamiento usa exclusivamente ejecutables de plataforma con `execFile` y `argv`
- **Prueba nueva**: `tests/brainstorm-server/lifecycle.test.js` asevera que `BRAINSTORM_OPEN_CMD` no se ejecuta

#### 2.2 Hardening de permisos de tokens
- Archivos `.last-port` y `.last-token`: Permisos restrictivos (0600 en Unix)
- **Comportamiento**: Al arrancar, se normalizan los permisos si están abiertos; si falla la normalización, el server aborta
- **Prueba nueva**: `tests/brainstorm-server/lifecycle.test.js` verifica normalización de permisos

#### 2.3 Restricción de auto-open a loopback
- **Problema**: Auto-open podría enviar el key de sesión a un host remoto malicioso
- **Solución**: Auto-open solo si `BRAINSTORM_URL_HOST` es loopback (`127.0.0.1` o `::1`)
- **Prueba nueva**: `tests/brainstorm-server/lifecycle.test.js` verifica que auto-open no se dispare con URL hosts remotos

#### 2.4 Eliminación de copia no condicional de configuración personal
- **Problema**: `run-haiku-test.sh` copiaba `~/.claude/CLAUDE.md` sin opt-in
- **Solución**: Eliminada la copia automática; se preserva solo si el usuario especifica explícitamente la ruta
- **Prueba nueva**: `tests/explicit-skill-requests/test-run-haiku-safety.sh` asevera el comportamiento seguro

#### 2.5 Política de seguridad documentada
- **Nuevo archivo**: `SECURITY.md`
- **Contenido**: Triaje de hallazgos de scans estáticos, scope, reportedoría y decisiones de hardening

---

### 3. Cobertura de regresión

#### 3.1 Prueba de límite Hermes-only
- **Nuevo archivo**: `tests/hermes/test_hermes_only.py`
- **Pruebas**:
  1. Sin artefactos no-Hermes en shipping (manifestos, dirs, hooks)
  2. README documenta solo instalación Hermes
  3. `using-superpowers` solo referencia tooling de Hermes
  4. Visual companion lee versión desde manifiesto de Hermes

#### 3.2 Suite completa del companion visual
- **Nuevo paquete**: `tests/brainstorm-server/ws` como dependencia de test
- **Suite**: 29 pruebas distribuidas en:
  - `auth.test.js`: Autenticación HTTP y WebSocket
  - `branding.test.js`: Comportamiento de imágenes de branding
  - `browser-launcher.test.js`: Lanzamiento seguro con argv
  - `helper.test.js`: Utilidades de test
  - `lifecycle.test.js`: Timeout inactivo y cierre de WebSocket
  - `server.test.js`: Inicio, parada, warm-restart y persistencia
  - `start-server.test.sh`: Script de inicio (Shell)
  - `stop-server.test.sh`: Script de parada (Shell)
  - `windows-lifecycle.test.sh`: Comportamiento en Windows
  - `ws-protocol.test.js`: Protocolo WebSocket y frame handling

---

### 4. Simplificación de arquitectura

#### 4.1 Eliminación de fallbacks multi-harness
- `package.json`: No se incluye en el distribution bundle (solo para tests de Comandante)
- `index.js`: No se incluye en el distribution bundle (solo para OpenCode)
- `GEMINI.md`: Eliminado (documentación de integración Gemini)

#### 4.2 Consolidación de metadatos
- Versión de plugin leída únicamente de `.hermes-plugin/plugin.yaml`
- Sin fallbacks a `package.json` o `package-lock.json`

#### 4.3 Eliminación de scripts de sincronización y package
- Scripts dedicados a mantener plugins para otros harnesses
- Reducción de superficie de ataque y complejidad

---

### 5. Documentación

#### 5.1 README actualizado
- Posicionamiento como **Hermespowers - Superpowers for Hermes Agent**
- Instalación: `hermes plugins install mtoscan-dev/hermespowers --enable`
- Sin menciones a otros agentes o herramientas
- Instrucciones claras de verificación

#### 5.2 SECURITY.md
- Políticas de triaje para hallazgos de scans estáticos
- Clasificación por riesgo: runtime vs fixtures vs histórico
- Guía para reportar vulnerabilidades sin exponer secretos

#### 5.3 Limpieza de historial
- `RELEASE-NOTES.md`: Preservado como historia técnica, no como guía activa
- `docs/superpowers/specs/`: Preservado como registro de diseño
- Sin referencias activas a integraciones abandonadas

---

### 6. Verificación y tests

#### 6.1 Suite de Hermes
- 29 pruebas en `tests/hermes` (antes 25)
- Cobertura: bootstrap, plugin loader, límite Hermes-only
- Ejecución: `.venv/bin/python -m pytest tests/hermes -q`

#### 6.2 Companion visual
- Suite completa en `tests/brainstorm-server` (antes 0 tests)
- 29 pruebas con cobertura de:
  - Autenticación (HTTP, WebSocket, cookies)
  - Inicio y parada (normal, timeout, fallback)
  - Lifecycle (idle shutdown, persistencia de port y key)
  - Browser launcher (seguridad, argv, loopback-only)

#### 6.3 Hardening verificable
- Pruebas para `BRAINSTORM_OPEN_CMD` no ejecutar
- Pruebas para permisos restringidos de tokens
- Pruebas para `BRAINSTORM_URL_HOST` loopback-only
- Pruebas para copia segura de configuración (opt-in)

---

## Resumen de eliminaciones

| Categoría | Archivos/dirs eliminados | Rationale |
|-----------|--------------------------|-----------|
| Manifestos de otros harnesses | `.antigravity-plugin`, `.claude-plugin`, `.codex-plugin`, `.cursor-plugin`, `.devin-plugin`, `.kimi-plugin`, `.muse-plugin`, `.opencode`, `.pi` | No se distribuyen artefactos no-Hermes |
| Hooks | `hooks/*` | Sin compatibilidad con otros agentes |
| Tests por harness | `tests/antigravity`, `tests/claude-code`, `tests/codex`, `tests/codex-plugin-sync`, `tests/devin`, `tests/kimi`, `tests/opencode`, `tests/pi` | Tests Hermes-only |
| Docs por harness | `docs/README.kimi.md`, `docs/README.opencode.md`, `docs/porting-to-a-new-harness.md`, `docs/windows/polyglot-hooks.md` | Docs Hermes-only |
| Scripts multi-harness | `scripts/package-codex-plugin.sh`, `scripts/sync-to-codex-plugin.sh`, `scripts/render-antigravity-logo.sh` | Scripts Hermes-only |
| Fallbacks meta | `package.json`, `index.js`, `GEMINI.md` | Versión desde `.hermes-plugin/plugin.yaml` |

---

## Resumen de mejoras de hardening

| Hallazgo | Riesgo | Solución | Prueba |
|----------|--------|----------|--------|
| `BRAINSTORM_OPEN_CMD` | Inyección de commandos shell | Eliminado; usar `execFile` con `argv` | `lifecycle.test.js` |
| Permisos abiertos de tokens | exposición de sesión | Normalización a 0600 en startup | `lifecycle.test.js` |
| Auto-open a URL hosts remotos | exposición de key a terceros | Loopback-only | `lifecycle.test.js` |
| Copia no condicional de CLAUDE.md | envío de configuración personal sin consentimiento | Opt-in explícito | `test-run-haiku-safety.sh` |

---

## Cambios en el README

### Antes (superpowers)
- Instalación: `hermes plugins install obra/superpowers --enable`
- Menciones genéricas a "Agent runtimes"
- Sin menciones explícitas a otros harnesses

### Después (hermespowers)
- Instalación: `hermes plugins install mtoscan-dev/hermespowers --enable`
- Posicionamiento: **Hermes-only**
- Sin menciones a otros agentes
- Referencia explícita a `SECURITY.md`
- Únicamente pruebas Hermes (no pruebas multi-harness)

---

## Compatibilidad

### Retrocompatibilidad
- **No se garantiza compatibilidad con plugins o configuraciones de otros agentes**
- Se recomienda un checkout limpio para instalar Hermespowers
- Las skills persisten en la configuración de Hermes y funcionan sin artifacts adicionales

### Upgrade path
1. Eliminar `superpowers` actual si está instalado
2. Instalar `mtoscan-dev/hermespowers`
3. Restart Hermes
4. Verificar con `tests/hermes` y `tests/brainstorm-server`

---

## Próximos pasos (opcional)

Estas mejoras no están incluidas en la versión actual pero podrían considerarse:

- CI/CD para pruebas automáticas (GitHub Actions)
- Publicación a npm (opcional, solo para companion visual)
- Documentación de troubleshooting para common issues
- Plugin metadata en `.hermes-plugin/plugin.yaml` actualizada con new repo URL

---

## Creditos

- **Diseño y ejecución**: Linus (ingeniería de software)
- **Revisión de seguridad**: Heimdall
- **Coordinación**: Noa (Orquestación)
- **Contexto y apoyo**: Miguel Ángel Toscan (CEO, Soberanía Digital)

---

**Última actualización**: 2026-10-24
**Versión del plugin**: 7.0.1 (Hermespowers)
