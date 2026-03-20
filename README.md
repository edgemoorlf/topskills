# AI Coding Agent Skills

A collection of useful skills for Claude Code and other AI coding agents.

## Skills Overview

| Skill | Purpose | Status |
|-------|---------|--------|
| [resume-adaptation-llm](#1-resume-adaptation-llm-recommended) | AI-powered resume tailoring | ⭐ **Recommended** |
| [pyenv-setup](#2-python-environment-setup) | Python venv helper | Ready |
| [resume-adaptation](#3-resume-adaptation-python-based) | Legacy Python version | Archived |

---

## 1. Resume Adaptation (LLM-Native) ⭐ RECOMMENDED

**Location:** `skills/resume-adaptation-llm/`

**What it does:** Adapts resumes to match job descriptions with ATS scoring and cover letter generation.

**Why it's better:** Unlike traditional approaches that use regex and templates, this skill delegates ALL processing to Claude for superior quality results.

### Quick Start

```bash
cd skills/resume-adaptation-llm

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

- ✅ Parses PDF/DOCX/TXT resumes
- ✅ Fetches job descriptions from URLs
- ✅ **Claude generates tailored resume** (professional quality)
- ✅ **Claude writes ATS analysis** (contextual, actionable)
- ✅ **Claude creates cover letter** (compelling, customized)
- ✅ Only ~200 lines of Python (vs ~1200 in traditional approach)

### Comparison: LLM-Native vs Python-Based

| Aspect | Python-Based | LLM-Native |
|--------|-------------|------------|
| **Code Size** | ~1200 lines | ~200 lines |
| **Resume Quality** | Robotic, template-like | Professional, nuanced |
| **ATS Analysis** | Algorithmic scores only | Contextual with actionable advice |
| **Cover Letter** | Generic template | Custom-written narrative |
| **Understanding** | Keyword matching | Semantic comprehension |

See [skills/resume-adaptation-llm/README.md](skills/resume-adaptation-llm/README.md) for full documentation.

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
    ├── resume-adaptation-llm/        # ⭐ Recommended resume tool
    │   ├── skill.json
    │   ├── resume_adapter_llm.py
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
