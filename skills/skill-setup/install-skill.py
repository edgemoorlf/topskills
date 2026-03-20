#!/usr/bin/env python3
"""
Skill Installer for Claude Code

Automatically installs skills from the topskills repository to your Claude Code settings.

Usage:
    python install-skill.py resume-adaptation
    python install-skill.py pyenv-setup
    python install-skill.py --list
    python install-skill.py --all
"""

import argparse
import json
import os
import sys
from pathlib import Path

SKILLS_REPO = Path(__file__).parent.parent  # Parent of skill-setup directory
SETTINGS_PATH = Path.home() / ".claude" / "settings.json"


AVAILABLE_SKILLS = {
    "resume-adaptation": {
        "name": "resume-adaptation",
        "description": "Adapts resumes to match job descriptions with ATS analysis and cover letter generation",
        "triggers": ["adapt my resume", "tailor my cv", "optimize resume for", "check my resume ats score", "write cover letter for"],
        "config_path": "resume-adaptation-llm/claude-code-skill.md"
    },
    "pyenv-setup": {
        "name": "pyenv-setup",
        "description": "Helper for setting up Python virtual environments with uv",
        "triggers": ["setup python venv", "create virtual environment", "activate venv"],
        "config_path": "pyenv-setup/skill.json"
    },
    "skill-setup": {
        "name": "skill-setup",
        "description": "Helper for installing and managing Claude Code skills",
        "triggers": ["install skill", "add skill", "setup skill", "list skills"],
        "config_path": "skill-setup/skill-setup.md"
    }
}


def load_settings():
    """Load existing Claude Code settings or create new."""
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    return {}


def save_settings(settings):
    """Save settings to Claude Code settings file."""
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f, indent=4)


def get_skill_config(skill_name):
    """Get skill configuration from repository."""
    skill_info = AVAILABLE_SKILLS.get(skill_name)
    if not skill_info:
        return None

    config_file = SKILLS_REPO / skill_info["config_path"]

    # If it's a markdown file, extract the JSON from code blocks
    if config_file.suffix == '.md':
        with open(config_file, 'r') as f:
            content = f.read()
        # Look for JSON in markdown code blocks
        import re
        json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))

    # Otherwise assume it's a JSON file
    with open(config_file, 'r') as f:
        return json.load(f)


def install_skill(skill_name):
    """Install a skill to Claude Code settings."""
    if skill_name not in AVAILABLE_SKILLS:
        print(f"❌ Unknown skill: {skill_name}")
        print(f"   Available skills: {', '.join(AVAILABLE_SKILLS.keys())}")
        return False

    print(f"📦 Installing skill: {skill_name}")

    # Load existing settings
    settings = load_settings()

    # Initialize skills dict if needed
    if "skills" not in settings:
        settings["skills"] = {}

    # Get skill config
    config = get_skill_config(skill_name)
    if not config:
        print(f"❌ Could not load configuration for {skill_name}")
        return False

    # Add skill to settings
    settings["skills"][skill_name] = config

    # Save settings
    save_settings(settings)

    print(f"   ✓ Skill '{skill_name}' installed successfully!")
    print(f"   📍 Settings file: {SETTINGS_PATH}")
    print(f"\n   Triggers:")
    for trigger in AVAILABLE_SKILLS[skill_name]["triggers"]:
        print(f"     • \"{trigger}\"")

    return True


def list_skills():
    """List all available skills."""
    print("📚 Available Skills\n")

    for key, info in AVAILABLE_SKILLS.items():
        print(f"  {info['name']}")
        print(f"    Description: {info['description']}")
        print(f"    Install: python install-skill.py {key}")
        print()


def show_current_skills():
    """Show currently installed skills."""
    settings = load_settings()
    skills = settings.get("skills", {})

    if not skills:
        print("📭 No skills currently installed")
        print(f"   Settings file: {SETTINGS_PATH}")
        return

    print(f"📦 Installed Skills ({len(skills)})\n")
    for name, config in skills.items():
        desc = config.get("description", "No description")
        print(f"  • {name}: {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="Install skills for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Install a specific skill
    python install-skill.py resume-adaptation

    # List all available skills
    python install-skill.py --list

    # Show currently installed skills
    python install-skill.py --current

    # Install all available skills
    python install-skill.py --all
        """
    )

    parser.add_argument('skill', nargs='?', help='Name of skill to install')
    parser.add_argument('--list', '-l', action='store_true', help='List available skills')
    parser.add_argument('--current', '-c', action='store_true', help='Show currently installed skills')
    parser.add_argument('--all', '-a', action='store_true', help='Install all available skills')

    args = parser.parse_args()

    if args.list:
        list_skills()
    elif args.current:
        show_current_skills()
    elif args.all:
        print("📦 Installing all skills...\n")
        for skill_name in AVAILABLE_SKILLS:
            install_skill(skill_name)
            print()
    elif args.skill:
        success = install_skill(args.skill)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        print("\n💡 Tip: Use --list to see available skills")


if __name__ == "__main__":
    main()
