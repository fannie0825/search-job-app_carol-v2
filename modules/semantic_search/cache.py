"""Job search caching functionality"""
import streamlit as st
from datetime import datetime, timedelta


def is_cache_valid(cache_entry):
    """Check if cache entry is still valid (not expired)."""
    if not cache_entry or not isinstance(cache_entry, dict):
        return False
    
    expires_at = cache_entry.get('expires_at')
    if expires_at is None:
        return False
    
    if isinstance(expires_at, str):
        try:
            expires_at = datetime.fromisoformat(expires_at)
        except ValueError:
            try:
                expires_at = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return False
    
    return datetime.now() < expires_at


def _build_jobs_cache_key(query, location, max_rows, job_type, country):
    """Create a unique cache key for job searches."""
    normalized_query = (query or "").strip().lower()
    return "|".join([
        normalized_query,
        (location or "").strip().lower(),
        str(max_rows),
        (job_type or "").strip().lower(),
        (country or "").strip().lower()
    ])


def _ensure_jobs_cache_structure():
    """Ensure jobs_cache is always a dict keyed by cache keys (handles legacy formats)."""
    if 'jobs_cache' not in st.session_state or not isinstance(st.session_state.jobs_cache, dict):
        st.session_state.jobs_cache = {}
        return
    cache = st.session_state.jobs_cache
    if cache and 'jobs' in cache and isinstance(cache['jobs'], list):
        cache_key = cache.get('cache_key') or _build_jobs_cache_key(
            cache.get('query', ''),
            cache.get('location', 'Hong Kong'),
            cache.get('count', len(cache.get('jobs', []))),
            cache.get('job_type', 'fulltime'),
            cache.get('country', 'hk')
        )
        st.session_state.jobs_cache = {cache_key: {**cache, 'cache_key': cache_key}}


def _get_cached_jobs(query, location, max_rows, job_type, country):
    """Return cached jobs for a given search signature if valid."""
    _ensure_jobs_cache_structure()
    cache_key = _build_jobs_cache_key(query, location, max_rows, job_type, country)
    cache_entry = st.session_state.jobs_cache.get(cache_key)
    if not cache_entry:
        return None
    if not is_cache_valid(cache_entry):
        st.session_state.jobs_cache.pop(cache_key, None)
        return None
    return cache_entry


def _store_jobs_in_cache(query, location, max_rows, job_type, country, jobs, cache_ttl_hours=168):
    """Persist job results in cache with TTL metadata."""
    _ensure_jobs_cache_structure()
    cache_key = _build_jobs_cache_key(query, location, max_rows, job_type, country)
    now = datetime.now()
    expires_at = now + timedelta(hours=cache_ttl_hours)
    st.session_state.jobs_cache[cache_key] = {
        'jobs': jobs,
        'count': len(jobs),
        'timestamp': now.isoformat(),
        'query': query,
        'location': location,
        'job_type': job_type,
        'country': country,
        'cache_key': cache_key,
        'expires_at': expires_at.isoformat()
    }
    return st.session_state.jobs_cache[cache_key]


def fetch_jobs_with_cache(scraper, query, location="Hong Kong", max_rows=25, job_type="fulltime",
                          country="hk", cache_ttl_hours=168, force_refresh=False):
    """
    Fetch jobs with session-level caching to avoid RapidAPI rate limits.
    Set force_refresh=True to bypass cache for a particular query.
    """
    if scraper is None:
        return []
    _ensure_jobs_cache_structure()
    cache_key = _build_jobs_cache_key(query, location, max_rows, job_type, country)
    if force_refresh:
        if cache_key in st.session_state.jobs_cache:
            st.caption("🔁 Forcing a fresh job search (cache bypassed)")
        st.session_state.jobs_cache.pop(cache_key, None)
    else:
        cache_entry = _get_cached_jobs(query, location, max_rows, job_type, country)
        if cache_entry:
            timestamp = cache_entry.get('timestamp')
            expires_at = cache_entry.get('expires_at')
            expires_in_minutes = None
            if isinstance(expires_at, str):
                try:
                    expires_dt = datetime.fromisoformat(expires_at)
                    expires_in_minutes = max(0, int((expires_dt - datetime.now()).total_seconds() // 60))
                except ValueError:
                    pass
            if timestamp and isinstance(timestamp, str):
                try:
                    ts_dt = datetime.fromisoformat(timestamp)
                    human_ts = ts_dt.strftime("%b %d %H:%M")
                except ValueError:
                    human_ts = timestamp
            else:
                human_ts = "earlier"
            remaining_text = f" (~{expires_in_minutes} min left)" if expires_in_minutes is not None else ""
            st.caption(f"♻️ Using cached job results from {human_ts}{remaining_text}")
            return cache_entry.get('jobs', [])
    jobs = scraper.search_jobs(query, location, max_rows, job_type, country)
    if jobs:
        _store_jobs_in_cache(query, location, max_rows, job_type, country, jobs, cache_ttl_hours)
    return jobs
