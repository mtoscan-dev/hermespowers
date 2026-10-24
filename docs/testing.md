# Testing Superpowers for Hermes Agent

The Hermes plugin is verified with two local suites:

- `tests/hermes/` — pytest coverage for plugin registration, bootstrap injection,
  install-layout resolution, skill descriptions, and the Hermes-only boundary.
- `tests/brainstorm-server/` — Node and Bash coverage for the optional visual
  companion server and lifecycle scripts.

Run the Hermes suite from the repository virtual environment:

```bash
.venv/bin/python -m pytest tests/hermes -q
```

Run the visual companion suite after installing its declared test dependency:

```bash
cd tests/brainstorm-server
npm install
npm test
```
