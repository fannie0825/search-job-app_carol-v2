"""Resume generator module"""
from .formatters import (
    generate_docx_from_json,
    generate_pdf_from_json,
    format_resume_as_text
)

__all__ = [
    'generate_docx_from_json',
    'generate_pdf_from_json',
    'format_resume_as_text'
]
