# Resume Adaptation Skill - LLM-Native Version

An **LLM-native** skill that delegates ALL processing to Claude, resulting in superior quality tailored resumes, ATS analysis, and cover letters.

## Philosophy

| Traditional Approach | LLM-Native Approach |
|---------------------|---------------------|
| Python does parsing, analysis, tailoring, formatting | Python only fetches files/URLs |
| Buggy regex-based extraction | Claude understands context and nuance |
| Poor formatting, robotic output | Professional, human-quality writing |
| Limited understanding of job requirements | Deep semantic analysis |
| ~1200 lines of Python code | ~200 lines of Python code |

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  User Input │────▶│ Python Code  │────▶│  Claude (LLM)   │
│  (resume +  │     │ (fetch only) │     │ (all processing)│
│   job desc) │     └──────────────┘     └─────────────────┘
└─────────────┘                                   │
                                                  ▼
                                         ┌─────────────────┐
                                         │ • Parse resume  │
                                         │ • Extract job   │
                                         │   requirements  │
                                         │ • Tailor content│
                                         │ • ATS scoring   │
                                         │ • Cover letter  │
                                         │ • Format output │
                                         └─────────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────────┐
                                         │  Output Files   │
                                         │ • resume.txt    │
                                         │ • cover_letter  │
                                         │ • ats_analysis  │
                                         └─────────────────┘
```

## Installation

```bash
cd skills/resume-adaptation-llm

# Create virtual environment
uv venv

# Install minimal dependencies
uv pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key"
```

## Usage

```bash
# Basic usage - text job description
python resume_adapter_llm.py \
    --resume my_resume.pdf \
    --job "Software Engineer position requiring Python, AWS..."

# Using a job posting URL
python resume_adapter_llm.py \
    --resume resume.pdf \
    --job https://company.com/careers/software-engineer

# With custom requirements
python resume_adapter_llm.py \
    --resume resume.pdf \
    --job job_desc.txt \
    --requirements "Emphasize my leadership experience"
```

## Output Files

The skill generates:

| File | Description |
|------|-------------|
| `{name}_resume.txt` | Tailored resume (professionally formatted) |
| `{name}_cover_letter.txt` | Custom cover letter for the job |
| `{name}_ats_analysis.txt` | Detailed ATS compatibility analysis |
| `{name}_full_response.txt` | Complete Claude response for reference |

## Why This Approach Is Better

### 1. **Superior Quality**
- Claude understands context, not just keywords
- Natural, human-quality writing
- Professional formatting
- Intelligent decisions about what to emphasize

### 2. **Less Code, Fewer Bugs**
- ~200 lines vs ~1200 lines
- No regex-based parsing errors
- No formatting glitches
- No edge cases to handle

### 3. **More Capable**
- Understands nuanced job requirements
- Can interpret ambiguous experience descriptions
- Adapts writing style to industry/role
- Provides meaningful ATS insights

### 4. **Easier to Maintain**
- Simple, clear code
- Single point of intelligence (Claude)
- Easy to update prompts
- No complex logic to debug

## Comparison Example

### Traditional Approach Output
```
John Doe
john@example.com

SKILLS
Python, AWS, Docker, Kubernetes

EXPERIENCE
Senior Engineer at TechCorp
- Built Python applications
- Deployed on AWS
[Robotic, keyword-stuffed, poor formatting]
```

### LLM-Native Approach Output
```
JOHN DOE
john@example.com | (555) 123-4567 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Senior software engineer with 6+ years architecting scalable cloud
solutions on AWS. Proven track record leading teams to deliver
high-performance systems serving millions of users.

CORE COMPETENCIES
• Cloud Architecture: AWS (EC2, Lambda, S3), Docker, Kubernetes
• Backend Development: Python, Django, REST APIs, Microservices
• Leadership: Team management, technical mentorship, Agile

PROFESSIONAL EXPERIENCE

SENIOR SOFTWARE ENGINEER | TechCorp | 2021-Present
• Architected cloud infrastructure serving 10M+ daily active users,
  reducing latency by 40% through strategic AWS optimization
• Lead cross-functional team of 5 engineers, establishing CI/CD
  pipelines that decreased deployment time by 60%
• Designed microservices architecture using Docker and Kubernetes,
  improving system reliability to 99.99% uptime
[Professionally written, tailored, impactful]
```

## API Costs

This skill uses Claude's API, which incurs costs:
- Input tokens: Resume + Job description (~2K-4K tokens)
- Output tokens: Full tailored resume + cover letter + ATS analysis (~2K-3K tokens)
- Estimated cost per run: $0.05-0.15 (using Claude 3.5 Sonnet)

## Configuration

### Environment Variables
- `ANTHROPIC_API_KEY` - Required for Claude API access

### Command Line Options
- `--resume` - Path to resume file(s)
- `--job` - Job description (text, URL, or file)
- `--requirements` - Additional user preferences
- `--output-name` - Base name for output files
- `--output-dir` - Output directory
- `--claude-api-key` - API key (if not using env var)

## Limitations

- Requires internet connection for Claude API
- API costs per run (see above)
- Output is text files (not DOCX/PDF - but you can ask Claude to convert)

## Future Enhancements

- [ ] Add support for other LLM providers (OpenAI, etc.)
- [ ] Caching to reduce API costs for repeated runs
- [ ] Batch processing for multiple jobs
- [ ] Integration with job board APIs
