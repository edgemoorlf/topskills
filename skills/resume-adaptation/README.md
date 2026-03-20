# Resume Adaptation Skill

An AI-powered skill for Claude Code that adapts resumes to match specific job descriptions, with ATS scoring and cover letter generation.

## Features

- **Multi-format Input Support**: Accepts resumes in PDF, DOCX, TXT, and Markdown formats
- **Flexible Job Description Input**: Supports direct text, URLs, or file uploads
- **Smart Content Analysis**: Automatically extracts key requirements and matches them to resume content
- **Skills Prioritization**: Reorders skills to highlight those most relevant to the job
- **Experience Tailoring**: Reorders and enhances experience entries based on job relevance
- **ATS Scoring**: Analyzes resume compatibility with Applicant Tracking Systems
- **Cover Letter Generation**: Creates tailored cover letters matching the job requirements
- **Dual Output Format**: Generates both editable DOCX and PDF files

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. For PDF-to-DOCX conversion on macOS/Windows:
```bash
pip install docx2pdf
```

On Linux, the skill will use LibreOffice command-line tools or reportlab as fallback.

## Usage

### Command Line

```bash
# Basic usage
python resume_adapter.py --resume my_resume.pdf --job "Software Engineer position..."

# Using a job posting URL
python resume_adapter.py --resume resume.docx --job https://company.com/careers/software-engineer

# With custom requirements
python resume_adapter.py --resume resume.pdf --job job_desc.txt --requirements "Emphasize leadership experience"

# Include ATS compatibility scoring
python resume_adapter.py --resume resume.pdf --job "Job description..." --ats-score

# Generate cover letter
python resume_adapter.py --resume resume.pdf --job "Job description..." --cover-letter

# Full feature set - resume adaptation + ATS score + cover letter
python resume_adapter.py --resume resume.pdf --job "Job description..." \
    --ats-score --cover-letter \
    --output-name "google_swe_application" \
    --output-dir ./applications
```

### As a Claude Code Skill

This skill can be invoked directly in Claude Code:

```
/adapt-resume --resume path/to/resume.pdf --job "Software Engineer at TechCorp..." --ats-score --cover-letter
```

Or through natural language:

```
Please adapt my resume for this job, check my ATS score, and generate a cover letter:
Resume: /path/to/resume.pdf
Job: [paste job description]
```

## Features in Detail

### 1. ATS Scoring

The ATS (Applicant Tracking System) scorer analyzes your resume against the job description and provides:

- **Overall Score** (0-100): Composite score across all factors
- **Section Scores**:
  - **Skills Match**: How well your skills align with job requirements
  - **Experience Match**: Relevance of your experience to job responsibilities
  - **Education Match**: Alignment of your education with requirements
  - **Keyword Density**: Distribution and frequency of important keywords
  - **Format Score**: ATS-friendliness of your resume format
  - **Content Score**: Quality of content (action verbs, measurable results)

- **Improvement Suggestions**: Actionable recommendations to improve your score
- **Missing Keywords**: Important skills and keywords not found in your resume

**Example Output:**
```
==================================================
📊 ATS COMPATIBILITY REPORT
==================================================

🎯 Overall Score: 78/100

📋 Section Scores:
   ✓ Skills Match: 85/100
   ✓ Experience Match: 80/100
   ✓ Education Match: 75/100
   ⚠ Keyword Density: 65/100
   ✓ Format Score: 90/100
   ✓ Content Score: 85/100

💡 Suggestions for Improvement:
   1. Add more relevant skills. Missing: Kubernetes, Terraform
   2. Increase keyword density by incorporating more job-specific terms
   3. Use more action verbs and quantify achievements

🔍 Missing Required Skills:
   • Kubernetes
   • Terraform
   • Microservices
```

### 2. Cover Letter Generation

The cover letter generator creates a tailored cover letter that:

- References the specific job title and company
- Highlights your most relevant skills and experience
- Connects your background to job requirements
- Uses professional tone and structure
- Includes proper formatting (header, salutation, body, closing)

**Generated Files:**
- `{output_name}_cover_letter.txt` - Plain text version
- `{output_name}_cover_letter.docx` - Editable Word document
- `{output_name}_cover_letter.pdf` - PDF version

### 3. Resume Tailoring

The resume tailor:

- Reorders skills to prioritize job-matching ones first
- Highlights most relevant experience entries
- Enhances professional summary with relevant keywords
- Maintains honesty while emphasizing alignment
- Generates clean, professional formatting

## How It Works

