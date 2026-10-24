from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


NON_HERMES_INTEGRATION_PATHS = (
    ".antigravity-plugin",
    ".agents",
    ".claude-plugin",
    ".codex-plugin",
    ".cursor-plugin",
    ".devin-plugin",
    ".kimi-plugin",
    ".muse-plugin",
    ".opencode",
    ".pi",
    "gemini-extension.json",
    "GEMINI.md",
    "index.js",
    "package.json",
    "hooks",
    "docs/README.kimi.md",
    "docs/README.opencode.md",
    "docs/porting-to-a-new-harness.md",
    "docs/windows/polyglot-hooks.md",
    "scripts/package-codex-plugin.sh",
    "scripts/render-antigravity-logo.sh",
    "scripts/sync-to-codex-plugin.sh",
    "tests/antigravity",
    "tests/claude-code",
    "tests/codex",
    "tests/codex-plugin-sync",
    "tests/devin",
    "tests/explicit-skill-requests",
    "tests/hooks",
    "tests/kimi",
    "tests/opencode",
    "tests/pi",
)


def test_no_non_hermes_integration_artifacts_are_shipped():
    def is_shipped(path: str) -> bool:
        candidate = REPO_ROOT / path
        return candidate.is_file() or (
            candidate.is_dir() and any(entry.is_file() for entry in candidate.rglob("*"))
        )

    remaining = [path for path in NON_HERMES_INTEGRATION_PATHS if is_shipped(path)]
    assert remaining == [], f"non-Hermes integration artifacts remain: {remaining}"


def test_readme_only_documents_hermes_installation():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "hermes plugins install mtoscan-dev/hermespowers --enable" in readme
    for heading in (
        "### Claude Code",
        "### Codex App",
        "### Codex CLI",
        "### OpenCode",
        "### Gemini CLI",
        "### Cursor",
        "### Devin CLI",
        "### Kimi Code",
        "### Muse",
    ):
        assert heading not in readme


def test_using_superpowers_only_references_hermes_tooling():
    skill = (REPO_ROOT / "skills/using-superpowers/SKILL.md").read_text(encoding="utf-8")
    assert "references/hermes-tools.md" in skill
    for reference in (
        "references/claude-code-tools.md",
        "references/codex-tools.md",
        "references/pi-tools.md",
        "references/antigravity-tools.md",
        "references/muse-tools.md",
    ):
        assert reference not in skill


def test_visual_companion_reads_version_from_hermes_manifest():
    server = (REPO_ROOT / "skills/brainstorming/scripts/server.cjs").read_text(
        encoding="utf-8"
    )
    assert ".hermes-plugin/plugin.yaml" in server
    assert ".codex-plugin/plugin.json" not in server
    assert "package.json" not in server
