# AI Coding Agent Skills

A collection of useful skills for Claude Code and other AI coding agents.

## Skills Overview

| Skill | Purpose | Status |
|-------|---------|--------|
| [skill-setup](#0-skill-setup-helper) | Install/manage other skills | 🛠️ **Start Here** |
| [adapt-my-resume](#1-adapt-my-resume-recommended) | AI-powered resume tailoring | ⭐ **Recommended** |
| [pyenv-setup](#2-python-environment-setup) | Python venv helper | Ready |
| [resume-adaptation](#3-resume-adaptation-python-based) | Legacy Python version | Archived |

---

## 0. Skill Setup Helper 🛠️ START HERE

**Location:** `skills/skill-setup/`

**What it does:** Helps you install and manage other skills in Claude Code.

### Quick Start

```bash
# See available skills
python skills/skill-setup/install-skill.py --list

# Install the resume adaptation skill
python skills/skill-setup/install-skill.py resume-adaptation

# Install all skills
python skills/skill-setup/install-skill.py --all
```

This will automatically add the skill configuration to your `~/.claude/settings.json`.

### Manual Setup (Alternative)

If you prefer to set up skills manually:

1. Open your Claude Code settings: `~/.claude/settings.json`
2. Add the skill configuration from the skill's `claude-code-skill.md` file
3. Restart Claude Code (or wait for it to reload)

See [skills/skill-setup/skill-setup.md](skills/skill-setup/skill-setup.md) for full documentation.

---

## 1. Resume Adaptation (LLM-Native) ⭐ RECOMMENDED

**Location:** `skills/adapt-my-resume/`

**What it does:** Adapts resumes to match job descriptions with ATS scoring and cover letter generation.

**Why it's better:** Unlike traditional approaches that use regex and templates, this skill delegates ALL processing to Claude for superior quality results.

### Usage Options

#### Option A: Claude Code Skill (Recommended)

For the best "vibe coding" experience, use this as a Claude Code skill:

**Setup:** Add to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "skills": {
    "adapt-my-resume": {
      "description": "Adapts resumes to match job descriptions",
      "triggers": ["adapt my resume", "tailor my cv", "check ats score"],
      "system_prompt": "You are a resume adaptation assistant. When the user wants to adapt their resume, ask for their resume file and job description, then use the Read tool to read the resume, fetch the job description (URL or file), and generate: 1) ATS compatibility analysis, 2) tailored resume, 3) cover letter. Save outputs to files."
    }
  }
}
```

**Then just talk to Claude naturally:**

```
User: "Adapt my resume at ./resume.pdf for this job: https://company.com/job"
Claude: "I'll analyze your resume and create tailored materials..."
```

See [claude-code-skill.md](skills/adapt-my-resume/claude-code-skill.md) for full configuration.

#### Option B: Command-Line Tool

For automation or CI/CD:

```bash
cd skills/adapt-my-resume

# Setup
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-api-key"

# Run
python resume_adapter_llm.py \
    --resume /path/to/resume.pdf \
    --job "https://company.com/job-posting" \
    --output-dir ./output
```

### Features

- ✅ **Claude generates tailored resume** (professional quality)
- ✅ **Claude writes ATS analysis** (contextual, actionable)
- ✅ **Claude creates cover letter** (compelling, customized)
- ✅ Parses PDF/DOCX/TXT resumes
- ✅ Fetches job descriptions from URLs
- ✅ Only ~200 lines of Python (vs ~1200 in traditional approach)

### Comparison

| Aspect | Python-Based | LLM-Native CLI | Claude Code Skill |
|--------|-------------|----------------|-------------------|
| **Setup** | Install deps, API key | Install deps, API key | Just add to settings |
| **Usage** | Run commands | Run commands | Natural conversation |
| **API Costs** | Your key | Your key | Included with Claude Code |
| **Quality** | Robotic | Professional | Professional |
| **Best For** | Legacy/Archive | Automation/CI | Daily use |

See [skills/adapt-my-resume/README.md](skills/adapt-my-resume/README.md) for full documentation.

---

## 2. Python Environment Setup

**Location:** `skills/pyenv-setup/`

**What it does:** Helps set up Python virtual environments with `uv`.

### Quick Start

```bash
# Check status
python skills/pyenv-setup/pyenv_setup.py --status

# Create virtual environment
python skills/pyenv-setup/pyenv_setup.py --create

# Install packages
python skills/pyenv-setup/pyenv_setup.py --install requests beautifulsoup4
```

### Quick Reference

| Task | Command |
|------|---------|
| Create venv | `uv venv` |
| Activate (Unix/Mac) | `source .venv/bin/activate` |
| Activate (Windows) | `.venv\Scripts\activate` |
| Install package | `uv pip install <package>` |
| Install from requirements | `uv pip install -r requirements.txt` |

See [skills/pyenv-setup/README.md](skills/pyenv-setup/README.md) for full documentation.

---

## 3. Resume Adaptation (Python-Based)

**Location:** `skills/resume-adaptation/`

**Status:** Archived for reference - kept to demonstrate the difference between Python-heavy and LLM-native approaches.

The Python-based version attempts to do parsing, analysis, and formatting in code. While functional, it produces inferior results compared to the LLM-native version.

---

## Project Structure

```
topskills/
├── README.md                          # This file
├── SKILLS_INDEX.md                   # Detailed skill index
└── skills/
    ├── skill-setup/                  # 🛠️ Skill installer helper
    │   ├── skill-setup.md
    │   └── install-skill.py
    ├── adapt-my-resume/        # ⭐ Recommended resume tool
    │   ├── skill.json
    │   ├── claude-code-skill.md      # Claude Code skill config
    │   ├── resume_adapter_llm.py     # CLI tool (optional)
    │   ├── requirements.txt
    │   └── README.md
    ├── pyenv-setup/                  # Python environment helper
    │   ├── skill.json
    │   ├── pyenv_setup.py
    │   └── README.md
    └── resume-adaptation/            # Legacy Python-based tool
        ├── skill.json
        ├── resume_adapter.py
        ├── requirements.txt
        ├── README.md
        ├── __init__.py
        ├── example.py
        └── test_resume_adapter.py
```

---

## Design Philosophy

### LLM-Native Skills

Modern AI coding skills should:

1. **Do minimal work in code** - Only handle I/O (files, URLs, APIs)
2. **Delegate intelligence to the LLM** - Let Claude do analysis, reasoning, and generation
3. **Focus on orchestration** - Connect inputs to LLM to outputs
4. **Produce higher quality** - LLMs understand nuance, context, and craft

**Example:** The resume adaptation skill fetches files and sends them to Claude. Claude does ALL the hard work: parsing experience, understanding job requirements, tailoring content, scoring ATS compatibility, and writing cover letters.

**Result:** Better output with less code that's easier to maintain.

---

## Contributing

To add a new skill:

1. Create `skills/{skill-name}/` directory
2. Add `skill.json` with metadata and triggers
3. Add main script(s) - keep them minimal, delegate to LLM
4. Add `README.md` with usage examples
5. Add `requirements.txt` for dependencies
6. Update this README and `SKILLS_INDEX.md`

---

## License

MIT License
