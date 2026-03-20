#!/usr/bin/env python3
"""
Test suite for Resume Adaptation Skill

Run with: python -m pytest test_resume_adapter.py -v
Or: python test_resume_adapter.py --demo
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the skill classes
from resume_adapter import (
    DocumentParser,
    ResumeAnalyzer,
    JobDescriptionAnalyzer,
    ResumeTailor,
    ResumeDocumentBuilder,
    ATSScorer,
    CoverLetterGenerator,
    ResumeAdaptationSkill,
    ParsedResume,
    JobRequirements,
    ResumeSection,
)


class TestDocumentParser(unittest.TestCase):
    """Tests for DocumentParser class."""

    def setUp(self):
        self.parser = DocumentParser()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_txt(self):
        """Test parsing plain text files."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_content = "John Doe\nSoftware Engineer\nPython, AWS, Docker"
        test_file.write_text(test_content)

        result = self.parser.parse_txt(str(test_file))
        self.assertEqual(result, test_content)

    def test_parse_md(self):
        """Test parsing markdown files."""
        test_file = Path(self.temp_dir) / "test.md"
        test_content = "# John Doe\n\n## Skills\n- Python\n- AWS"
        test_file.write_text(test_content)

        result = self.parser.parse_md(str(test_file))
        self.assertIn("John Doe", result)
        self.assertIn("Python", result)

    def test_unsupported_format(self):
        """Test that unsupported formats raise ValueError."""
        test_file = Path(self.temp_dir) / "test.xyz"
        test_file.write_text("content")

        with self.assertRaises(ValueError):
            self.parser.parse(str(test_file))


class TestResumeAnalyzer(unittest.TestCase):
    """Tests for ResumeAnalyzer class."""

    def setUp(self):
        self.analyzer = ResumeAnalyzer()

    def test_analyze_basic_resume(self):
        """Test analyzing a basic resume."""
        raw_text = """John Doe
john@example.com | 555-123-4567

SUMMARY
Experienced software engineer

SKILLS
Python, AWS, Docker

EXPERIENCE
TechCorp - Senior Engineer - 2020-2023
Built microservices

EDUCATION
BS Computer Science, University of Test"""

        resume = self.analyzer.analyze(raw_text)

        self.assertEqual(resume.name, "John Doe")
        self.assertEqual(resume.contact_info.get('email'), "john@example.com")
        self.assertIn("Python", resume.skills)
        self.assertTrue(len(resume.sections) >= 3)

    def test_extract_contact_info(self):
        """Test contact information extraction."""
        text = """Jane Smith
jane.smith@company.org
linkedin.com/in/janesmith
www.janesmith.com"""

        contact = self.analyzer._extract_contact_info(text)

        self.assertEqual(contact['email'], "jane.smith@company.org")
        self.assertEqual(contact['linkedin'], "linkedin.com/in/janesmith")
        self.assertEqual(contact['website'], "www.janesmith.com")

    def test_extract_sections(self):
        """Test section extraction from resume."""
        text = """NAME

SUMMARY
This is summary

EXPERIENCE
Job 1 details

EDUCATION
Degree info"""

        sections = self.analyzer._extract_sections(text)

        section_titles = [s.title.lower() for s in sections]
        self.assertIn("summary", section_titles)
        self.assertIn("experience", section_titles)
        self.assertIn("education", section_titles)


class TestJobDescriptionAnalyzer(unittest.TestCase):
    """Tests for JobDescriptionAnalyzer class."""

    def setUp(self):
        self.analyzer = JobDescriptionAnalyzer()

    def test_analyze_basic_job(self):
        """Test analyzing a basic job description."""
        job_text = """Software Engineer

Requirements:
- Python
- AWS
- 5+ years experience

Preferred:
- Kubernetes
- React"""

        job = self.analyzer.analyze(job_text)

        self.assertEqual(job.title, "Software Engineer")
        # Check case-insensitively since skill extraction may vary in case
        all_skills_lower = [s.lower() for s in job.required_skills]
        self.assertIn("python", all_skills_lower)
        self.assertTrue(any('aws' in s.lower() for s in job.required_skills))
        self.assertEqual(job.experience_years, 5)

    def test_extract_experience_years(self):
        """Test extracting years of experience requirement."""
        test_cases = [
            ("Requires 5+ years of experience", 5),
            ("Minimum of 3 years experience", 3),
            ("7 years in software development", 7),
            ("No experience mentioned", None),
        ]

        for text, expected in test_cases:
            result = self.analyzer._extract_experience_years(text)
            self.assertEqual(result, expected, f"Failed for: {text}")

    def test_extract_skills(self):
        """Test skill extraction from job description."""
        text = "We need Python, JavaScript, and AWS expertise. Kubernetes preferred."

        skills = self.analyzer._extract_skills(text)

        # Check case-insensitively
        skills_lower = [s.lower() for s in skills]
        self.assertIn("python", skills_lower)
        self.assertTrue(any('aws' in s.lower() for s in skills))


