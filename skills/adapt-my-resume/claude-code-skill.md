# Claude Code Skill: Resume Adaptation

This skill integrates directly into Claude Code, allowing natural language interactions for resume adaptation.

## Installation

Add to your Claude Code settings (`~/.claude/settings.json`):

```json
{
  "skills": {
    "resume-adaptation": {
      "description": "Adapts resumes to match job descriptions with ATS analysis and cover letter generation",
      "triggers": [
        "adapt my resume",
        "tailor my cv",
        "optimize resume for",
        "check my resume ats score",
        "write cover letter for",
        "make resume for job",
        "match resume to job"
      ],
      "system_prompt": "You are a resume adaptation assistant. When the user wants to adapt their resume:\n\n1. Ask for their resume file path if not provided\n2. Ask for the job description (text, file, or URL) if not provided\n3. Use the Read tool to read the resume file\n4. If job is a URL, use WebFetch to get the content\n5. If job is a file, use Read to get the content\n6. Analyze the resume against the job requirements\n7. Generate:\n   - ATS compatibility analysis with scores and suggestions\n   - A tailored resume optimized for the job\n   - A compelling cover letter\n8. Use Write to save all outputs to the specified directory\n\nProvide professional, detailed analysis and well-formatted outputs."
    }
  }
}
```

## Usage Examples

Once installed, just talk to Claude naturally:

### Example 1: Basic Usage
**User:** "Adapt my resume for this job"

**Claude:** "I'd be happy to help! Please provide:\n1. The path to your resume file\n2. The job description (you can paste text, give me a file path, or share a URL)"

### Example 2: With Specific File
**User:** "Tailor my resume at ./resumes/my_resume.pdf for https://company.com/job-posting"

**Claude:** "I'll analyze your resume against that job posting and create tailored materials for you..."

### Example 3: ATS Check
**User:** "Check the ATS score for my resume against this job description"

**Claude:** "I'll analyze how well your resume matches the job requirements and provide an ATS compatibility report..."

### Example 4: Cover Letter Only
**User:** "Write a cover letter for my resume for this Software Engineer position at Google"

**Claude:** "I'll craft a compelling cover letter based on your experience and the job requirements..."

## What Claude Will Generate

For each request, Claude will create:

1. **`{name}_ats_analysis.txt`** - Detailed ATS compatibility report
   - Overall score (0-100)
   - Section-by-section breakdown
   - Missing keywords/skills
   - Strengths
   - Specific improvement suggestions

2. **`{name}_tailored_resume.txt`** - Professionally formatted resume
   - Rewritten summary targeting the job
   - Skills prioritized by relevance
   - Experience reframed to match requirements
   - Clean, ATS-friendly formatting

3. **`{name}_cover_letter.txt`** - Custom cover letter
   - Strong opening hook
   - 2-3 relevant achievements highlighted
   - Connection to company/role
   - Professional closing

## Directory Structure

```
output/
├── {name}_ats_analysis.txt
├── {name}_tailored_resume.txt
└── {name}_cover_letter.txt
```

## Tips for Best Results

- **Provide complete job descriptions** - The more detail, the better the tailoring
- **Include your requirements** - Tell Claude if you want to emphasize specific experience
- **Use PDF or text resumes** - These work best for parsing
- **Review the ATS analysis** - It shows you exactly what to improve

## Comparison with Command-Line Version

| Feature | Command-Line | Claude Code Skill |
|---------|-------------|-------------------|
| **Setup** | Install Python, deps, API key | Just add to settings.json |
| **Usage** | Run commands | Natural conversation |
| **Flexibility** | Fixed arguments | Dynamic, interactive |
| **API Costs** | Your Anthropic API key | Included with Claude Code |
| **Quality** | Good | Better (more context) |

The Claude Code skill is the recommended way to use this tool!
