# Skill Setup Helper for Claude Code

A skill that helps you set up and manage other skills in Claude Code.

## What It Does

This skill helps you:
- Install skills from this repository
- Configure skills in your Claude Code settings
- List available skills
- Remove skills you no longer need

## Installation

Add this to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "skills": {
    "skill-setup": {
      "description": "Helper for installing and managing Claude Code skills",
      "triggers": [
        "install skill",
        "add skill",
        "setup skill",
        "list skills",
        "remove skill"
      ],
      "system_prompt": "You are a skill setup assistant for Claude Code. Help users install, configure, and manage skills.\n\nWhen a user wants to install a skill:\n1. Check if the skill exists in the topskills repository\n2. Read the skill's claude-code-skill.md or skill.json file\n3. Guide them to add the configuration to ~/.claude/settings.json\n4. Offer to create the settings file if it doesn't exist\n\nAvailable skills in topskills:\n- resume-adaptation: Adapts resumes to job descriptions\n- pyenv-setup: Python virtual environment helper\n\nBe helpful and provide exact configuration snippets."
    }
  }
}
```

## Usage

Once installed, just ask Claude naturally:

### Install a Skill
**User:** "Install the resume adaptation skill"

**Claude:** "I'll help you set up the resume adaptation skill. Let me read the configuration..."

### List Available Skills
**User:** "What skills are available?"

**Claude:** "Here are the available skills in the topskills repository..."

### Check Current Skills
**User:** "What skills do I have installed?"

**Claude:** "Let me check your Claude Code settings..."

## Manual Setup

If you prefer to do it manually, here's how to add any skill:

1. **Find the skill config** - Look for `claude-code-skill.md` or `skill.json` in the skill directory

2. **Copy the configuration** - Get the JSON from the file

3. **Add to settings** - Paste into `~/.claude/settings.json` under the `"skills"` key

4. **Restart Claude Code** - Or the skill will be available immediately

## Example: Adding Resume Adaptation Skill

```bash
# 1. Read the skill configuration
cat skills/resume-adaptation-llm/claude-code-skill.md

# 2. Edit your Claude Code settings
nano ~/.claude/settings.json

# 3. Add the skill configuration
# (See the claude-code-skill.md file for the exact config)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not triggering | Check the trigger phrases match what you're saying |
| Skill not in settings | Make sure the JSON is valid (use a linter) |
| Changes not working | Restart Claude Code or wait a moment |

## Available Skills Reference

### resume-adaptation-llm
**Purpose:** Adapts resumes to match job descriptions
**File:** `skills/resume-adaptation-llm/claude-code-skill.md`
**Triggers:** "adapt my resume", "tailor my cv", "check ats score"

### pyenv-setup
**Purpose:** Python virtual environment helper
**File:** `skills/pyenv-setup/skill.json`
**Triggers:** "setup python venv", "create virtual environment"

### skill-setup (this skill)
**Purpose:** Helps install and manage other skills
**File:** `skills/skill-setup/skill-setup.md`
**Triggers:** "install skill", "add skill", "list skills"
