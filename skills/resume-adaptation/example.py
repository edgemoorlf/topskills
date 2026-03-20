#!/usr/bin/env python3
"""
Example usage of the Resume Adaptation Skill

This script demonstrates how to use the skill programmatically
with ATS scoring and cover letter generation.
"""

from resume_adapter import (
    ResumeAdaptationSkill,
    ResumeAnalyzer,
    JobDescriptionAnalyzer,
    ATSScorer,
    CoverLetterGenerator,
    ResumeTailor,
)


class Args:
    """Example arguments for the skill."""
    resume = ["sample_resume.pdf"]  # Replace with your resume path
    job = """
    Senior Software Engineer

    We are looking for an experienced Software Engineer to join our team.

    Requirements:
    - 5+ years of experience with Python
    - Experience with cloud platforms (AWS, GCP, or Azure)
    - Strong understanding of distributed systems
    - Experience with Kubernetes and Docker
    - Bachelor's degree in Computer Science or equivalent

    Preferred:
    - Experience with machine learning
    - Open source contributions
    - Technical leadership experience
    """
    requirements = "Emphasize my cloud infrastructure and team leadership experience"
    output_name = "senior_swe_resume"
    output_dir = "./output"
    ats_score = True  # Enable ATS scoring
    cover_letter = True  # Generate cover letter


def example_full_workflow():
    """Demonstrate the complete skill workflow."""
    print("=" * 60)
    print("Resume Adaptation Skill - Full Workflow Example")
    print("=" * 60)

    # Create skill instance
    skill = ResumeAdaptationSkill()

    # Run with example arguments
    args = Args()
    results = skill.run(args)

    print("\n" + "=" * 60)
    print("RESULTS:")
    print(f"  Success: {results['success']}")
    print(f"  Resume DOCX: {results.get('docx_path', 'N/A')}")
    print(f"  Resume PDF: {results.get('pdf_path', 'N/A')}")
    print(f"  Cover Letter DOCX: {results.get('cover_letter_docx', 'N/A')}")
    print(f"  Cover Letter PDF: {results.get('cover_letter_pdf', 'N/A')}")

    if results.get('ats_score'):
        print("\n  ATS Score Details:")
        ats = results['ats_score']
        print(f"    Overall: {ats['overall']}/100")
        print(f"    Skills Match: {ats['sections']['skills_match']}/100")
        print(f"    Experience Match: {ats['sections']['experience_match']}/100")

    if results['errors']:
        print("\n  Errors:")
        for error in results['errors']:
            print(f"    - {error}")

    print("=" * 60)


def example_ats_scoring_only():
    """Example: Just get ATS score without generating documents."""
    print("\n" + "=" * 60)
    print("Example: ATS Scoring Only")
    print("=" * 60)

    # Sample resume text
    resume_text = """John Doe
john@example.com | 555-123-4567

SUMMARY
Experienced software engineer with Python and AWS expertise.

SKILLS
Python, AWS, Docker, Kubernetes, React

EXPERIENCE
Senior Engineer at TechCorp
- Built Python microservices on AWS
- Led team of 4 developers
- Implemented CI/CD pipelines
"""

    # Sample job description
    job_text = """Senior Software Engineer

Requirements:
- 5+ years Python experience
- AWS and cloud platforms
- Kubernetes and Docker
- Leadership experience
"""

    # Analyze
    resume_analyzer = ResumeAnalyzer()
    job_analyzer = JobDescriptionAnalyzer()

    parsed_resume = resume_analyzer.analyze(resume_text)
    job_requirements = job_analyzer.analyze(job_text)

    # Score
    ats_scorer = ATSScorer(parsed_resume, job_requirements)
    scores = ats_scorer.score()

    print(f"\nATS Overall Score: {scores['overall']}/100")
    print("\nSection Breakdown:")
    for section, score in scores['sections'].items():
        print(f"  {section.replace('_', ' ').title()}: {score}/100")

    print("\nTop Suggestions:")
    for suggestion in scores['suggestions'][:3]:
        print(f"  • {suggestion}")

    print("\nMissing Skills:")
    for skill in scores['keyword_match'].get('required_missing', [])[:5]:
        print(f"  • {skill}")


