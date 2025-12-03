# Solutions for the 4 Issues

## Issue 1: Fix Persistent Store Error

### Problem
Line 2146 uses `if retrieved['embeddings']:` which fails when `retrieved['embeddings']` is a numpy array or list with multiple elements.

### Solution
Replace the boolean check with an explicit length check.

**File**: `app.py`  
**Line**: 2146

**Current Code**:
```python
if retrieved and 'embeddings' in retrieved and retrieved['embeddings']:
```

**Fixed Code**:
```python
if retrieved and 'embeddings' in retrieved and retrieved['embeddings'] is not None and len(retrieved['embeddings']) > 0:
```

**Why this works**: Explicitly checks that the embeddings list exists, is not None, and has at least one element, avoiding the ambiguous truthiness check.

---

## Issue 2: Improve Rate Limit Messaging

### Problem
Rate limit retry messages are too verbose and shown for every attempt, causing user confusion.

### Solution
Reduce verbosity by:
1. Only showing detailed messages on first retry attempt
2. Using a progress indicator for subsequent retries
3. Adding a flag to suppress messages for embedding API calls (which are expected to hit limits)

**File**: `app.py`  
**Lines**: 180-258 (api_call_with_retry function)

**Current Code** (lines 202-214):
```python
elif response.status_code == 429:
    if attempt < max_retries - 1:
        fallback_delay = _calculate_exponential_delay(initial_delay, attempt, max_delay)
        delay, delay_source = _determine_retry_delay(response, fallback_delay, max_delay)
        source_note = ""
        if delay_source != "fallback":
            source_note = f" (server hint: {delay_source})"
        # Show user-friendly message
        st.warning(
            f"⏳ Rate limit reached. Retrying in {delay} seconds{source_note}... "
            f"(Attempt {attempt + 1}/{max_retries})"
        )
        time.sleep(delay)
        continue
```

**Fixed Code**:
```python
elif response.status_code == 429:
    if attempt < max_retries - 1:
        fallback_delay = _calculate_exponential_delay(initial_delay, attempt, max_delay)
        delay, delay_source = _determine_retry_delay(response, fallback_delay, max_delay)
        source_note = ""
        if delay_source != "fallback":
            source_note = f" (server hint: {delay_source})"
        
        # Only show detailed message on first retry, use progress indicator for subsequent retries
        if attempt == 0:
            st.warning(
                f"⏳ Rate limit reached. Retrying in {delay} seconds{source_note}... "
                f"(Attempt {attempt + 1}/{max_retries})"
            )
        else:
            # Use progress indicator for subsequent retries (less intrusive)
            progress_text = f"⏳ Retrying... ({attempt + 1}/{max_retries})"
            st.caption(progress_text)
        
        time.sleep(delay)
        continue
```

**Alternative Solution** (if you want to suppress messages entirely for embedding calls):
Add a `suppress_messages` parameter to `api_call_with_retry` and pass it for embedding API calls.

---

## Issue 3: Fix Missing Items from Field Filtering

### Problem
1. Domain filtering only checks first 2000 characters
2. Only 9 predefined domains in dictionary
3. Salary filtering includes all jobs without salary info
4. Limited keyword matching

### Solution

#### 3A: Fix Domain Filtering

**File**: `app.py`  
**Lines**: 2745-2774

**Current Code** (line 2765):
```python
desc_lower = job.get('description', '').lower()[:2000]  # Check first 2000 chars
```

**Fixed Code**:
```python
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
        # Check full description, not just first 2000 chars
        title_lower = job.get('title', '').lower()
        desc_lower = job.get('description', '').lower()  # Check full description
        company_lower = job.get('company', '').lower()
        combined = f"{title_lower} {desc_lower} {company_lower}"
        
        for domain in target_domains:
            keywords = domain_keywords.get(domain, [domain.lower()])
            # Use case-insensitive matching with word boundaries for better accuracy
            if any(keyword.lower() in combined for keyword in keywords):
                filtered.append(job)
                break  # Job matched a domain, no need to check other domains
    
    return filtered if filtered else jobs  # Return all if no matches
```

