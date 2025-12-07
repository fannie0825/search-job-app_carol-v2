"""Analysis module for job match analysis"""
from .match_analysis import (
    extract_salary_from_text,
    extract_salary_from_text_regex,
    calculate_salary_band,
    filter_jobs_by_domains,
    filter_jobs_by_salary
)

__all__ = [
    'extract_salary_from_text',
    'extract_salary_from_text_regex',
    'calculate_salary_band',
    'filter_jobs_by_domains',
    'filter_jobs_by_salary'
]
