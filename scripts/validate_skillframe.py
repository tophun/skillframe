#!/usr/bin/env python3
"""Validate the repository's plugin metadata and documentation structure."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, path: Path, message: str) -> None:
        relative = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        self.errors.append(f"{relative}: {message}")


def parse_frontmatter(path: Path, validation: Validation) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        validation.error(path, "frontmatter must start with ---")
        return {}

    try:
        end = lines.index("---", 1)
    except ValueError:
        validation.error(path, "frontmatter closing --- is missing")
        return {}

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith((" ", "\t", "-")):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            validation.error(path, f"invalid frontmatter line: {line}")
            continue
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def load_json(path: Path, validation: Validation) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        validation.error(path, f"invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        validation.error(path, "top-level JSON value must be an object")
        return {}
    return value


def check_required_fields(
    path: Path, fields: dict[str, str], required: tuple[str, ...], validation: Validation
) -> None:
    for field in required:
        if not fields.get(field):
            validation.error(path, f"frontmatter field is missing: {field}")


def check_manifest_paths(validation: Validation) -> None:
    marketplace = ROOT / ".claude-plugin/marketplace.json"
    marketplace_data = load_json(marketplace, validation)
    for plugin in marketplace_data.get("plugins", []):
        if not isinstance(plugin, dict):
            validation.error(marketplace, "plugins entries must be objects")
            continue
        source = plugin.get("source")
        if isinstance(source, str):
            source_path = (ROOT / source).resolve()
            if not source_path.exists():
                validation.error(marketplace, f"plugin source does not exist: {source}")

    plugin_manifest = ROOT / "plugins/skillframe/.claude-plugin/plugin.json"
    load_json(plugin_manifest, validation)

    codex_manifest = ROOT / "plugins/skillframe-codex/.codex-plugin/plugin.json"
    codex_data = load_json(codex_manifest, validation)
    skills_path = codex_data.get("skills")
    if isinstance(skills_path, str):
        resolved = (codex_manifest.parent.parent / skills_path).resolve()
        if not resolved.exists():
            validation.error(codex_manifest, f"skills path does not exist: {skills_path}")


def check_frontmatter(validation: Validation) -> None:
    skill_files = sorted(ROOT.glob("skills/*/SKILL.md"))
    skill_files += sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))

    for path in skill_files:
        fields = parse_frontmatter(path, validation)
        check_required_fields(path, fields, ("name", "description"), validation)

    for package_root in (ROOT / "plugins/skillframe", ROOT / "plugins/skillframe-codex"):
        names: dict[str, Path] = {}
        for path in sorted((package_root / "skills").glob("*/SKILL.md")):
            fields = parse_frontmatter(path, validation)
            name = fields.get("name")
            if not name:
                continue
            previous = names.get(name)
            if previous:
                validation.error(path, f"duplicate skill name {name!r}; already used by {previous}")
            names[name] = path

    agent_root = ROOT / "plugins/skillframe/agents"
    names = {}
    for path in sorted(agent_root.glob("*.md")):
        fields = parse_frontmatter(path, validation)
        check_required_fields(path, fields, ("name", "description", "model"), validation)
        if fields.get("status") == "deprecated":
            validation.error(path, "deprecated agents must not be in the active agents directory")
        name = fields.get("name")
        if not name:
            continue
        previous = names.get(name)
        if previous:
            validation.error(path, f"duplicate agent name {name!r}; already used by {previous}")
        names[name] = path


def check_markdown_links(validation: Validation) -> None:
    markdown_files = sorted(ROOT.rglob("*.md"))
    for path in markdown_files:
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip("<>").split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                validation.error(path, f"broken relative link: {target}")


def check_humanize_fast_path(validation: Validation) -> None:
    path = ROOT / "plugins/skillframe/skills/humanize-korean/SKILL.md"
    text = path.read_text(encoding="utf-8")
    fast_section = text.split("## Strict 모드", 1)[0]
    if "humanize-monolith" in fast_section:
        validation.error(path, "fast path must not reference humanize-monolith")
    if "Agent" in fast_section:
        validation.error(path, "fast path must not call an Agent")


def main() -> int:
    validation = Validation()
    check_manifest_paths(validation)
    check_frontmatter(validation)
    check_markdown_links(validation)
    check_humanize_fast_path(validation)

    if validation.errors:
        for error in validation.errors:
            print(f"::error::{error}")
        return 1

    print("Skillframe structure validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