**Key Changes**:
1. Removed `[:2000]` limit - now checks full description
2. Added company name to search
3. Expanded domain keywords dictionary with more domains and keywords
4. Better keyword matching

#### 3B: Fix Salary Filtering

**File**: `app.py`  
**Lines**: 2776-2798

**Current Code**:
```python
def filter_jobs_by_salary(jobs, min_salary):
    """Filter jobs by minimum salary expectation"""
    if not min_salary or min_salary <= 0:
        return jobs
    
    filtered = []
    for job in jobs:
        salary_str = job.get('salary', '')
        description = job.get('description', '')
        
        # Try to extract salary
        min_sal, max_sal = extract_salary_from_text(salary_str)
        if not min_sal:
            min_sal, max_sal = extract_salary_from_text(description[:5000])
        
        # If we found a salary and it meets the minimum, include it
        # If no salary found, include it (can't filter what we don't know)
        if min_sal and min_sal >= min_salary:
            filtered.append(job)
        elif not min_sal:
            filtered.append(job)  # Include jobs without salary info
    
    return filtered
```

**Fixed Code**:
```python
def filter_jobs_by_salary(jobs, min_salary):
    """Filter jobs by minimum salary expectation"""
    if not min_salary or min_salary <= 0:
        return jobs
    
    filtered = []
    jobs_without_salary = []
    
    for job in jobs:
        salary_str = job.get('salary', '')
        description = job.get('description', '')
        
        # Try to extract salary from salary field first
        min_sal, max_sal = extract_salary_from_text(salary_str)
        
        # If not found, try full description (not just first 5000 chars)
        if not min_sal:
            min_sal, max_sal = extract_salary_from_text(description)  # Check full description
        
        # If we found a salary
        if min_sal:
            # Include if minimum salary meets requirement OR if salary range overlaps with requirement
            # (e.g., if job is 50k-70k and user wants 60k, include it because 70k >= 60k)
            if min_sal >= min_salary or (max_sal and max_sal >= min_salary):
                filtered.append(job)
            # else: job salary is too low, exclude it
        else:
            # No salary info found - store separately to add at end if no matches
            jobs_without_salary.append(job)
    
    # If we have matches, return only matches
    # If no matches but we have jobs without salary, include those (user can decide)
    if filtered:
        return filtered
    elif jobs_without_salary:
        # No jobs met salary requirement, but return jobs without salary info
        # so user knows there are jobs available (they just don't have salary listed)
        return jobs_without_salary
    else:
        # No jobs at all
        return []
```

**Key Changes**:
1. Checks full description, not just first 5000 chars
2. Handles salary ranges better (includes if range overlaps with requirement)
3. Only includes jobs without salary if no jobs meet the requirement
4. Better logic flow

**Alternative**: Add a parameter to control whether to include jobs without salary:
```python
def filter_jobs_by_salary(jobs, min_salary, include_no_salary=True):
    # ... same logic but use include_no_salary flag
    if filtered:
        return filtered
    elif include_no_salary and jobs_without_salary:
        return jobs_without_salary
    else:
        return []
```

---

## Issue 4: Fix Auto-loading/Refreshing

### Problem
`setInterval` runs every 1 second to check theme, causing unnecessary DOM manipulation and potential React re-renders.

### Solution
Replace polling with event-driven approach and add cleanup.

**File**: `app.py`  
**Lines**: 1035-1045

**Current Code**:
```javascript
// Re-apply theme periodically to catch dynamically loaded content
setInterval(function() {
    const currentPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const hasDarkTheme = document.documentElement.hasAttribute('data-theme');
    
    if (currentPrefersDark && !hasDarkTheme) {
        updateTheme();
    } else if (!currentPrefersDark && hasDarkTheme) {
        updateTheme();
    }
}, 1000); // Check every second
```

