"""Job match analysis functions including salary extraction and filtering"""
import json
import re
import streamlit as st
import requests
import numpy as np
from modules.utils import get_text_generator, api_call_with_retry


def extract_salary_from_text(text):
    """Extract salary information from job description text using LLM"""
    if not text:
        return None, None
    
    text_for_extraction = text[:3000] if len(text) > 3000 else text
    
    try:
        text_gen = get_text_generator()
        if text_gen is None:
            return None, None
        
        prompt = f"""Extract salary information from this job description text. 
Look for salary ranges, amounts, and compensation details. Normalize everything to monthly HKD (Hong Kong Dollars).

JOB DESCRIPTION TEXT:
{text_for_extraction}

Extract and return salary information as JSON with this structure:
{{
    "min_salary_hkd_monthly": <number or null>,
    "max_salary_hkd_monthly": <number or null>,
    "found": true/false,
    "raw_text": "the exact salary text found in the description"
}}

Rules:
- Convert all amounts to monthly HKD (multiply annual by 12, weekly by 4.33, daily by 22)
- If only one amount is found, set both min and max to that value
- If a range is found (e.g., "60k-80k"), extract both min and max
- Handle formats like "competitive", "based on experience", "around 60k-80k annually" by extracting the numeric range
- If no salary is found, set "found": false and return null for min/max
- Always return valid JSON, no additional text"""

        payload = {
            "messages": [
                {"role": "system", "content": "You are a salary extraction expert. Extract salary information and normalize to monthly HKD. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }
        
        def make_request():
            return requests.post(
                text_gen.url,
                headers=text_gen.headers,
                json=payload,
                timeout=30
            )
        
        response = api_call_with_retry(make_request, max_retries=2)
        
        if response and response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            if text_gen.token_tracker and 'usage' in result:
                usage = result['usage']
                prompt_tokens = usage.get('prompt_tokens', 0)
                completion_tokens = usage.get('completion_tokens', 0)
                text_gen.token_tracker.add_completion_tokens(prompt_tokens, completion_tokens)
            
            try:
                salary_data = json.loads(content)
                if salary_data.get('found', False):
                    min_sal = salary_data.get('min_salary_hkd_monthly')
                    max_sal = salary_data.get('max_salary_hkd_monthly')
                    if min_sal is not None and max_sal is not None:
                        return int(min_sal), int(max_sal)
                    elif min_sal is not None:
                        return int(min_sal), int(min_sal * 1.2)
            except (json.JSONDecodeError, ValueError, TypeError) as e:
                pass
        
        return extract_salary_from_text_regex(text)
        
    except Exception as e:
        return extract_salary_from_text_regex(text)


def extract_salary_from_text_regex(text):
    """Fallback regex-based salary extraction"""
    if not text:
        return None, None
    
    patterns = [
        r'HKD\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*[-–—]\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:k|K)?)',
        r'(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*[-–—]\s*(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*HKD',
        r'HKD\s*\$?\s*(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*(?:per month|/month|/mth|monthly)',
        r'(\d{1,3}(?:,\d{3})*(?:k|K)?)\s*HKD\s*(?:per month|/month|/mth|monthly)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            match = matches[0]
            if isinstance(match, tuple) and len(match) == 2:
                min_sal = match[0].replace(',', '').replace('k', '000').replace('K', '000')
                max_sal = match[1].replace(',', '').replace('k', '000').replace('K', '000')
                try:
                    min_val = int(min_sal)
                    max_val = int(max_sal)
                    return min_val, max_val
                except:
                    pass
            elif isinstance(match, tuple) and len(match) == 1:
                sal = match[0].replace(',', '').replace('k', '000').replace('K', '000')
                try:
                    sal_val = int(sal)
                    return sal_val, int(sal_val * 1.2)
                except:
                    pass
    
    return None, None


def calculate_salary_band(matched_jobs):
    """Calculate estimated salary band from matched jobs"""
    salaries = []
    
    for result in matched_jobs:
        job = result['job']
        salary_str = job.get('salary', '')
        if salary_str and salary_str != 'Not specified':
            min_sal, max_sal = extract_salary_from_text(salary_str)
            if min_sal and max_sal:
                salaries.append((min_sal, max_sal))
        
        description = job.get('description', '')
        if description:
            min_sal, max_sal = extract_salary_from_text(description[:5000])
            if min_sal and max_sal:
                salaries.append((min_sal, max_sal))
    
    if not salaries:
        return 45000, 55000
    
    avg_min = int(np.mean([s[0] for s in salaries]))
    avg_max = int(np.mean([s[1] for s in salaries]))
    
    return avg_min, avg_max


def filter_jobs_by_domains(jobs, target_domains):
    """Filter jobs by target domains"""
    if not target_domains:
        return jobs
    
    filtered = []
    domain_keywords = {
        'FinTech': ['fintech', 'financial technology', 'blockchain', 'crypto', 'cryptocurrency', 'payment', 'banking technology', 'digital banking', 'wealthtech', 'insurtech'],
        'ESG & Sustainability': ['esg', 'sustainability', 'environmental', 'green', 'carbon', 'climate', 'renewable', 'sustainable'],
        'Data Analytics': ['data analytics', 'data analysis', 'business intelligence', 'bi', 'data science', 'data engineer', 'analytics', 'big data'],
        'Digital Transformation': ['digital transformation', 'digitalization', 'digital strategy', 'innovation', 'digital', 'transformation'],
        'Investment Banking': ['investment banking', 'ib', 'm&a', 'mergers', 'acquisitions', 'capital markets', 'equity research', 'corporate finance'],
        'Consulting': ['consulting', 'consultant', 'advisory', 'strategy consulting', 'management consulting'],
        'Technology': ['software', 'technology', 'tech', 'engineering', 'developer', 'programming', 'it', 'information technology', 'software engineer'],
        'Healthcare': ['healthcare', 'medical', 'health', 'hospital', 'clinical', 'pharmaceutical', 'biotech'],
        'Education': ['education', 'teaching', 'academic', 'university', 'school', 'e-learning', 'edtech'],
        'Real Estate': ['real estate', 'property', 'realty', 'property management', 'real estate development'],
        'Retail & E-commerce': ['retail', 'e-commerce', 'ecommerce', 'online retail', 'retail management'],
        'Marketing & Advertising': ['marketing', 'advertising', 'brand', 'digital marketing', 'social media marketing'],
        'Legal': ['legal', 'law', 'attorney', 'lawyer', 'compliance', 'regulatory'],
        'Human Resources': ['human resources', 'hr', 'recruitment', 'talent acquisition', 'people operations'],
        'Operations': ['operations', 'operations management', 'supply chain', 'logistics', 'procurement']
    }
    
    for job in jobs:
        title_lower = job.get('title', '').lower()
        desc_lower = job.get('description', '').lower()
        company_lower = job.get('company', '').lower()
        combined = f"{title_lower} {desc_lower} {company_lower}"
        
        for domain in target_domains:
            keywords = domain_keywords.get(domain, [domain.lower()])
            if any(keyword.lower() in combined for keyword in keywords):
                filtered.append(job)
                break
    
    return filtered if filtered else jobs


def filter_jobs_by_salary(jobs, min_salary):
    """Filter jobs by minimum salary expectation"""
    if not min_salary or min_salary <= 0:
        return jobs
    
    filtered = []
    jobs_without_salary = []
    
    for job in jobs:
        salary_str = job.get('salary', '')
        description = job.get('description', '')
        
        min_sal, max_sal = extract_salary_from_text(salary_str)
        
        if not min_sal:
            min_sal, max_sal = extract_salary_from_text(description)
        
        if min_sal:
            if min_sal >= min_salary or (max_sal and max_sal >= min_salary):
                filtered.append(job)
        else:
            jobs_without_salary.append(job)
    
    if filtered:
        return filtered
    elif jobs_without_salary:
        return jobs_without_salary
    else:
        return []
