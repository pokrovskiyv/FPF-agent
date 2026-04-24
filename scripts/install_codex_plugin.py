#!/usr/bin/env python3
"""Install the packaged FPF Codex plugin into a home-local marketplace.

Default install location:
  ~/plugins/fpf
  ~/.agents/plugins/marketplace.json

Use --home in tests or when installing into an alternate home directory.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLUGIN_SOURCE = PROJECT_ROOT / "plugins" / "fpf"
PLUGIN_NAME = "fpf"


def plugin_entry() -> dict:
    return {
        "name": PLUGIN_NAME,
        "source": {
            "source": "local",
            "path": "./plugins/fpf",
        },
        "policy": {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        },
        "category": "Productivity",
    }


def load_marketplace(path: Path) -> dict:
    if not path.exists():
        return {
            "name": "local",
            "interface": {
                "displayName": "Local Codex Plugins",
            },
            "plugins": [],
        }

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Marketplace is not valid JSON: {path}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Marketplace root must be a JSON object: {path}")
    if "plugins" not in data or not isinstance(data["plugins"], list):
        data["plugins"] = []
    if "name" not in data:
        data["name"] = "local"
    if "interface" not in data or not isinstance(data["interface"], dict):
        data["interface"] = {"displayName": "Local Codex Plugins"}
    elif "displayName" not in data["interface"]:
        data["interface"]["displayName"] = "Local Codex Plugins"
    return data


def update_marketplace(path: Path) -> None:
    marketplace = load_marketplace(path)
    marketplace["plugins"] = [
        entry for entry in marketplace["plugins"]
        if entry.get("name") != PLUGIN_NAME
    ]
    marketplace["plugins"].append(plugin_entry())

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def sync_plugin(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Plugin source does not exist: {source}")
    manifest = source / ".codex-plugin" / "plugin.json"
    if not manifest.exists():
        raise FileNotFoundError(f"Plugin manifest does not exist: {manifest}")

    if target.exists():
        shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the FPF Codex plugin into a home-local marketplace.",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory to install into (default: current user's home)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_PLUGIN_SOURCE,
        help="Packaged plugin source directory (default: plugins/fpf)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    home = args.home.expanduser().resolve()
    source = args.source.expanduser().resolve()

    target = home / "plugins" / PLUGIN_NAME
    marketplace_path = home / ".agents" / "plugins" / "marketplace.json"

    sync_plugin(source, target)
    update_marketplace(marketplace_path)

    print(f"Installed plugin: {target}")
    print(f"Updated marketplace: {marketplace_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
