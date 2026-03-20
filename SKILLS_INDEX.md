# AI Coding Agent Skills - Index

A collection of useful skills for Claude Code and other AI coding agents.

## Available Skills

### 1. Resume Adaptation (LLM-Native) ⭐ RECOMMENDED

**Location:** `skills/adapt-my-resume/`

**What it does:** Adapts resumes to match job descriptions with ATS scoring and cover letter generation.

**Why it's better:** Delegates ALL processing to Claude for superior quality results.

**Quick Start:**
```bash
cd skills/adapt-my-resume
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"

python resume_adapter_llm.py \
    --resume /path/to/resume.pdf \
    --job "https://company.com/job-posting" \
    --output-dir ./output
```

**Features:**
- Parses PDF/DOCX/TXT resumes
- Fetches job descriptions from URLs
- Claude generates tailored resume
- Claude writes ATS analysis
- Claude creates cover letter
- Professional, human-quality output

---

### 2. Python Environment Setup

**Location:** `skills/pyenv-setup/`

**What it does:** Helps set up Python virtual environments with uv.

**Quick Start:**
```bash
# Check status
python skills/pyenv-setup/pyenv_setup.py --status

# Create venv
python skills/pyenv-setup/pyenv_setup.py --create

# Show activation command
python skills/pyenv-setup/pyenv_setup.py --activate

# Install packages
python skills/pyenv-setup/pyenv_setup.py --install requests beautifulsoup4
```

**Quick Reference:**
| Task | Command |
|------|---------|
| Create venv | `uv venv` |
| Activate (Unix) | `source .venv/bin/activate` |
| Activate (Windows) | `.venv\Scripts\activate` |
| Install package | `uv pip install <package>` |
| Install requirements | `uv pip install -r requirements.txt` |

---

### 3. Resume Adaptation (Python-Based)

**Location:** `skills/resume-adaptation/`

**What it does:** Same as LLM version but uses Python for processing.

**Status:** Legacy - kept for comparison. The LLM-native version produces better results.

---

## Using Skills

### Via Python (Recommended)
```bash
cd skills/<skill-name>
python <skill-script>.py [options]
```

### Via Natural Language with Claude
You can ask Claude:
- "Help me set up a Python virtual environment"
- "Adapt my resume for this job: [paste job description]"

---

## Project Structure

```
topskills/
├── README.md                 # Project overview
├── SKILLS_INDEX.md          # This file
└── skills/
    ├── adapt-my-resume/   # ⭐ Recommended resume tool
    ├── pyenv-setup/             # Python environment helper
    └── resume-adaptation/       # Legacy Python-based tool
```

## Contributing

To add a new skill:
1. Create `skills/<skill-name>/` directory
2. Add `skill.json` with metadata
3. Add main script(s)
4. Add `README.md` with documentation
5. Add `requirements.txt` if needed
6. Update this index