def example_cover_letter_only():
    """Example: Generate just a cover letter."""
    print("\n" + "=" * 60)
    print("Example: Cover Letter Generation Only")
    print("=" * 60)

    # Sample resume
    resume_text = """Jane Smith
jane@example.com | 555-987-6543
linkedin.com/in/janesmith

SUMMARY
Product manager with 4 years of experience in SaaS products.

SKILLS
Product strategy, Agile, User research, Data analysis, Stakeholder management

EXPERIENCE
Product Manager at SaaS Co
- Led product roadmap for B2B platform
- Increased user engagement by 35%
- Managed cross-functional team of 12
"""

    job_text = """Senior Product Manager

Requirements:
- 4+ years product management experience
- B2B SaaS experience
- Data-driven decision making
- Cross-functional leadership
"""

    # Analyze and generate
    resume_analyzer = ResumeAnalyzer()
    job_analyzer = JobDescriptionAnalyzer()

    parsed_resume = resume_analyzer.analyze(resume_text)
    job_requirements = job_analyzer.analyze(job_text)

    cover_gen = CoverLetterGenerator(
        parsed_resume,
        job_requirements,
        user_requirements="Emphasize my data analysis skills"
    )

    cover_letter = cover_gen.generate()

    print("\nGenerated Cover Letter:")
    print("-" * 40)
    print(cover_letter)


def example_manual_tailoring():
    """Example: Manual resume tailoring without file output."""
    print("\n" + "=" * 60)
    print("Example: Manual Resume Tailoring")
    print("=" * 60)

    # Original resume content
    resume_text = """Alex Johnson
alex@example.com

SUMMARY
Software developer with experience in various technologies.

SKILLS
Java, Python, JavaScript, AWS, Docker, React, Node.js, PostgreSQL, Git

EXPERIENCE
Full Stack Developer at WebAgency
- Worked on client projects using various technologies

Backend Developer at TechStart
- Built REST APIs
- Managed database schemas
"""

    # Target job
    job_text = """Backend Engineer

Requirements:
- Python expertise
- PostgreSQL databases
- REST API development
- Docker containerization
"""

    # Analyze
    resume_analyzer = ResumeAnalyzer()
    job_analyzer = JobDescriptionAnalyzer()

    parsed_resume = resume_analyzer.analyze(resume_text)
    job_requirements = job_analyzer.analyze(job_text)

    print("\nOriginal Skills Order:")
    print(f"  {parsed_resume.skills}")

    # Tailor
    tailor = ResumeTailor(parsed_resume, job_requirements)
    tailored_resume = tailor.tailor()

    print("\nTailored Skills Order (job-matching skills first):")
    print(f"  {tailored_resume.skills}")

    print("\nOriginal Summary:")
    print(f"  {parsed_resume.summary}")

    print("\nTailored Summary:")
    print(f"  {tailored_resume.summary}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("RESUME ADAPTATION SKILL - EXAMPLES")
    print("=" * 60)
    print("\nThis script demonstrates various ways to use the skill:\n")
    print("1. Full workflow with ATS scoring and cover letter")
    print("2. ATS scoring only (analysis without file generation)")
    print("3. Cover letter generation only")
    print("4. Manual tailoring (in-memory processing)")
    print("\n" + "=" * 60)

    # Run examples
    example_ats_scoring_only()
    example_cover_letter_only()
    example_manual_tailoring()

    # Note: full workflow requires actual files
    print("\n" + "=" * 60)
    print("Note: Full workflow example requires actual resume files.")
    print("Create sample_resume.pdf or modify the Args class to test.")
    print("=" * 60)


if __name__ == "__main__":
    main()
