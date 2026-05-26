#!/bin/bash
# Script to create CLAUDE.md symlinks to AGENTS.md files
# Purpose: Allow Claude Code (which uses CLAUDE.md) to work with AGENTS.md standard
#
# Run this after cloning the repo or adding new AGENTS.md files
# Usage: ./utils/setup-claude-symlinks.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "Setting up CLAUDE.md symlinks for Claude Code compatibility..."
echo "Project root: $PROJECT_ROOT"
echo ""

cd "$PROJECT_ROOT"

# Find all AGENTS.md files and create corresponding CLAUDE.md symlinks
find . -name "AGENTS.md" -type f ! -path "./.git/*" | while read agents_file; do
    dir=$(dirname "$agents_file")
    claude_file="$dir/CLAUDE.md"

    # Skip if CLAUDE.md is already a regular file (migration case)
    if [ -f "$claude_file" ] && [ ! -L "$claude_file" ]; then
        echo "WARNING: $claude_file exists as regular file"
        echo "         Run: del \"$claude_file\" then re-run this script"
        continue
    fi

    # Remove existing symlink if present
    if [ -L "$claude_file" ]; then
        rm "$claude_file"
    fi

    # Create hard link on Windows (no admin/Developer Mode required), symlink elsewhere
    # Note: cmd /c mklink does not work from Git Bash; use PowerShell instead
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -n "$WINDIR" ]]; then
        agents_win=$(cygpath -w "$agents_file")
        claude_win=$(cygpath -w "$claude_file")
        powershell -Command "New-Item -ItemType HardLink -Path '$claude_win' -Target '$agents_win'" > /dev/null
        echo "Created hard link: $claude_file -> $agents_file"
    else
        ln -s "$(basename "$agents_file")" "$claude_file"
        echo "Created symlink: $claude_file -> $(basename "$agents_file")"
    fi
done

echo ""
echo "Done!"
echo "Remember: Edit AGENTS.md files, not CLAUDE.md"
echo ""
echo "Hard links/symlinks are gitignored. If you add new AGENTS.md files, re-run this script."
echo "On Windows: uses 'mklink /H' (hard link, no admin needed). On Linux/macOS: uses 'ln -s' (symlink)."