class TestATSScorer(unittest.TestCase):
    """Tests for ATSScorer class."""

    def setUp(self):
        self.resume = ParsedResume()
        self.resume.name = "John Doe"
        self.resume.raw_text = """John Doe
john@example.com | 555-123-4567

SUMMARY
Experienced software engineer with Python and AWS

SKILLS
Python, AWS, Docker, Kubernetes

EXPERIENCE
Senior Engineer at TechCorp
Built Python applications on AWS infrastructure
Led team of 5 developers"""
        self.resume.skills = ["Python", "AWS", "Docker", "Kubernetes"]
        self.resume.contact_info = {'email': 'john@example.com', 'phone': '555-123-4567'}
        self.resume.sections = [
            ResumeSection("Summary", "Experienced software engineer", 0),
            ResumeSection("Skills", "Python, AWS, Docker", 1),
            ResumeSection("Experience", "Senior Engineer at TechCorp", 2),
        ]

        self.job = JobRequirements()
        self.job.required_skills = ["Python", "AWS"]
        self.job.preferred_skills = ["Kubernetes", "Terraform"]
        self.job.responsibilities = ["Build scalable applications", "Lead development teams"]
        self.job.experience_years = 5
        self.job.keywords = ["Python", "AWS", "scalable", "leadership"]

        self.scorer = ATSScorer(self.resume, self.job)

    def test_score_structure(self):
        """Test that score returns correct structure."""
        scores = self.scorer.score()

        self.assertIn('overall', scores)
        self.assertIn('sections', scores)
        self.assertIn('suggestions', scores)
        self.assertIn('keyword_match', scores)
        self.assertIn('format_score', scores)
        self.assertIn('content_score', scores)

    def test_skills_match_scoring(self):
        """Test skills match scoring."""
        scores = self.scorer.score()

        # Should have good score since Python and AWS are present
        self.assertGreater(scores['sections']['skills_match'], 50)

    def test_missing_skills_detection(self):
        """Test detection of missing skills."""
        missing = self.scorer._get_missing_skills()

        # Terraform should be missing
        self.assertIn("Terraform", missing)

    def test_keyword_match_analysis(self):
        """Test keyword matching analysis."""
        keyword_match = self.scorer._analyze_keyword_match()

        self.assertIn('found', keyword_match)
        self.assertIn('missing', keyword_match)
        self.assertIn('required_found', keyword_match)
        self.assertIn('required_missing', keyword_match)

    def test_suggestions_generation(self):
        """Test that suggestions are generated."""
        scores = self.scorer.score()

        self.assertIsInstance(scores['suggestions'], list)
        self.assertTrue(len(scores['suggestions']) > 0)

    def test_format_scoring(self):
        """Test format scoring."""
        scores = self.scorer.score()

        # Should have good format score with complete contact info
        self.assertGreater(scores['format_score'], 70)

    def test_content_scoring(self):
        """Test content quality scoring."""
        scores = self.scorer.score()

        # Should detect action verbs and content quality
        self.assertIn('content_score', scores)


