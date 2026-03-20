#!/usr/bin/env python3
"""
Skill Installer for Claude Code

Installs skills as SKILL.md files in ~/.claude/skills/<name>/,
which enables them as slash commands (/<name>) in Claude Code.

Usage:
    python install-skill.py adapt-my-resume
    python install-skill.py pyenv-setup
    python install-skill.py --list
    python install-skill.py --all
    python install-skill.py --current
    python install-skill.py --uninstall adapt-my-resume
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SKILLS_REPO = Path(__file__).parent.parent  # Parent of skill-setup directory
CLAUDE_SKILLS_DIR = Path.home() / ".claude" / "skills"
SETTINGS_PATH = Path.home() / ".claude" / "settings.json"


AVAILABLE_SKILLS = {
    "adapt-my-resume": {
        "name": "adapt-my-resume",
        "description": "Adapts resumes to match job descriptions with ATS analysis and cover letter generation",
        "config_path": "adapt-my-resume/claude-code-skill.md"
    },
    "pyenv-setup": {
        "name": "pyenv-setup",
        "description": "Helper for setting up Python virtual environments with uv",
        "config_path": "pyenv-setup/skill.json"
    },
    "skill-setup": {
        "name": "skill-setup",
        "description": "Helper for installing and managing Claude Code skills",
        "config_path": "skill-setup/skill-setup.md"
    }
}


def get_skill_config(skill_name):
    """Extract skill config (description + system_prompt) from source file."""
    skill_info = AVAILABLE_SKILLS.get(skill_name)
    if not skill_info:
        return None

    config_file = SKILLS_REPO / skill_info["config_path"]

    if config_file.suffix == '.md':
        with open(config_file, 'r') as f:
            content = f.read()
        json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group(1))
            # Unwrap full-settings format: {"skills": {"name": {...}}}
            if "skills" in parsed and isinstance(parsed["skills"], dict):
                inner = parsed["skills"]
                if len(inner) == 1:
                    return next(iter(inner.values()))
                return inner
            return parsed

    with open(config_file, 'r') as f:
        return json.load(f)


def build_skill_md(skill_name, config):
    """Render a SKILL.md with YAML frontmatter and system prompt body."""
    description = config.get("description") or AVAILABLE_SKILLS[skill_name]["description"]

    # Build frontmatter
    lines = ["---", f"name: {skill_name}", f"description: {description}", "---", ""]

    system_prompt = config.get("system_prompt")
    if system_prompt:
        lines.append(system_prompt)
    else:
        # Fallback: generate a basic prompt from whatever metadata is available
        lines.append(f"You are a {skill_name} assistant.")
        commands = config.get("commands")
        if commands:
            lines.append("\nAvailable commands:")
            for cmd_name, cmd in commands.items():
                lines.append(f"- {cmd_name}: `{cmd}`")
        quick_ref = config.get("quick_reference")
        if quick_ref:
            lines.append("\nQuick reference:")
            for key, val in quick_ref.items():
                lines.append(f"- {key}: `{val}`")

    return "\n".join(lines) + "\n"


def install_skill(skill_name):
    """Install a skill as a SKILL.md file in ~/.claude/skills/<name>/."""
    if skill_name not in AVAILABLE_SKILLS:
        print(f"❌ Unknown skill: {skill_name}")
        print(f"   Available skills: {', '.join(AVAILABLE_SKILLS.keys())}")
        return False

    print(f"📦 Installing skill: {skill_name}")

    config = get_skill_config(skill_name)
    if not config:
        print(f"❌ Could not load configuration for {skill_name}")
        return False

    skill_dir = CLAUDE_SKILLS_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(build_skill_md(skill_name, config))

    print(f"   ✓ Created: {skill_md_path}")
    print(f"   ✓ Slash command available: /{skill_name}")

    return True


def uninstall_skill(skill_name):
    """Remove a skill's directory from ~/.claude/skills/."""
    skill_dir = CLAUDE_SKILLS_DIR / skill_name
    if not skill_dir.exists():
        print(f"⚠️  Skill '{skill_name}' is not installed")
        return False

    import shutil
    shutil.rmtree(skill_dir)
    print(f"🗑️  Removed: {skill_dir}")
    return True


def cleanup_settings_json():
    """Remove the defunct 'skills' key from settings.json if present."""
    if not SETTINGS_PATH.exists():
        return
    with open(SETTINGS_PATH, 'r') as f:
        settings = json.load(f)
    if "skills" in settings:
        del settings["skills"]
        with open(SETTINGS_PATH, 'w') as f:
            json.dump(settings, f, indent=4)
        print(f"   ✓ Removed stale 'skills' key from {SETTINGS_PATH}")


def list_skills():
    """List all available skills."""
    print("📚 Available Skills\n")
    for key, info in AVAILABLE_SKILLS.items():
        print(f"  {info['name']}")
        print(f"    Description: {info['description']}")
        print(f"    Install:     python install-skill.py {key}")
        print()


def show_current_skills():
    """Show currently installed skills by scanning ~/.claude/skills/."""
    if not CLAUDE_SKILLS_DIR.exists():
        print("📭 No skills currently installed")
        print(f"   Skills directory: {CLAUDE_SKILLS_DIR}")
        return

    installed = [d for d in CLAUDE_SKILLS_DIR.iterdir() if (d / "SKILL.md").exists()]
    if not installed:
        print("📭 No skills currently installed")
        print(f"   Skills directory: {CLAUDE_SKILLS_DIR}")
        return

    print(f"📦 Installed Skills ({len(installed)})\n")
    for skill_dir in sorted(installed):
        skill_md = skill_dir / "SKILL.md"
        # Extract description from frontmatter
        content = skill_md.read_text()
        desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
        desc = desc_match.group(1).strip() if desc_match else "No description"
        print(f"  • /{skill_dir.name}: {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="Install skills for Claude Code as slash commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python install-skill.py adapt-my-resume     # installs /adapt-my-resume
    python install-skill.py --list              # list available skills
    python install-skill.py --current           # show installed skills
    python install-skill.py --all               # install all skills
    python install-skill.py --uninstall adapt-my-resume
        """
    )

    parser.add_argument('skill', nargs='?', help='Name of skill to install')
    parser.add_argument('--list', '-l', action='store_true', help='List available skills')
    parser.add_argument('--current', '-c', action='store_true', help='Show currently installed skills')
    parser.add_argument('--all', '-a', action='store_true', help='Install all available skills')
    parser.add_argument('--uninstall', metavar='SKILL', help='Uninstall a skill')
    parser.add_argument('--cleanup-settings', action='store_true',
                        help='Remove defunct skills key from settings.json')

    args = parser.parse_args()

    if args.list:
        list_skills()
    elif args.current:
        show_current_skills()
    elif args.uninstall:
        success = uninstall_skill(args.uninstall)
        sys.exit(0 if success else 1)
    elif args.cleanup_settings:
        cleanup_settings_json()
    elif args.all:
        print("📦 Installing all skills...\n")
        for skill_name in AVAILABLE_SKILLS:
            install_skill(skill_name)
            print()
        cleanup_settings_json()
    elif args.skill:
        success = install_skill(args.skill)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        print("\n💡 Tip: Use --list to see available skills")


if __name__ == "__main__":
    main()
