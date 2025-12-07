"""Dashboard display components"""
from typing import Optional

import streamlit as st
import pandas as pd
import gc
from modules.analysis import calculate_salary_band, filter_jobs_by_domains, filter_jobs_by_salary
from modules.semantic_search import SemanticJobSearch, fetch_jobs_with_cache, generate_and_store_resume_embedding
from modules.utils import get_embedding_generator, get_job_scraper, get_text_generator
from modules.utils.config import _determine_index_limit

# ---------------------------------------------------------------------------
# Design system helpers for the refreshed CareerLens dashboard experience
# ---------------------------------------------------------------------------

_DASHBOARD_STYLE_KEY = "_careerlens_dashboard_v2_styles"

_ICON_PATHS = {
    "eye": """
        <path d="M1 12s4-8 11-8 11 8-4 8-11 8-11-8-11-8Z"></path>
        <circle cx="12" cy="12" r="3"></circle>
    """,
    "layout-grid": """
        <rect x="3" y="3" width="7" height="7" rx="1"></rect>
        <rect x="14" y="3" width="7" height="7" rx="1"></rect>
        <rect x="14" y="14" width="7" height="7" rx="1"></rect>
        <rect x="3" y="14" width="7" height="7" rx="1"></rect>
    """,
    "file-text": """
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"></path>
        <path d="M14 2v6h6"></path>
        <path d="M16 13H8"></path>
        <path d="M16 17H8"></path>
    """,
    "target": """
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="6"></circle>
        <circle cx="12" cy="12" r="2"></circle>
    """,
    "settings": """
        <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"></path>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V11a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1Z"></path>
    """,
}


def _icon_svg(name: str, *, size: int = 20, stroke: Optional[str] = None, opacity: float = 1.0) -> str:
    """Return an inline SVG icon that matches the requested brand specs."""
    path = _ICON_PATHS.get(name, "")
    stroke_color = stroke or "var(--icon-default)"
    return (
        f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{stroke_color}" stroke-width="1.75" stroke-linecap="round" '
        f'stroke-linejoin="round" style="opacity:{opacity}; flex-shrink:0;">{path}</svg>'
    )