class TestCoverLetterGenerator(unittest.TestCase):
    """Tests for CoverLetterGenerator class."""

    def setUp(self):
        self.resume = ParsedResume()
        self.resume.name = "John Doe"
        self.resume.raw_text = "Experienced software engineer with Python expertise"
        self.resume.skills = ["Python", "AWS", "Docker"]
        self.resume.contact_info = {
            'email': 'john@example.com',
            'phone': '555-123-4567',
            'linkedin': 'linkedin.com/in/johndoe'
        }
        self.resume.experience = [{
            'raw': 'Senior Engineer at TechCorp',
            'description': 'Led development of Python applications'
        }]

        self.job = JobRequirements()
        self.job.title = "Senior Software Engineer"
        self.job.company = "TechCorp"
        self.job.required_skills = ["Python", "AWS"]
        self.job.preferred_skills = ["Docker"]
        self.job.responsibilities = ["Build scalable systems", "Lead teams"]

        self.generator = CoverLetterGenerator(self.resume, self.job)

    def test_generate_structure(self):
        """Test that generated cover letter has proper structure."""
        letter = self.generator.generate()

        # Should contain key sections
        self.assertIn("John Doe", letter)
        self.assertIn("Dear", letter)  # Salutation
        self.assertIn("Senior Software Engineer", letter)  # Job title
        self.assertIn("Sincerely", letter)  # Closing

    def test_header_generation(self):
        """Test header generation."""
        header = self.generator._generate_header()

        self.assertIn("John Doe", header)
        self.assertIn("john@example.com", header)
        self.assertIn("555-123-4567", header)

    def test_opening_generation(self):
        """Test opening paragraph generation."""
        opening = self.generator._generate_opening()

        self.assertIn("Senior Software Engineer", opening)
        self.assertIn("TechCorp", opening)

    def test_body_generation(self):
        """Test body paragraphs generation."""
        body = self.generator._generate_body()

        self.assertTrue(len(body) > 100)
        self.assertIn("Python", body)  # Should mention matching skills

    def test_skill_inclusion(self):
        """Test that matching skills are included."""
        letter = self.generator.generate()

        # Should mention at least one matching skill
        self.assertTrue(
            "Python" in letter or "AWS" in letter or "Docker" in letter
        )


class TestResumeTailor(unittest.TestCase):
    """Tests for ResumeTailor class."""

    def setUp(self):
        self.resume = ParsedResume()
        self.resume.name = "John Doe"
        self.resume.summary = "Software engineer with diverse experience"
        self.resume.skills = ["Python", "Java", "AWS", "React", "Docker"]
        self.resume.experience = [
            {'raw': 'Python Developer role', 'description': 'Worked with Python and AWS'},
            {'raw': 'Java Developer role', 'description': 'Worked with Java and Spring'},
        ]

        self.job = JobRequirements()
        self.job.required_skills = ["Python", "AWS"]
        self.job.keywords = ["Python", "AWS", "cloud"]

        self.tailor = ResumeTailor(self.resume, self.job)

    def test_tailor_preserves_name(self):
        """Test that tailoring preserves candidate name."""
        tailored = self.tailor.tailor()
        self.assertEqual(tailored.name, "John Doe")

    def test_skills_prioritization(self):
        """Test that matching skills are prioritized."""
        tailored = self.tailor.tailor()

        # Python and AWS should come first
        if len(tailored.skills) >= 2:
            self.assertTrue(
                "Python" in tailored.skills[0] or "AWS" in tailored.skills[1]
            )

    def test_experience_reordering(self):
        """Test that experience is reordered by relevance."""
        tailored = self.tailor.tailor()

        # Python experience should be first
        if tailored.experience:
            self.assertIn("Python", tailored.experience[0]['raw'])


