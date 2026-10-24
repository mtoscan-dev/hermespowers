# Security policy and scan triage

## Scope

Hermespowers is a Hermes Agent plugin. Security review covers the plugin loader,
bundled executable scripts, the visual companion server, and any dependency
introduced for those components.

## Reporting vulnerabilities

Do not include secrets, session keys, or private project data in a public
report. Provide a minimal reproduction, affected path and version, impact, and
a safe remediation proposal.

## Static scan triage

A pattern match is evidence to review, not automatically a vulnerability. Classify
findings by executable context and data flow:

| Finding class | Review rule |
|---|---|
| Runtime shell execution | Block unless arguments are fixed or passed as an argv vector without a shell. |
| Runtime secrets or tokens | Block if logged, committed, transmitted unexpectedly, or granted broader access than intended. |
| Filesystem deletion | Verify the path is controlled, scoped to a temporary/session directory, and quoted. |
| Test fixture tokens | Accept only when clearly synthetic, isolated from production configuration, and never usable externally. |
| Historical plans and release notes | Treat as documentation, not executable behavior; preserve provenance but do not report as a runtime vulnerability. |

## Current hardening decisions

- The visual companion binds locally by default and uses a random session key
  for HTTP and WebSocket access.
- Persisted companion key files are restricted to owner permissions.
- `BRAINSTORM_OPEN_CMD` is intentionally unsupported: browser launches use
  platform-selected executables through `execFile`, preventing shell command
  construction from an environment variable.
- The plugin does not ship compatibility code for other agent harnesses.

## Re-running checks

```bash
.venv/bin/python -m pytest tests/hermes -q
cd tests/brainstorm-server && npm test
```

Before publishing a change, inspect the diff for runtime execution, credential,
and path-handling changes; then run the relevant suites above.
