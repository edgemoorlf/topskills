"""
Resume Adaptation Skill for Claude Code

A skill that adapts resumes to match specific job descriptions,
producing tailored Word and PDF outputs.
"""

from .resume_adapter import (
    ResumeAdaptationSkill,
    DocumentParser,
    ResumeAnalyzer,
    JobDescriptionAnalyzer,
    ResumeTailor,
    ResumeDocumentBuilder,
    ParsedResume,
    JobRequirements,
)

__version__ = "1.0.0"
__all__ = [
    "ResumeAdaptationSkill",
    "DocumentParser",
    "ResumeAnalyzer",
    "JobDescriptionAnalyzer",
    "ResumeTailor",
    "ResumeDocumentBuilder",
    "ParsedResume",
    "JobRequirements",
]