def _inject_dashboard_styles() -> None:
    """Inject the CareerLens v2 dashboard design tokens + layout styles once."""
    if st.session_state.get(_DASHBOARD_STYLE_KEY):
        return

    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            :root {
                --color-brand: #2CC3F6;
                --color-brand-hover: #22ACE0;
                --color-secondary: #7B8AA0;
                --color-bg-app: #0D1B2A;
                --color-bg-hero-left: #0D1B2A;
                --color-bg-hero-right: #162A3A;
                --color-bg-sidebar: #0A1725;
                --color-bg-card: #F5F7FB;
                --color-bg-white: #FFFFFF;
                --color-border-card: #E3E8F2;
                --color-line-muted: #D8DEE9;
                --color-text-strong: #1B2A41;
                --color-text-body: #2A3B52;
                --color-text-muted: #7B8AA0;
                --color-text-inverse: #FFFFFF;
                --color-positive: #2CC3F6;
                --color-warning: #F85F73;
                --color-success: #3CCB7C;
                --color-info: #5C7CFA;
                --radius-card: 12px;
                --radius-input: 8px;
                --radius-badge: 6px;
                --shadow-card: 0 4px 12px rgba(10, 24, 38, 0.15);
                --shadow-hover: 0 6px 18px rgba(10, 24, 38, 0.20);
                --space-xxs: 4px;
                --space-xs: 8px;
                --space-sm: 12px;
                --space-md: 16px;
                --space-lg: 24px;
                --space-xl: 32px;
                --font-sans: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial;
                --fs-hero: 28px; --lh-hero: 36px; --fw-hero: 700;
                --fs-section: 20px; --lh-section: 28px; --fw-section: 600;
                --fs-body: 14px; --lh-body: 22px;
                --fs-label: 12px; --lh-label: 18px; --ls-label: 0.02em;
                --fs-value: 24px; --lh-value: 32px; --fw-value: 700;
                --icon-default: #7B8AA0;
                --icon-active: #2CC3F6;
            }

            body,
            .stApp {
                font-family: var(--font-sans);
                background-color: var(--color-bg-app);
                color: var(--color-text-body);
            }

            .stApp {
                padding: 0;
            }

            .cl-dashboard-wrapper {
                width: 100%;
                padding: var(--space-xl) 0;
                background: linear-gradient(90deg, var(--color-bg-hero-left) 0%, var(--color-bg-hero-left) 45%, var(--color-bg-hero-right) 100%);
            }

            .cl-app-shell {
                margin: 0 auto;
                max-width: 1400px;
                display: flex;
                gap: var(--space-xl);
                padding: 0 var(--space-lg);
            }

            .cl-sidebar {
                width: 240px;
                background: var(--color-bg-sidebar);
                border-radius: var(--radius-card);
                padding: var(--space-lg) calc(var(--space-md));
                flex-shrink: 0;
                display: flex;
                flex-direction: column;
                gap: var(--space-lg);
                min-height: 100%;
                box-shadow: var(--shadow-card);
            }

            .cl-brand-block {
                display: flex;
                align-items: center;
                gap: var(--space-sm);
                color: var(--color-brand);
                font-weight: 700;
                font-size: 18px;
                letter-spacing: 0.01em;
            }

            .cl-nav-section {
                display: flex;
                flex-direction: column;
                gap: var(--space-xs);
            }

            .cl-nav-item {
                width: 100%;
                display: flex;
                align-items: center;
                gap: var(--space-sm);
                padding: var(--space-sm) calc(var(--space-sm)) var(--space-sm) calc(var(--space-md));
                color: #E6EDF5;
                background: transparent;
                border: none;
                border-left: 4px solid transparent;
                border-radius: 8px;
                font-size: 14px;
                line-height: 20px;
                text-align: left;
                transition: background 150ms ease-out, color 150ms ease-out, border-color 150ms ease-out, transform 150ms ease-out;
                cursor: pointer;
            }

            .cl-nav-item svg {
                stroke: var(--icon-default);
            }

            .cl-nav-item:hover {
                background: rgba(255, 255, 255, 0.06);
                color: var(--color-text-inverse);
            }

            .cl-nav-item:focus-visible {
                outline: 2px solid var(--color-brand);
                outline-offset: 2px;
            }

            .cl-nav-item.is-active {
                background: rgba(44, 195, 246, 0.08);
                border-left-color: var(--color-brand);
                color: var(--color-text-inverse);
            }

            .cl-nav-item.is-active svg {
                stroke: var(--icon-active);
            }

            .cl-main-area {
                flex: 1;
                max-width: 1200px;
                width: 100%;
                margin: 0 auto;
                display: flex;
                flex-direction: column;
                gap: var(--space-xl);
                padding-bottom: var(--space-xl);
            }

            .cl-hero {
                position: relative;
                background: linear-gradient(90deg, var(--color-bg-hero-left), var(--color-bg-hero-right));
                border-radius: var(--radius-card);
                padding: var(--space-lg) var(--space-xl);
                min-height: 140px;
                overflow: hidden;
                color: var(--color-text-inverse);
                box-shadow: var(--shadow-card);
            }

            .cl-hero-brand {
                display: inline-flex;
                align-items: center;
                gap: var(--space-xs);
                color: var(--color-brand);
                font-size: 13px;
                letter-spacing: 0.04em;
                text-transform: uppercase;
            }

            .cl-hero-title {
                font-size: var(--fs-hero);
                line-height: var(--lh-hero);
                font-weight: var(--fw-hero);
                margin: var(--space-xs) 0 var(--space-xxs);
                color: var(--color-text-inverse);
            }

            .cl-hero-subtitle {
                font-size: var(--fs-body);
                line-height: var(--lh-body);
                color: var(--color-text-muted);
                max-width: 460px;
            }

            .cl-hero-watermark {
                position: absolute;
                right: var(--space-md);
                bottom: -10px;
                opacity: 0.1;
            }

            .cl-section {
                background: var(--color-bg-card);
                border-radius: var(--radius-card);
                padding: var(--space-lg);
                box-shadow: var(--shadow-card);
                border: 1px solid var(--color-border-card);
            }

            .cl-section h2 {
                font-size: var(--fs-section);
                line-height: var(--lh-section);
                font-weight: var(--fw-section);
                color: var(--color-text-strong);
                margin: 0 0 var(--space-md);
            }

            .cl-metric-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: var(--space-lg);
            }

            .cl-metric-card {
                background: var(--color-bg-white);
                border: 1px solid var(--color-border-card);
                border-radius: var(--radius-card);
                padding: var(--space-md);
                box-shadow: var(--shadow-card);
                transition: transform 150ms ease-out, box-shadow 150ms ease-out;
            }

            .cl-metric-card:hover {
                box-shadow: var(--shadow-hover);
                transform: translateY(-1px);
            }

            .cl-metric-card:focus-visible {
                outline: 2px solid var(--color-brand);
                outline-offset: 2px;
            }

            .cl-metric-label {
                font-size: var(--fs-label);
                line-height: var(--lh-label);
                color: var(--color-text-muted);
                text-transform: uppercase;
                letter-spacing: var(--ls-label);
                margin-bottom: var(--space-xs);
            }

            .cl-metric-value {
                font-size: var(--fs-value);
                line-height: var(--lh-value);
                font-weight: var(--fw-value);
                color: var(--color-text-strong);
                text-align: right;
            }

            .cl-metric-card.is-positive .cl-metric-value {
                color: var(--color-positive);
            }

            .cl-metric-card.is-warning .cl-metric-value {
                color: var(--color-warning);
            }

            .cl-chart-panel {
                margin-top: var(--space-lg);
                background: var(--color-bg-white);
                border: 1px solid var(--color-border-card);
                border-radius: var(--radius-card);
                padding: var(--space-lg);
                box-shadow: var(--shadow-card);
                min-height: 360px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .cl-chart-panel .cl-chart-placeholder {
                width: 100%;
                height: 100%;
                border: 2px dashed var(--color-line-muted);
                border-radius: calc(var(--radius-card) - var(--space-sm));
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--color-text-muted);
                font-weight: 500;
                text-align: center;
            }

            .cl-chart-panel .cl-chart-placeholder:focus-visible {
                outline: 2px solid var(--color-brand);
                outline-offset: 6px;
            }

            @media (max-width: 1199px) {
                .cl-app-shell {
                    padding: 0 var(--space-md);
                    gap: var(--space-lg);
                }

                .cl-sidebar {
                    width: 220px;
                }

                .cl-metric-grid {
                    gap: var(--space-md);
                    grid-template-columns: repeat(2, minmax(200px, 1fr));
                }
            }

            @media (max-width: 767px) {
                .cl-app-shell {
                    padding: 0 var(--space-md);
                }

                .cl-sidebar {
                    width: 64px;
                    padding: var(--space-md) var(--space-sm);
                    align-items: center;
                    gap: var(--space-md);
                }

                .cl-brand-block {
                    display: none;
                }

                .cl-nav-section {
                    gap: var(--space-sm);
                }

                .cl-nav-item {
                    border-left: none;
                    border-radius: var(--radius-card);
                    padding: var(--space-md);
                    justify-content: center;
                }

                .cl-nav-label {
                    display: none;
                }

                .cl-hero {
                    min-height: 110px;
                    padding: var(--space-lg);
                }

                .cl-hero-title {
                    font-size: 24px;
                    line-height: 32px;
                }

                .cl-hero-subtitle {
                    font-size: 13px;
                }

                .cl-metric-grid {
                    grid-template-columns: 1fr;
                    gap: var(--space-sm);
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.session_state[_DASHBOARD_STYLE_KEY] = True


def _render_sidebar_nav(active_item: str) -> str:
    """Build the navigation rail markup."""
    nav_items = [
        {"label": "Dashboard", "icon": "layout-grid"},
        {"label": "Resume Analysis", "icon": "file-text"},
        {"label": "Market Match", "icon": "target"},
        {"label": "Settings", "icon": "settings"},
    ]

    buttons = []
    for item in nav_items:
        is_active = item["label"].lower() == active_item.lower()
        state_class = " is-active" if is_active else ""
        aria_current = "page" if is_active else "false"
        icon_color = "var(--cl-icon-active)" if is_active else None
        icon_stroke = icon_color or "var(--icon-default)"
        buttons.append(
            f"""
            <button type="button" class="cl-nav-item{state_class}" aria-label="{item['label']}"
                    aria-current="{aria_current}" title="{item['label']}">
                {_icon_svg(item['icon'], stroke=icon_stroke)}
                <span class="cl-nav-label">{item['label']}</span>
            </button>
            """
        )

    return f"""
    <aside class="cl-sidebar" role="navigation" aria-label="Primary navigation">
        <div class="cl-brand-block">
            {_icon_svg("eye", stroke="var(--color-brand)")}
            <span>CareerLens</span>
        </div>
        <div class="cl-nav-section">
            {''.join(buttons)}
        </div>
    </aside>
    """


def _render_hero_header(user_name: str, subtitle: str) -> str:
    """Return the hero header layout."""
    greeting = f"Welcome back, {user_name or 'Alex'}."
    return f"""
    <header class="cl-hero" role="banner">
        <div class="cl-hero-content">
            <div class="cl-hero-brand">
                {_icon_svg("eye", stroke="var(--color-brand)", size=18)}
                <span>CareerLens</span>
            </div>
            <h1 class="cl-hero-title">{greeting}</h1>
            <p class="cl-hero-subtitle">{subtitle}</p>
        </div>
        <div class="cl-hero-watermark" aria-hidden="true">
            {_icon_svg("eye", stroke="var(--color-brand)", size=220, opacity=0.1)}
        </div>
    </header>
    """


def _render_metric_card(label: str, value: str, variant: str = "default") -> str:
    """Return HTML for a metric card with variant coloring."""
    variant_class = "" if variant == "default" else f" is-{variant}"
    return f"""
    <article class="cl-metric-card{variant_class}" tabindex="0" aria-label="{label} {value}">
        <p class="cl-metric-label">{label}</p>
        <p class="cl-metric-value">{value}</p>
    </article>
    """


def _render_chart_panel() -> str:
    """Placeholder chart area with dashed boundary."""
    return """
    <div class="cl-chart-panel">
        <div class="cl-chart-placeholder" tabindex="0">
            <span>Chart Area / Data Visualization</span>
        </div>
    </div>
    """


def _render_section(title: str, content_html: str) -> str:
    """Generic section wrapper."""
    return f"""
    <section class="cl-section" aria-label="{title}">
        <h2>{title}</h2>
        {content_html}
    </section>
    """


def display_skill_matching_matrix(user_profile):
    """Display skill matching calculation matrix to help users understand ranking"""
    st.markdown("---")
    st.markdown("### 📊 How Job Ranking Works")
    
    user_skills = user_profile.get('skills', '') if user_profile else ''
    
    if not user_skills:
        st.info("💡 **Skill-Based Ranking**: Jobs are ranked purely by how many required skills you match. Upload your profile to see your skills analyzed.")
        return
    
    user_skills_list = [s.strip() for s in str(user_skills).split(',') if s.strip()]
    
    if not user_skills_list:
        st.info("💡 **Skill-Based Ranking**: Jobs are ranked purely by how many required skills you match.")
        return
    
    st.markdown("#### Your Skills")
    skills_display = ", ".join(user_skills_list[:10])
    if len(user_skills_list) > 10:
        skills_display += f" (+{len(user_skills_list) - 10} more)"
    st.markdown(f"**{len(user_skills_list)} skills identified:** {skills_display}")
    
    st.markdown("---")
    
    st.markdown("#### Ranking Formula")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **Skill Match Score =**
        
        ```
        Matched Skills
        ──────────────
        Required Skills
        ```
        
        **Example:**
        - Job requires: Python, SQL, React, Docker
        - You have: Python, SQL, React
        - **Score: 3/4 = 75%**
        """)
    
    with col2:
        st.markdown("""
        **Ranking Logic:**
        
        1. ✅ Jobs are fetched from job boards
        2. 🔍 Your skills are matched against each job's required skills
        3. 📊 Jobs are sorted by skill match score (highest first)
        4. 🎯 Top matches appear at the top of the list
        
        **Why this approach?**
        - Transparent: You see exactly why jobs rank high
        - Objective: Based on concrete skill requirements
        - Actionable: Shows which skills to learn
        """)
    
    st.markdown("---")
    
    st.markdown("#### Matching Method")
    
    method_col1, method_col2 = st.columns(2)
    
    with method_col1:
        st.markdown("""
        **Semantic Matching** (Primary)
        - Uses AI embeddings to understand skill similarity
        - Recognizes related skills (e.g., "JavaScript" ≈ "JS")
        - Handles variations and synonyms
        - Threshold: 70% similarity required
        """)
    
    with method_col2:
        st.markdown("""
        **String Matching** (Fallback)
        - Used when semantic matching unavailable
        - Direct text comparison
        - Case-insensitive matching
        - Handles partial matches
        """)
    
    if 'matched_jobs' in st.session_state and st.session_state.matched_jobs:
        st.markdown("---")
        st.markdown("#### Example: Top Match Breakdown")
        
        top_match = st.session_state.matched_jobs[0] if st.session_state.matched_jobs else None
        if top_match:
            job = top_match.get('job', {})
            job_skills = job.get('skills', [])
            skill_score = top_match.get('skill_match_score', 0.0)
            matched_count = int(skill_score * len(job_skills)) if job_skills else 0
            
            if job_skills:
                st.markdown(f"**{job.get('title', 'Job')} at {job.get('company', 'Company')}**")
                st.markdown(f"**Match Score: {int(skill_score * 100)}%** ({matched_count}/{len(job_skills)} skills matched)")
                
                job_skills_lower = [s.lower().strip() for s in job_skills if isinstance(s, str)]
                user_skills_lower = [s.lower().strip() for s in user_skills_list]
                
                matched_skills_list = []
                missing_skills_list = []
                
                for js in job_skills_lower:
                    matched = False
                    for us in user_skills_lower:
                        if js in us or us in js:
                            matched_skills_list.append(js)
                            matched = True
                            break
                    if not matched:
                        missing_skills_list.append(js)
                
                if matched_skills_list:
                    st.success(f"✅ **Matched Skills:** {', '.join(matched_skills_list[:5])}")
                if missing_skills_list:
                    st.warning(f"⚠️ **Missing Skills:** {', '.join(missing_skills_list[:5])}")


def display_market_positioning_profile(matched_jobs, user_profile):
    """Display Dashboard with 3 key metric cards: Match Score, Est. Salary, Skill Gaps"""
    if not matched_jobs:
        return

    _inject_dashboard_styles()

    avg_match_score = sum(r.get('combined_match_score', 0) for r in matched_jobs) / len(matched_jobs)
    match_score_pct = int(avg_match_score * 100)

    salary_min, salary_max = calculate_salary_band(matched_jobs)
    avg_salary = (salary_min + salary_max) // 2

    user_skills = user_profile.get('skills', '')
    all_job_skills = []
    for result in matched_jobs:
        all_job_skills.extend(result['job'].get('skills', []))

    user_skills_list = [s.lower().strip() for s in str(user_skills).split(',') if s.strip()]
    skill_gaps = set()
    for job_skill in all_job_skills:
        if isinstance(job_skill, str):
            job_skill_lower = job_skill.lower().strip()
            if job_skill_lower and not any(us in job_skill_lower or job_skill_lower in us for us in user_skills_list):
                skill_gaps.add(job_skill_lower)

    num_skill_gaps = len(skill_gaps)

    metric_cards = [
        _render_metric_card("MATCH SCORE", f"{match_score_pct}%", variant="positive"),
        _render_metric_card("EST SALARY", f"HK${max(avg_salary // 1000, 0)}k"),
        _render_metric_card("SKILL GAPS", str(num_skill_gaps), variant="warning"),
    ]

    metrics_html = f'<div class="cl-metric-grid">{"".join(metric_cards)}</div>'
    chart_html = _render_chart_panel()
    section_html = _render_section("Recent Activity", metrics_html + chart_html)

    hero_name = user_profile.get('name') or user_profile.get('first_name') or "Alex"
    hero_subtitle = "Your market value has increased by 5% since last month."

    layout_html = f"""
    <div class="cl-dashboard-wrapper">
        <div class="cl-app-shell">
            {_render_sidebar_nav("Dashboard")}
            <main class="cl-main-area" role="main" aria-live="polite">
                {_render_hero_header(hero_name, hero_subtitle)}
                {section_html}
            </main>
        </div>
    </div>
    """

    st.markdown(layout_html, unsafe_allow_html=True)


def display_refine_results_section(matched_jobs, user_profile):
    """Display Refine Results section with filters"""
    st.markdown("---")
    with st.expander("🔧 Refine Results", expanded=False):
        st.markdown("### Adjust Search Criteria")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_domains = st.session_state.get('target_domains', [])
            target_domains = st.multiselect(
                "Target Domains (HK Focus)",
                options=["FinTech", "ESG & Sustainability", "Data Analytics", "Digital Transformation", 
                        "Investment Banking", "Consulting", "Technology", "Healthcare", "Education"],
                default=current_domains,
                key="refine_domains"
            )
        
        with col2:
            current_salary = st.session_state.get('salary_expectation', 0)
            salary_expectation = st.slider(
                "Min. Monthly Salary (HKD)",
                min_value=0,
                max_value=150000,
                value=current_salary,
                step=5000,
                help="Set to 0 to disable salary filtering",
                key="refine_salary"
            )
        
        force_refresh = st.checkbox(
            "Force new API fetch",
            value=False,
            help="Bypass cached results (only if results seem stale).",
            key="force_refresh_jobs_toggle"
        )
        
        if st.button("🔄 Apply Filters & Refresh", type="primary", use_container_width=True):
            st.session_state.target_domains = target_domains
            st.session_state.salary_expectation = salary_expectation
            
            search_query = " ".join(target_domains) if target_domains else "Hong Kong jobs"
            scraper = get_job_scraper()
            
            if scraper is None:
                st.error("⚠️ Job scraper not configured.")
                return
            
            with st.spinner("🔄 Refreshing results from Indeed..."):
                jobs = fetch_jobs_with_cache(
                    scraper,
                    search_query,
                    location="Hong Kong",
                    max_rows=25,
                    job_type="fulltime",
                    country="hk",
                    force_refresh=force_refresh
                )
                
                if not jobs:
                    st.error("❌ No jobs found from Indeed.")
                    return
                
                total_fetched = len(jobs)
                
                if target_domains:
                    jobs = filter_jobs_by_domains(jobs, target_domains)
                
                if salary_expectation > 0:
                    jobs = filter_jobs_by_salary(jobs, salary_expectation)
                
                if not jobs:
                    st.warning(f"⚠️ No jobs match your filters. Found {total_fetched} jobs but none passed your criteria.")
                    return
                
                embedding_gen = get_embedding_generator()
                desired_matches = min(15, len(jobs))
                jobs_to_index_limit = _determine_index_limit(len(jobs), desired_matches)
                top_match_count = min(desired_matches, jobs_to_index_limit)
                search_engine = SemanticJobSearch(embedding_gen)
                search_engine.index_jobs(jobs, max_jobs_to_index=jobs_to_index_limit)
                
                resume_embedding = st.session_state.get('resume_embedding')
                if not resume_embedding and st.session_state.resume_text:
                    resume_embedding = generate_and_store_resume_embedding(
                        st.session_state.resume_text,
                        st.session_state.user_profile if st.session_state.user_profile else None
                    )
                
                resume_query = None
                if not resume_embedding:
                    if st.session_state.resume_text:
                        resume_query = st.session_state.resume_text
                        if st.session_state.user_profile.get('summary'):
                            profile_data = f"{st.session_state.user_profile.get('summary', '')} {st.session_state.user_profile.get('experience', '')} {st.session_state.user_profile.get('skills', '')}"
                            resume_query = f"{resume_query} {profile_data}"
                    else:
                        resume_query = f"{st.session_state.user_profile.get('summary', '')} {st.session_state.user_profile.get('experience', '')} {st.session_state.user_profile.get('skills', '')} {st.session_state.user_profile.get('education', '')}"
                
                results = search_engine.search(query=resume_query, top_k=top_match_count, resume_embedding=resume_embedding)
                
                user_skills = st.session_state.user_profile.get('skills', '')
                for result in results:
                    job_skills = result['job'].get('skills', [])
                    skill_score, missing_skills = search_engine.calculate_skill_match(user_skills, job_skills)
                    result['skill_match_score'] = skill_score
                    result['missing_skills'] = missing_skills
                    
                    semantic_score = result.get('similarity_score', 0.0)
                    combined_score = (semantic_score * 0.6) + (skill_score * 0.4)
                    result['combined_match_score'] = combined_score
                
                results.sort(key=lambda x: x.get('combined_match_score', 0.0), reverse=True)
                
                st.session_state.matched_jobs = results
                st.session_state.dashboard_ready = True
                
                gc.collect()
                
                st.rerun()


def display_ranked_matches_table(matched_jobs, user_profile):
    """Display Smart Ranked Matches Table with interactive dataframe"""
    if not matched_jobs:
        return
    
    st.markdown("---")
    st.markdown("### Top AI-Ranked Opportunities")
    st.caption("💡 **Tip:** Click any row to expand and see full job description, match analysis, and application copilot")
    
    user_skills = user_profile.get('skills', '')
    
    def calc_skill_match(user_skills_str, job_skills_list):
        if not user_skills_str or not job_skills_list:
            return 0.0, []
        user_skills_lower = [s.lower().strip() for s in str(user_skills_str).split(',') if s.strip()]
        job_skills_lower = [s.lower().strip() for s in job_skills_list if isinstance(s, str) and s.strip()]
        if not user_skills_lower or not job_skills_lower:
            return 0.0, []
        matched_skills = []
        for job_skill in job_skills_lower:
            for user_skill in user_skills_lower:
                if job_skill in user_skill or user_skill in job_skill:
                    matched_skills.append(job_skill)
                    break
        match_score = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0.0
        missing_skills = [s for s in job_skills_lower if s not in matched_skills]
        return min(match_score, 1.0), missing_skills[:5]
    
    for result in matched_jobs:
        if 'skill_match_score' not in result:
            job_skills = result['job'].get('skills', [])
            skill_score, missing_skills = calc_skill_match(user_skills, job_skills)
            result['skill_match_score'] = skill_score
            result['missing_skills'] = missing_skills
        
        if 'combined_match_score' not in result:
            semantic_score = result.get('similarity_score', 0.0)
            skill_score = result.get('skill_match_score', 0.0)
            combined_score = (semantic_score * 0.6) + (skill_score * 0.4)
            result['combined_match_score'] = combined_score
    
    matched_jobs.sort(key=lambda x: x.get('combined_match_score', 0.0), reverse=True)
    
    table_data = []
    for i, result in enumerate(matched_jobs):
        job = result['job']
        semantic_score = result.get('similarity_score', 0.0)
        skill_score = result.get('skill_match_score', 0.0)
        match_score = result.get('combined_match_score', (semantic_score * 0.6) + (skill_score * 0.4))
        
        job_skills = job.get('skills', [])
        matching_skills = []
        user_skills_list = [s.lower().strip() for s in str(user_skills).split(',') if s.strip()]
        for js in job_skills[:6]:
            if isinstance(js, str):
                js_lower = js.lower().strip()
                if any(us in js_lower or js_lower in us for us in user_skills_list):
                    matching_skills.append(js)
                    if len(matching_skills) >= 4:
                        break
        
        missing_critical = result.get('missing_skills', [])
        missing_critical_skill = missing_critical[0] if missing_critical else "None"
        
        table_data.append({
            'Rank': i + 1,
            'Match Score': int(match_score * 100),
            'Job Title': job['title'],
            'Company': job['company'],
            'Location': job['location'],
            'Key Matching Skills': matching_skills[:4] if matching_skills else [],
            'Missing Critical Skill': missing_critical_skill,
            '_index': i
        })
    
    df = pd.DataFrame(table_data)
    
    column_config = {
        'Rank': st.column_config.NumberColumn(
            'Rank',
            help='Job ranking position (fixed, does not change when sorting)',
            width='small',
            format='%d'
        ),
        'Match Score': st.column_config.ProgressColumn(
            'Match Score',
            help='Combined match score: 60% semantic similarity + 40% skill overlap (jobs ranked by this)',
            min_value=0,
            max_value=100,
            format='%d%%'
        ),
        'Job Title': st.column_config.TextColumn(
            'Job Title',
            width='medium',
            help='Click to select and view full details'
        ),
        'Company': st.column_config.TextColumn(
            'Company',
            width='medium'
        ),
        'Location': st.column_config.TextColumn(
            'Location',
            width='small'
        ),
        'Key Matching Skills': st.column_config.ListColumn(
            'Key Matching Skills',
            help='Top skills you have that match this role'
        ),
        'Missing Critical Skill': st.column_config.TextColumn(
            'Missing Critical Skill',
            help='Most important skill gap for this role',
            width='medium'
        ),
        '_index': st.column_config.NumberColumn(
            '_index',
            width='small',
            help=None
        )
    }
    
    column_order = ['Rank', 'Match Score', 'Job Title', 'Company', 'Location', 'Key Matching Skills', 'Missing Critical Skill']
    
    df_display = df[column_order].copy()
    
    selected_rows = st.dataframe(
        df_display,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    if selected_rows.selection.rows:
        selected_idx = df.iloc[selected_rows.selection.rows[0]]['_index']
        st.session_state.selected_job_index = int(selected_idx)
    else:
        st.session_state.selected_job_index = None


def display_match_breakdown(matched_jobs, user_profile):
    """Display Match Breakdown & Application Copilot in expander"""
    if st.session_state.selected_job_index is None:
        return
    
    selected_result = matched_jobs[st.session_state.selected_job_index]
    job = selected_result['job']
    semantic_score = selected_result.get('similarity_score', 0.0)
    skill_score = selected_result.get('skill_match_score', 0.0)
    missing_skills = selected_result.get('missing_skills', [])
    
    user_skills = user_profile.get('skills', '')
    job_skills = job.get('skills', [])
    user_skills_list = [s.lower().strip() for s in str(user_skills).split(',') if s.strip()]
    job_skills_list = [s.lower().strip() for s in job_skills if isinstance(s, str) and s.strip()]
    
    matched_skills_count = 0
    for js in job_skills_list:
        if any(us in js or js in us for us in user_skills_list):
            matched_skills_count += 1
    
    total_required = len(job_skills_list) if job_skills_list else 1
    skill_overlap_pct = (matched_skills_count / total_required * 100) if total_required > 0 else 0
    
    text_gen = get_text_generator()
    if text_gen is None:
        recruiter_note = "AI analysis unavailable. Please configure Azure OpenAI credentials."
    else:
        recruiter_note = text_gen.generate_recruiter_note(job, user_profile, semantic_score, skill_score)
    
    rank_position = st.session_state.selected_job_index + 1 if st.session_state.selected_job_index is not None else 0
    
    expander_title = f"📋 Rank #{rank_position}: {job['title']} at {job['company']}"
    
    with st.expander(expander_title, expanded=True):
        st.markdown("#### 📝 Full Job Description")
        description_text = job.get('description', 'No description available.')
        if len(description_text) > 10000:
            st.info(f"📄 Full description ({len(description_text):,} characters)")
            st.text_area(
                "Job Description",
                value=description_text,
                height=400,
                key=f"job_desc_{st.session_state.selected_job_index}",
                label_visibility="collapsed"
            )
        else:
            st.markdown(description_text)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🎯 Match Analysis & Why This is a Fit")
            
            st.markdown(f"""
            **Match Score Breakdown:**
            - **🎯 Skill Match Score (Ranking Factor):** {skill_score:.0%} ({matched_skills_count}/{total_required} skills matched)
              - This is the primary ranking factor. Jobs are sorted by this score.
            - **📊 Semantic Similarity Score:** {semantic_score:.0%}
              - Measures how well your experience contextually aligns with role requirements.
            - **⚖️ Combined Match Score:** {(semantic_score * 0.6 + skill_score * 0.4):.0%}
              - Weighted combination: 60% semantic + 40% skill overlap
            """)
            
            if matched_skills_count > 0:
                matched_skills_display = []
                for js in job_skills_list:
                    if any(us in js or js in us for us in user_skills_list):
                        matched_skills_display.append(js)
                        if len(matched_skills_display) >= 10:
                            break
                if matched_skills_display:
                    st.success(f"✅ **Matched Skills:** {', '.join(matched_skills_display[:10])}")
            
            if missing_skills:
                st.warning(f"⚠️ **Missing Skills:** {', '.join(missing_skills[:5])}")
            
            st.markdown("---")
            st.info(f"**🤖 AI Recruiter Analysis:**\n\n{recruiter_note}")
        
        with col2:
            st.markdown("#### Application Copilot")
            
            if missing_skills:
                top_missing = missing_skills[0]
                cert_keywords = ['certification', 'certified', 'accreditation', 'license', 'pmp', 'scrum', 'hkicpa', 'cpa', 'cfa', 'cpa', 'aws', 'azure', 'gcp']
                is_cert = any(kw in top_missing.lower() for kw in cert_keywords)
                
                if is_cert:
                    st.warning(f"⚠️ **Crucial Gap:** This job highly values {top_missing}. Consider starting this certification.")
                else:
                    st.warning(f"⚠️ **Skill Gap:** Consider developing expertise in {top_missing}.")
            
            if st.button("✨ Tailor Resume for this Job", use_container_width=True, type="primary", key="tailor_resume_button"):
                st.session_state.selected_job = job
                st.session_state.show_resume_generator = True
                st.rerun()
            
            st.caption("Generates a citation-locked, AI-optimized CV emphasizing your matching skills.")
            
            job_url = job.get('url', '#')
            if job_url and job_url != '#':
                st.markdown("---")
                st.link_button("🚀 Apply to Job", job_url, use_container_width=True, type="secondary")
