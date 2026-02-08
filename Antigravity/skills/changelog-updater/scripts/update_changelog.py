#!/usr/bin/env python3
"""
changelog-updater — update_changelog.py
Actualiza automáticamente CHANGELOG.md basándose en el último commit de git.

Analiza mensajes con formato Conventional Commits (con emoji opcional)
y genera entradas formateadas con emoji, scope y hash corto.

Usage:
    python update_changelog.py [--file CHANGELOG.md] [--repo-url <github-url>]

Examples:
    python update_changelog.py
    python update_changelog.py --file HISTORIAL.md
    python update_changelog.py --repo-url https://github.com/user/repo
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────

TYPE_EMOJIS = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📚",
    "style": "💄",
    "refactor": "♻️",
    "perf": "⚡",
    "test": "✅",
    "build": "📦",
    "ci": "👷",
    "chore": "🔧",
    "revert": "⏪",
    "other": "📝",
}

# Pattern: optional emoji, then type(scope): description
COMMIT_PATTERN = re.compile(
    r"^(?:[\U0001F300-\U0001FAFF\u2600-\u27FF\u231A-\u23AB]\s*)?"
    r"(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r":\s*(?P<desc>.+)$",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────
# Git Operations
# ─────────────────────────────────────────────

def get_last_commit() -> dict | None:
    """Retrieve the last commit hash, subject and body from git."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%H%n%s%n%b"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            print(f"❌ Error ejecutando git: {result.stderr.strip()}")
            return None

        lines = result.stdout.strip().split("\n", 2)
        if len(lines) < 2:
            print("❌ No se pudo parsear el commit.")
            return None

        return {
            "hash": lines[0],
            "subject": lines[1],
            "body": lines[2].strip() if len(lines) > 2 else "",
        }
    except FileNotFoundError:
        print("❌ Git no está instalado o no está en el PATH.")
        return None
    except Exception as e:
        print(f"❌ Error accediendo a git: {e}")
        return None


# ─────────────────────────────────────────────
# Parsing
# ─────────────────────────────────────────────

def parse_commit(commit: dict) -> dict:
    """Parse a commit dict into structured data with type, scope, description."""
    match = COMMIT_PATTERN.match(commit["subject"])

    if match:
        return {
            "hash": commit["hash"],
            "type": match.group("type").lower(),
            "scope": match.group("scope"),
            "desc": match.group("desc").strip(),
            "body": commit["body"],
        }

    # Fallback for non-conventional commits
    return {
        "hash": commit["hash"],
        "type": "other",
        "scope": None,
        "desc": commit["subject"].strip(),
        "body": commit["body"],
    }


# ─────────────────────────────────────────────
# Formatting
# ─────────────────────────────────────────────

def format_entry(data: dict, repo_url: str | None = None) -> str:
    """Format a parsed commit into a CHANGELOG entry line."""
    emoji = TYPE_EMOJIS.get(data["type"], "❓")
    scope = f"**({data['scope']})** " if data["scope"] else ""
    short_hash = data["hash"][:7]

    if repo_url:
        # Link to the commit on GitHub/GitLab
        commit_ref = f"[`{short_hash}`]({repo_url.rstrip('/')}/commit/{data['hash']})"
    else:
        commit_ref = f"(`{short_hash}`)"

    return f"- {emoji} {scope}{data['desc']} {commit_ref}\n"


# ─────────────────────────────────────────────
# File Operations
# ─────────────────────────────────────────────

def update_changelog(entry: str, filename: str = "CHANGELOG.md") -> None:
    """Insert a new entry into the CHANGELOG file under today's date section."""
    today = datetime.now().strftime("%Y-%m-%d")
    header = f"## [{today}]"

    # Read existing content
    content: list[str] = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.readlines()

    # Case 1: File doesn't exist or is empty
    if not content:
        new_content = [
            "# Changelog\n",
            "\n",
            f"{header}\n",
            "\n",
            entry,
        ]
        _write(filename, new_content)
        return

    # Case 2: Today's section already exists
    date_index = _find_line(content, header)
    if date_index != -1:
        # Insert after the header + blank line
        insert_at = date_index + 2
        # Make sure we don't go past the file length
        insert_at = min(insert_at, len(content))
        content.insert(insert_at, entry)
        _write(filename, content)
        return

    # Case 3: Other date sections exist — insert before the first one
    first_section = _find_first_section(content)
    if first_section != -1:
        new_section = [f"\n{header}\n", "\n", entry, "\n"]
        new_content = content[:first_section] + new_section + content[first_section:]
        _write(filename, new_content)
        return

    # Case 4: Fallback — append at the end
    content.extend([f"\n{header}\n", "\n", entry])
    _write(filename, content)


def _find_line(content: list[str], target: str) -> int:
    """Find the index of a line matching the target string."""
    for i, line in enumerate(content):
        if line.strip() == target.strip():
            return i
    return -1


def _find_first_section(content: list[str]) -> int:
    """Find the first '## [' section header after the title."""
    for i, line in enumerate(content):
        if line.startswith("## [") and i > 0:
            return i
    return -1


def _write(filename: str, lines: list[str]) -> None:
    """Write lines to file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"✅ {filename} actualizado correctamente.")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Actualiza CHANGELOG.md con el último commit de git."
    )
    parser.add_argument(
        "--file",
        default="CHANGELOG.md",
        help="Archivo de changelog (default: CHANGELOG.md)",
    )
    parser.add_argument(
        "--repo-url",
        default=None,
        help="URL del repositorio para generar links a commits (ej: https://github.com/user/repo)",
    )

    args = parser.parse_args()

    # Get and parse the last commit
    commit = get_last_commit()
    if not commit:
        print("⚠️ No se encontró commit o hubo un error de git.")
        sys.exit(1)

    data = parse_commit(commit)
    entry = format_entry(data, args.repo_url)

    print(f"📝 Registrando: {entry.strip()}")
    update_changelog(entry, args.file)


if __name__ == "__main__":
    main()