**Fixed Code** (Option 1 - Remove interval, rely on event listeners):
```javascript
// Remove the setInterval - event listeners should be sufficient
// The mediaQuery.addEventListener('change', updateTheme) already handles theme changes
// For dynamically loaded content, we can use MutationObserver instead

// Use MutationObserver to watch for DOM changes and re-apply theme if needed
// This is more efficient than polling every second
if (typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver(function(mutations) {
        // Only check theme if significant DOM changes occurred
        // Check at most once per second (throttle)
        let lastCheck = 0;
        const now = Date.now();
        if (now - lastCheck > 1000) {
            lastCheck = now;
            const currentPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            const hasDarkTheme = document.documentElement.hasAttribute('data-theme');
            
            if ((currentPrefersDark && !hasDarkTheme) || (!currentPrefersDark && hasDarkTheme)) {
                updateTheme();
            }
        }
    });
    
    // Observe changes to document body and Streamlit app container
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Store observer for potential cleanup (though it's not critical in this context)
    window.__themeObserver = observer;
}
```

**Fixed Code** (Option 2 - Keep interval but make it much less frequent):
```javascript
// Re-apply theme periodically to catch dynamically loaded content
// Use longer interval to reduce performance impact
const themeCheckInterval = setInterval(function() {
    const currentPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const hasDarkTheme = document.documentElement.hasAttribute('data-theme');
    
    // Only update if theme actually needs to change
    if (currentPrefersDark && !hasDarkTheme) {
        updateTheme();
    } else if (!currentPrefersDark && hasDarkTheme) {
        updateTheme();
    }
}, 5000); // Check every 5 seconds instead of 1 second

// Clean up interval if page unloads (good practice)
if (window.addEventListener) {
    window.addEventListener('beforeunload', function() {
        if (themeCheckInterval) {
            clearInterval(themeCheckInterval);
        }
    });
}
```

**Recommended**: Use Option 1 (MutationObserver) as it's event-driven and more efficient.

**Complete Fixed Section** (replace lines 1029-1045):
```javascript
// Also update theme when Streamlit app is ready (for dynamic content)
if (window.parent !== window) {
    // Running in iframe (Streamlit Cloud)
    window.addEventListener('load', updateTheme);
}

// Use MutationObserver instead of setInterval for better performance
// This watches for DOM changes and only checks theme when needed
if (typeof MutationObserver !== 'undefined') {
    let lastThemeCheck = 0;
    const themeCheckThrottle = 2000; // Check at most once every 2 seconds
    
    const themeObserver = new MutationObserver(function() {
        const now = Date.now();
        if (now - lastThemeCheck < themeCheckThrottle) {
            return; // Throttle checks
        }
        lastThemeCheck = now;
        
        const currentPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const hasDarkTheme = document.documentElement.hasAttribute('data-theme');
        
        if ((currentPrefersDark && !hasDarkTheme) || (!currentPrefersDark && hasDarkTheme)) {
            updateTheme();
        }
    });
    
    // Observe document body for changes (Streamlit dynamically loads content)
    themeObserver.observe(document.body, { 
        childList: true, 
        subtree: true,
        attributes: false // We don't need to watch attribute changes
    });
}
```

---

## Summary of All Fixes

| Issue | File | Lines | Change Type | Impact |
|-------|------|-------|-------------|--------|
| 1. Persistent Store | `app.py` | 2146 | Fix boolean check | High - Fixes embedding caching |
| 2. Rate Limit Messages | `app.py` | 210-213 | Reduce verbosity | Medium - Better UX |
| 3A. Domain Filtering | `app.py` | 2745-2774 | Expand search scope | High - More accurate filtering |
| 3B. Salary Filtering | `app.py` | 2776-2798 | Improve logic | High - Better salary matching |
| 4. Auto-loading | `app.py` | 1035-1045 | Replace setInterval | Medium - Better performance |

---

## Testing Recommendations

After applying fixes:

1. **Issue 1**: Test that embeddings are cached and reused on subsequent runs
2. **Issue 2**: Test that rate limit messages are less intrusive
3. **Issue 3**: Test filtering with various domains and salary ranges
4. **Issue 4**: Monitor browser performance and check that page doesn't keep refreshing