1. **Input Parsing**: Parse resume files and job descriptions from various sources
2. **Resume Analysis**: Extract structured information (contact info, summary, skills, experience, education)
3. **Job Analysis**: Identify key requirements (skills, experience, keywords)
4. **ATS Scoring**: Calculate compatibility score with detailed breakdown
5. **Content Tailoring**: Reorder and enhance content for job alignment
6. **Cover Letter Generation**: Create matching cover letter
7. **Document Generation**: Create professional DOCX and PDF outputs

## File Structure

```
skills/resume-adaptation/
├── skill.json              # Skill definition for Claude Code
├── resume_adapter.py       # Main implementation (~1200 lines)
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── __init__.py            # Package init
└── example.py             # Example usage
```

## Input Formats

### Resume Files
- **PDF**: Extracted using pypdf
- **DOCX**: Microsoft Word format
- **TXT**: Plain text
- **MD**: Markdown format

### Job Descriptions
- **Direct text**: Paste the job description
- **URL**: Provide a link to the job posting
- **File**: PDF, DOCX, or TXT file

## Output Files

The skill generates the following files in the output directory:

**Resume Files:**
- `{output_name}.docx` - Editable Microsoft Word document
- `{output_name}.pdf` - PDF version

**Cover Letter Files** (if `--cover-letter` is used):
- `{output_name}_cover_letter.txt` - Plain text
- `{output_name}_cover_letter.docx` - Word document
- `{output_name}_cover_letter.pdf` - PDF version

## Testing

Run the test suite:

```bash
# Run unit tests
python -m pytest test_resume_adapter.py -v

# Run with sample data
python test_resume_adapter.py --demo

# Test specific features
python test_resume_adapter.py --test-ats
python test_resume_adapter.py --test-cover-letter
```

See [Testing Guide](#testing-guide) below for more details.

## Customization Tips

### User Requirements Prompts

Guide the adaptation with specific instructions:

- "Emphasize my management experience"
- "Focus on technical skills over soft skills"
- "Highlight projects related to AI/ML"
- "Keep it to one page"
- "Target a senior-level position"

### Multiple Resume Versions

Combine information from different resume versions:

```bash
python resume_adapter.py --resume tech_resume.pdf mgmt_resume.pdf --job "..."
```

## Limitations

- PDF conversion quality depends on source document structure
- URL fetching may not work with all job boards
- Complex formatting may not be fully preserved
- Images and graphics are not extracted

## Future Enhancements

Potential improvements:

- [ ] LinkedIn profile optimization suggestions
- [ ] Batch processing for multiple job applications
- [ ] Resume version management and tracking
- [ ] Industry-specific templates
- [ ] Interview preparation tips based on job requirements

## License

MIT License

## Testing Guide

### Unit Tests

The skill includes comprehensive unit tests covering:

- **Document Parsing**: PDF, DOCX, TXT, MD file parsing
- **Resume Analysis**: Contact extraction, section identification, skill extraction
- **Job Analysis**: Skill extraction, requirement parsing, keyword identification
- **ATS Scoring**: Scoring algorithms, suggestion generation
- **Cover Letter Generation**: Content generation, formatting
- **Document Builder**: DOCX and PDF creation

### Running Tests

```bash
# Navigate to skill directory
cd skills/resume-adaptation

# Run all tests
python -m pytest test_resume_adapter.py -v

# Run specific test category
python -m pytest test_resume_adapter.py::TestATSScorer -v
python -m pytest test_resume_adapter.py::TestCoverLetterGenerator -v

# Run with coverage
python -m pytest test_resume_adapter.py --cov=resume_adapter --cov-report=html
```

### Manual Testing

Create test files and run:

```bash
# Create sample resume
echo "John Doe
john@example.com | 555-123-4567
linkedin.com/in/johndoe

SUMMARY
Experienced software engineer with 5+ years in Python and cloud technologies.

SKILLS
Python, AWS, Docker, Kubernetes, React, PostgreSQL

EXPERIENCE
Senior Software Engineer | TechCorp | 2020-Present
- Led development of microservices architecture
- Managed team of 5 engineers

Software Engineer | StartupXYZ | 2018-2020
- Built REST APIs using Python and Flask
- Deployed applications on AWS" > test_resume.txt

# Create sample job description
echo "Senior Software Engineer

Requirements:
- 5+ years Python experience
- AWS or cloud platform expertise
- Kubernetes and Docker
- Leadership experience
- React frontend development

Preferred:
- Microservices architecture
- PostgreSQL databases" > test_job.txt

# Run the skill
python resume_adapter.py \
    --resume test_resume.txt \
    --job test_job.txt \
    --ats-score \
    --cover-letter \
    --output-name test_output
```

## Contributing

This is an open skill for the Claude Code community. Contributions and improvements are welcome!
