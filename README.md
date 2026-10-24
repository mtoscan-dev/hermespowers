# Hermespowers

Hermespowers is **Superpowers for Hermes Agent**: a Hermes-native plugin that
registers a library of engineering skills and injects a workflow bootstrap at
the beginning of a session.

It is intentionally **Hermes-only**. This repository does not package
marketplace manifests, hooks, installers, or compatibility layers for other
agent runtimes.

## What it provides

- Native registration of every bundled `skills/*/SKILL.md` through Hermes.
- A first-turn bootstrap that makes the `using-superpowers` workflow available
  without manual setup per session.
- Reusable workflows for discovery, planning, debugging, testing, review, and
  delivery.
- An optional local visual brainstorming companion with session-key access
  control.

## Install

Install from the repository:

```bash
hermes plugins install mtoscan-dev/hermespowers --enable
```

Restart an active Hermes session after installation. Hermes has no
post-compaction hook, so start a fresh session if an unusually long session
compacts past its first turn and skills stop triggering.

## How it works

On the first turn, the plugin registers the skills and injects the workflow
bootstrap. When a task applies to a skill, load it with Hermes' native
`skill_view` tool.

Typical workflow:

1. **brainstorming** — clarify the desired outcome before implementation.
2. **writing-plans** — turn approved designs into verifiable steps.
3. **test-driven-development** — establish a red/green regression loop.
4. **systematic-debugging** — isolate root causes before patching defects.
5. **requesting-code-review** — review evidence before delivery.

## Visual companion

The optional brainstorming companion serves local HTML mockups and records
user selections. Start it only after the user agrees:

```bash
bash skills/brainstorming/scripts/start-server.sh --project-dir /path/to/project --open
```

The returned URL includes a per-session key. Share the complete URL, including
its query string. By default the server binds to `127.0.0.1`; only use a
non-loopback host when the user needs remote access and understands the
network exposure. Set `SUPERPOWERS_DISABLE_TELEMETRY=1` to disable the optional
remote branding image.

## Security posture

- The plugin contains no credential store and does not load `.env` files.
- The visual companion uses a random session key, validates access for HTTP
  and WebSocket requests, and keeps persisted key files owner-readable only.
- Browser launch is opt-in (`--open`) and uses platform launchers with argument
  vectors, not an operator-provided shell command.
- Static findings in test fixtures and historical design documents require
  context review; see [SECURITY.md](SECURITY.md) for the scan triage policy.

## Verify

Run the Hermes plugin suite from a Python environment with pytest:

```bash
.venv/bin/python -m pytest tests/hermes -q
```

Run the visual companion suite after installing its declared test dependency:

```bash
cd tests/brainstorm-server
npm install
npm test
```

## License

MIT License — see [LICENSE](LICENSE).