class TestResumeAdaptationSkill(unittest.TestCase):
    """Integration tests for ResumeAdaptationSkill."""

    def setUp(self):
        self.skill = ResumeAdaptationSkill()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_test_files(self):
        """Create test resume and job description files."""
        resume_file = Path(self.temp_dir) / "resume.txt"
        job_file = Path(self.temp_dir) / "job.txt"

        resume_content = """John Doe
john@example.com | 555-123-4567

SUMMARY
Software engineer with 5 years Python experience

SKILLS
Python, AWS, Docker

EXPERIENCE
Software Engineer | TechCorp | 2020-2023
- Built Python applications
- Deployed on AWS"""

        job_content = """Software Engineer

Requirements:
- Python programming
- AWS experience
- Docker containers"""

        resume_file.write_text(resume_content)
        job_file.write_text(job_content)

        return str(resume_file), str(job_file)

    def test_end_to_end_basic(self):
        """Test end-to-end skill execution."""
        resume_path, job_path = self.create_test_files()

        # Mock args object
        args = Mock()
        args.resume = [resume_path]
        args.job = job_path
        args.requirements = ""
        args.output_name = "test_output"
        args.output_dir = self.temp_dir
        args.ats_score = False
        args.cover_letter = False

        results = self.skill.run(args)

        self.assertTrue(results['success'])
        self.assertIsNotNone(results['docx_path'])

    def test_with_ats_scoring(self):
        """Test skill with ATS scoring enabled."""
        resume_path, job_path = self.create_test_files()

        args = Mock()
        args.resume = [resume_path]
        args.job = job_path
        args.requirements = ""
        args.output_name = "test_output"
        args.output_dir = self.temp_dir
        args.ats_score = True
        args.cover_letter = False

        results = self.skill.run(args)

        self.assertTrue(results['success'])
        self.assertIsNotNone(results['ats_score'])
        self.assertIn('overall', results['ats_score'])

    def test_with_cover_letter(self):
        """Test skill with cover letter generation."""
        resume_path, job_path = self.create_test_files()

        args = Mock()
        args.resume = [resume_path]
        args.job = job_path
        args.requirements = ""
        args.output_name = "test_output"
        args.output_dir = self.temp_dir
        args.ats_score = False
        args.cover_letter = True

        results = self.skill.run(args)

        self.assertTrue(results['success'])
        # Cover letter text file should exist
        cover_txt = Path(self.temp_dir) / "test_output_cover_letter.txt"
        self.assertTrue(cover_txt.exists())


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def test_empty_resume(self):
        """Test handling of empty resume."""
        resume = ParsedResume()
        resume.raw_text = ""
        resume.name = ""
        resume.skills = []

        analyzer = ResumeAnalyzer()
        result = analyzer.analyze("")

        # Should not crash, should return empty but valid ParsedResume
        self.assertIsInstance(result, ParsedResume)

    def test_empty_job_description(self):
        """Test handling of empty job description."""
        job = JobRequirements()

        analyzer = JobDescriptionAnalyzer()
        result = analyzer.analyze("")

        self.assertIsInstance(result, JobRequirements)
        self.assertEqual(result.required_skills, [])

    def test_missing_contact_info(self):
        """Test ATS scoring with missing contact info."""
        resume = ParsedResume()
        resume.raw_text = "John Doe\nNo contact info here"
        resume.contact_info = {}
        resume.sections = [ResumeSection("Summary", "Test", 0)]

        job = JobRequirements()

        scorer = ATSScorer(resume, job)
        scores = scorer.score()

        # Format score should be lower due to missing contact
        self.assertLess(scores['format_score'], 100)

    def test_very_long_resume(self):
        """Test handling of very long resume."""
        resume = ParsedResume()
        resume.raw_text = "Word " * 2000  # Very long resume
        resume.contact_info = {'email': 'test@test.com'}
        resume.sections = [ResumeSection("Summary", "Test", 0)]

        job = JobRequirements()

        scorer = ATSScorer(resume, job)
        scores = scorer.score()

        # Should warn about length
        self.assertLess(scores['format_score'], 100)


def run_demo():
    """Run a demonstration of all features."""
    print("=" * 60)
    print("RESUME ADAPTATION SKILL - DEMO")
    print("=" * 60)

    # Create sample resume
    sample_resume = """Jane Smith
jane.smith@email.com | (555) 123-4567
linkedin.com/in/janesmith

PROFESSIONAL SUMMARY
Results-driven software engineer with 6+ years of experience building scalable web applications and leading development teams.

TECHNICAL SKILLS
Python, Django, AWS, Docker, PostgreSQL, React, JavaScript, Git, REST APIs, Microservices

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021-Present
- Lead a team of 5 engineers developing cloud-based SaaS platform
- Architected and implemented microservices infrastructure using Docker and AWS
- Improved system performance by 40% through optimization initiatives
- Mentored junior developers and conducted code reviews

Software Engineer | StartupXYZ | 2018-2021
- Developed RESTful APIs using Python and Django
- Built React frontend components for customer dashboard
- Implemented CI/CD pipelines using GitHub Actions
- Collaborated with product team to deliver features on schedule

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2018
"""

    # Create sample job description
    sample_job = """Senior Backend Engineer

About the Role:
We are seeking an experienced backend engineer to join our growing team.

Requirements:
- 5+ years of experience with Python
- Strong experience with AWS services (EC2, S3, Lambda)
- Experience with Docker and containerization
- Proficiency with PostgreSQL or similar databases
- Experience with microservices architecture
- Bachelor's degree in Computer Science or related field

Preferred:
- Experience with Django or Flask
- Knowledge of React or frontend frameworks
- Team leadership experience
- Experience with CI/CD pipelines

Responsibilities:
- Design and build scalable backend services
- Lead technical projects and mentor team members
- Collaborate with cross-functional teams
- Optimize system performance and reliability
"""

    print("\n📄 SAMPLE RESUME:")
    print("-" * 40)
    print(sample_resume[:500] + "...")

    print("\n💼 SAMPLE JOB DESCRIPTION:")
    print("-" * 40)
    print(sample_job[:500] + "...")

    # Analyze resume
    print("\n🔍 ANALYZING RESUME...")
    resume_analyzer = ResumeAnalyzer()
    parsed_resume = resume_analyzer.analyze(sample_resume)

    print(f"   Name: {parsed_resume.name}")
    print(f"   Email: {parsed_resume.contact_info.get('email')}")
    print(f"   Skills found: {len(parsed_resume.skills)}")
    print(f"   Sections: {[s.title for s in parsed_resume.sections]}")

    # Analyze job
    print("\n🎯 ANALYZING JOB DESCRIPTION...")
    job_analyzer = JobDescriptionAnalyzer()
    job_requirements = job_analyzer.analyze(sample_job)

    print(f"   Title: {job_requirements.title}")
    print(f"   Required skills: {job_requirements.required_skills}")
    print(f"   Preferred skills: {job_requirements.preferred_skills}")
    print(f"   Years of experience required: {job_requirements.experience_years}")

    # ATS Scoring
    print("\n📊 ATS SCORING...")
    ats_scorer = ATSScorer(parsed_resume, job_requirements)
    ats_results = ats_scorer.score()

    print(f"   Overall Score: {ats_results['overall']}/100")
    print("\n   Section Scores:")
    for section, score in ats_results['sections'].items():
        print(f"      {section}: {score}/100")
    print("\n   Suggestions:")
    for suggestion in ats_results['suggestions']:
        print(f"      • {suggestion}")

    # Cover Letter Generation
    print("\n💌 GENERATING COVER LETTER...")
    cover_gen = CoverLetterGenerator(parsed_resume, job_requirements)
    cover_letter = cover_gen.generate()

    print("\n   Generated Cover Letter (first 500 chars):")
    print("   " + "-" * 40)
    print("   " + cover_letter[:500].replace("\n", "\n   "))
    print("   ...")

    # Resume Tailoring
    print("\n✨ TAILORING RESUME...")
    tailor = ResumeTailor(parsed_resume, job_requirements)
    tailored_resume = tailor.tailor()

    print(f"   Prioritized skills: {tailored_resume.skills[:5]}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print("\nThis skill can:")
    print("  ✓ Parse resumes from PDF, DOCX, TXT, MD files")
    print("  ✓ Extract job requirements from text, URLs, or files")
    print("  ✓ Calculate ATS compatibility scores")
    print("  ✓ Generate tailored cover letters")
    print("  ✓ Create optimized DOCX and PDF outputs")
    print("\nRun with --help for usage information.")


if __name__ == '__main__':
    import argparse

    test_parser = argparse.ArgumentParser()
    test_parser.add_argument('--demo', action='store_true', help='Run demo instead of tests')
    test_parser.add_argument('--test-ats', action='store_true', help='Test only ATS scoring')
    test_parser.add_argument('--test-cover-letter', action='store_true', help='Test only cover letter')

    # Parse known args to handle pytest arguments
    args, remaining = test_parser.parse_known_args()
    sys.argv = [sys.argv[0]] + remaining

    if args.demo:
        run_demo()
    elif args.test_ats:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestATSScorer)
        unittest.TextTestRunner(verbosity=2).run(suite)
    elif args.test_cover_letter:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCoverLetterGenerator)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        # Run all tests
        unittest.main(verbosity=2)
