"""CareerLens hero + dashboard shell renderer."""

from __future__ import annotations

from typing import Optional

import streamlit as st

from .dashboard import (
    _inject_dashboard_styles,
    _render_chart_panel,
    _render_hero_header,
    _render_metric_card,
    _render_section,
    _render_sidebar_nav,
)

_PLACEHOLDER_METRICS = [
    ("MATCH SCORE", "92%", "positive"),
    ("EST SALARY", "HK$55k", "default"),
    ("SKILL GAPS", "3", "warning"),
]

_HERO_STYLE_KEY = "_careerlens_hero_banner_refresh_styles"

_HERO_BANNER_STYLES = """
<style>
    .cl-hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr);
        gap: var(--space-xl);
        align-items: stretch;
    }

    .cl-hero-spotlight {
        display: flex;
        flex-direction: column;
        gap: var(--space-lg);
    }

    .cl-hero-spotlight .cl-hero {
        margin: 0;
    }

    .cl-hero-cta-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: var(--space-md);
    }

    .cl-hero-cta {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: var(--radius-card);
        padding: var(--space-lg);
        color: var(--color-text-inverse);
        min-height: 170px;
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
    }

    .cl-hero-cta h3 {
        margin: 0;
        font-size: 18px;
        color: var(--color-text-inverse);
    }

    .cl-hero-cta p {
        margin: 0;
        color: rgba(255, 255, 255, 0.8);
        font-size: 14px;
        line-height: 20px;
    }

    .cl-hero-cta button {
        margin-top: auto;
        border-radius: var(--radius-input);
        border: none;
        padding: var(--space-sm) var(--space-md);
        background: var(--color-brand);
        color: var(--color-text-inverse);
        font-weight: 600;
        cursor: pointer;
        transition: background 150ms ease-out, transform 150ms ease-out;
    }

    .cl-hero-cta button:hover {
        background: var(--color-brand-hover);
        transform: translateY(-1px);
    }

    .cl-hero-progress {
        background: var(--color-bg-card);
        border-radius: var(--radius-card);
        padding: var(--space-lg);
        box-shadow: var(--shadow-card);
        border: 1px solid var(--color-border-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .cl-panel-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: var(--color-text-muted);
        font-size: 12px;
        margin: 0;
    }

    .cl-panel-subcopy {
        margin: 0;
        color: var(--color-text-body);
        font-size: 14px;
        line-height: 20px;
    }

    .cl-checklist {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: var(--space-sm);
    }

    .cl-check-item {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: var(--space-sm);
        align-items: start;
    }

    .cl-check-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-top: var(--space-xxs);
        background: var(--color-warning);
    }

    .cl-check-indicator.is-complete {
        background: var(--color-success);
    }

    .cl-check-label {
        font-weight: 600;
        margin: 0;
        color: var(--color-text-strong);
        font-size: 14px;
    }

    .cl-check-desc {
        margin: 0;
        font-size: 13px;
        color: var(--color-text-muted);
    }

    .cl-check-status {
        font-size: 12px;
        font-weight: 600;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .cl-check-status.is-complete {
        color: var(--color-success);
    }

    .cl-progress-track {
        background: var(--color-line-muted);
        border-radius: 999px;
        height: 8px;
        position: relative;
        overflow: hidden;
    }

    .cl-progress-track span {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        border-radius: inherit;
        background: linear-gradient(90deg, var(--color-brand), var(--color-info));
    }

    .cl-secondary-btn {
        border: 1px solid var(--color-border-card);
        border-radius: var(--radius-input);
        padding: var(--space-sm) var(--space-md);
        background: var(--color-bg-white);
        font-weight: 600;
        color: var(--color-text-strong);
        cursor: pointer;
        transition: border 150ms ease-out, box-shadow 150ms ease-out;
    }

    .cl-secondary-btn:hover {
        border-color: var(--color-brand);
        box-shadow: var(--shadow-card);
    }

    .cl-panel-grid {
        display: grid;
        gap: var(--space-xl);
    }

    @media (min-width: 1100px) {
        .cl-panel-grid {
            grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr) minmax(0, 1fr);
        }
    }

    .cl-panel {
        background: var(--color-bg-card);
        border-radius: var(--radius-card);
        padding: var(--space-xl) var(--space-lg);
        box-shadow: var(--shadow-card);
        border: 1px solid var(--color-border-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .cl-drop-zone {
        border: 2px dashed var(--color-line-muted);
        border-radius: var(--radius-card);
        padding: var(--space-lg);
        text-align: center;
        background: var(--color-bg-white);
        display: flex;
        flex-direction: column;
        gap: var(--space-sm);
    }

    .cl-panel-divider {
        height: 1px;
        background: var(--color-border-card);
        margin: var(--space-sm) 0;
    }

    .cl-onboarding-steps {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .cl-panel h4 {
        margin: 0;
        color: var(--color-text-strong);
    }

    .cl-drop-zone button {
        align-self: center;
        border: none;
        border-radius: var(--radius-input);
        padding: var(--space-sm) var(--space-lg);
        background: var(--color-brand);
        color: var(--color-text-inverse);
        font-weight: 600;
        cursor: pointer;
    }

    .cl-form-group {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .cl-form-group label {
        font-weight: 600;
        font-size: 14px;
        color: var(--color-text-strong);
    }

    .cl-select-display {
        border: 1px solid var(--color-border-card);
        border-radius: var(--radius-input);
        padding: var(--space-sm) var(--space-md);
        background: var(--color-bg-white);
        color: var(--color-text-muted);
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
    }

    .cl-select-display svg {
        stroke: var(--color-text-muted);
    }

    .cl-slider-row {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        font-size: 13px;
        color: var(--color-text-muted);
    }

    .cl-slider-track {
        flex: 1;
        height: 6px;
        border-radius: 999px;
        background: var(--color-line-muted);
        position: relative;
    }

    .cl-slider-track span {
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        border-radius: inherit;
        background: var(--color-brand);
    }

    .cl-primary-btn {
        border: none;
        border-radius: var(--radius-input);
        padding: var(--space-sm) var(--space-lg);
        background: var(--color-brand);
        color: var(--color-text-inverse);
        font-weight: 600;
        cursor: pointer;
        box-shadow: var(--shadow-card);
    }

    .cl-primary-btn:hover {
        background: var(--color-brand-hover);
    }

    .cl-interview-layout {
        display: grid;
        gap: var(--space-lg);
    }

    @media (min-width: 960px) {
        .cl-interview-layout {
            grid-template-columns: 280px 1fr;
        }
    }

    .cl-interview-nav {
        background: var(--color-bg-white);
        border-radius: var(--radius-card);
        border: 1px solid var(--color-border-card);
        padding: var(--space-lg);
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .cl-interview-nav button {
        border: 1px solid var(--color-border-card);
        border-radius: var(--radius-input);
        background: var(--color-bg-card);
        padding: var(--space-xs) var(--space-md);
        font-weight: 600;
        cursor: pointer;
    }

    .cl-interview-nav ul {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }

    .cl-interview-nav li {
        padding: var(--space-xs) 0;
        font-weight: 600;
        color: var(--color-text-body);
        border-bottom: 1px dashed var(--color-line-muted);
    }

    .cl-interview-body {
        background: var(--color-bg-white);
        border-radius: var(--radius-card);
        border: 1px solid var(--color-border-card);
        padding: var(--space-xl);
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .cl-interview-badges {
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-lg);
    }

    .cl-badge {
        border-radius: var(--radius-badge);
        padding: var(--space-xxs) var(--space-sm);
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        background: var(--color-line-muted);
        color: var(--color-text-strong);
    }

    .cl-badge.is-success {
        background: rgba(60, 203, 124, 0.16);
        color: var(--color-success);
    }

    .cl-select-pill {
        border: 1px solid var(--color-border-card);
        border-radius: var(--radius-input);
        padding: var(--space-sm) var(--space-md);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .cl-meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: var(--space-md);
        background: var(--color-bg-card);
        border-radius: var(--radius-card);
        border: 1px solid var(--color-border-card);
        padding: var(--space-md);
    }

    .cl-question-card {
        border: 1px solid var(--color-border-card);
        border-radius: var(--radius-card);
        padding: var(--space-lg);
        background: var(--color-bg-card);
        display: flex;
        flex-direction: column;
        gap: var(--space-sm);
    }

    .cl-question-card h4 {
        margin: 0;
        font-size: 16px;
        color: var(--color-text-strong);
    }

    .cl-question-card p {
        margin: 0;
        color: var(--color-text-body);
        line-height: 22px;
    }

    .cl-question-card textarea {
        width: 100%;
        min-height: 140px;
        border-radius: var(--radius-input);
        border: 1px solid var(--color-border-card);
        padding: var(--space-md);
        font-family: var(--font-sans);
        resize: vertical;
    }

    .cl-eval-banner {
        border-radius: var(--radius-card);
        padding: var(--space-sm) var(--space-md);
        background: rgba(248, 95, 115, 0.12);
        color: var(--color-warning);
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: var(--space-sm);
    }

    .cl-progress-meta {
        display: flex;
        justify-content: space-between;
        font-size: 13px;
        color: var(--color-text-muted);
    }

    .cl-activity-feed {
        display: flex;
        flex-direction: column;
        gap: var(--space-md);
    }

    .cl-activity-item {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: var(--space-md);
        position: relative;
        padding-left: var(--space-md);
    }

    .cl-activity-item::before {
        content: "";
        position: absolute;
        left: 0;
        top: var(--space-sm);
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--color-info);
    }

    .cl-activity-item.is-positive::before {
        background: var(--color-success);
    }

    .cl-activity-item.is-warning::before {
        background: var(--color-warning);
    }

    .cl-activity-time {
        margin: 0;
        font-size: 12px;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .cl-activity-title {
        margin: 0;
        font-weight: 600;
        color: var(--color-text-strong);
    }

    .cl-activity-desc {
        margin: 0;
        color: var(--color-text-body);
        font-size: 13px;
        line-height: 20px;
    }

    .cl-insight-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: var(--space-md);
    }

    .cl-insight-metrics .cl-metric-card {
        min-height: 120px;
    }

    .cl-insight-chart .cl-chart-panel {
        margin-top: 0;
        min-height: 220px;
    }

    @media (max-width: 1023px) {
        .cl-hero-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
"""


def _build_recent_activity_section() -> str:
    """Return the Recent Activity section with placeholder metrics + chart."""
    metric_cards = [
        _render_metric_card(label, value, variant)
        for label, value, variant in _PLACEHOLDER_METRICS
    ]
    metrics_html = f'<div class="cl-metric-grid">{"".join(metric_cards)}</div>'
    chart_html = _render_chart_panel()
    return _render_section("Recent Activity", metrics_html + chart_html)


def _inject_hero_banner_styles() -> None:
    """Inject additional layout styles for the refreshed hero experience."""
    if st.session_state.get(_HERO_STYLE_KEY):
        return

    st.markdown(_HERO_BANNER_STYLES, unsafe_allow_html=True)
    st.session_state[_HERO_STYLE_KEY] = True


def _build_hero_overview(user_name: str, subtitle: str) -> str:
    """Top-of-page hero spotlight plus quick call-to-actions."""
    cta_definitions = [
        {
            "label": "Next action",
            "title": "Upload latest CV",
            "copy": "Refresh AI insights with your most recent experience.",
            "button": "Upload CV",
        },
        {
            "label": "Practice",
            "title": "Schedule mock interview",
            "copy": "Simulate recruiter prompts and capture structured answers.",
            "button": "Open AI Interview",
        },
        {
            "label": "Insight",
            "title": "Review market value",
            "copy": "Compare HK salary benchmarks for your target domain.",
            "button": "View Insights",
        },
    ]
    cta_cards = "".join(
        f"""
        <div class="cl-hero-cta">
            <p class="cl-panel-eyebrow">{cta['label']}</p>
            <h3>{cta['title']}</h3>
            <p>{cta['copy']}</p>
            <button type="button">{cta['button']}</button>
        </div>
        """
        for cta in cta_definitions
    )

    checklist = [
        ("Resume upload", "CV_HK-market.pdf", True),
        ("Target domains", "UX/UI, Digital Transformation", True),
        ("Salary expectation", "HK$55k minimum", True),
        ("AI mock interview", "Draft answers pending review", False),
    ]
    checklist_items = "".join(
        f"""
        <li class="cl-check-item">
            <span class="cl-check-indicator{' is-complete' if complete else ''}" aria-hidden="true"></span>
            <div>
                <p class="cl-check-label">{title}</p>
                <p class="cl-check-desc">{desc}</p>
            </div>
            <span class="cl-check-status{' is-complete' if complete else ''}">
                {"done" if complete else "todo"}
            </span>
        </li>
        """
        for title, desc, complete in checklist
    )

    hero_header = _render_hero_header(user_name, subtitle)
    return f"""
    <section class="cl-hero-grid" aria-label="Welcome overview">
        <div class="cl-hero-spotlight">
            {hero_header}
            <div class="cl-hero-cta-row">
                {cta_cards}
            </div>
        </div>
        <aside class="cl-hero-progress" aria-label="Onboarding tracker">
            <p class="cl-panel-eyebrow">Activation steps</p>
            <h3>Finish setup to unlock tailored matches</h3>
            <p class="cl-panel-subcopy">
                We tailor recommendations once your profile, salary target, and mock interview are completed.
            </p>
            <ul class="cl-checklist">
                {checklist_items}
            </ul>
            <div class="cl-progress-meta">
                <span>3 / 4 completed</span>
                <span>Next: Mock interview</span>
            </div>
            <div class="cl-progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="4" aria-valuenow="3">
                <span style="width:75%;"></span>
            </div>
            <button type="button" class="cl-secondary-btn">View detailed profile</button>
        </aside>
    </section>
    """


def _build_onboarding_panel() -> str:
    """Left column replicating CV upload + search criteria from the legacy UI."""
    return """
    <article class="cl-panel cl-panel--onboarding" aria-labelledby="cl-onboarding-title">
        <div>
            <p class="cl-panel-eyebrow">1. Upload your CV to begin</p>
            <h3 id="cl-onboarding-title">Get activated in two minutes</h3>
        </div>
        <div class="cl-drop-zone" role="button" tabindex="0" aria-label="Drag and drop resume">
            <strong>Drag and drop file here</strong>
            <span>Limit 10MB per file • PDF, DOCX</span>
            <button type="button">Browse files</button>
        </div>
        <div class="cl-panel-divider"></div>
        <div class="cl-onboarding-steps">
            <p class="cl-panel-eyebrow">2. Set Search Criteria</p>
            <h4>Personalize your CareerLens search</h4>
            <div class="cl-form-group">
                <label for="cl-target-domains">Target Domains</label>
                <div class="cl-select-display" id="cl-target-domains" role="listbox" aria-label="Choose target domains">
                    <span>Choose options</span>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </div>
            </div>
            <div class="cl-form-group">
                <label for="cl-salary-slider">Min. Monthly Salary (HKD)</label>
                <div class="cl-slider-row" id="cl-salary-slider">
                    <span>0</span>
                    <div class="cl-slider-track">
                        <span style="width:35%;"></span>
                    </div>
                    <span>150k</span>
                </div>
                <p class="cl-panel-subcopy">Adjust the slider to filter out roles below your expectation.</p>
            </div>
        </div>
        <button type="button" class="cl-primary-btn">Analyze Profile &amp; Find Matches</button>
    </article>
    """


def _build_interview_nav_block() -> str:
    """Helper that produces the vertical navigation list for the mock interview UI."""
    nav_items = ["Job Seeker", "Job Match", "Recruiter", "Recruitment Match", "AI Interview"]
    nav_list = "".join(f"<li>{item}</li>" for item in nav_items)
    return f"""
    <div class="cl-interview-nav" aria-label="Interview navigation">
        <div>
            <p class="cl-panel-eyebrow">Database Debug</p>
            <button type="button">View all job seeker records</button>
            <p class="cl-panel-subcopy">Current Session ID: <strong>JS_F9FF4S4D</strong></p>
        </div>
        <div>
            <p class="cl-panel-eyebrow">Navigation</p>
            <ul>{nav_list}</ul>
        </div>
        <div>
            <p class="cl-panel-eyebrow">Select Function</p>
            <label><input type="radio" name="cl_interview_mode" checked /> Start Mock Interview</label>
            <label><input type="radio" name="cl_interview_mode" /> Interview Preparation Guide</label>
            <label><input type="radio" name="cl_interview_mode" /> Instructions</label>
        </div>
        <div>
            <p class="cl-panel-eyebrow">Usage Instructions</p>
            <ul>
                <li>Upload smart resume to unlock automatic matching.</li>
                <li>Explore job seeker profiles and verify data.</li>
                <li>Launch AI mock interviews to rehearse answers.</li>
            </ul>
        </div>
    </div>
    """


def _build_ai_mock_interview_panel() -> str:
    """Middle column mirroring the AI Mock Interview screen (pic2)."""
    nav_block = _build_interview_nav_block()
    return f"""
    <article class="cl-panel cl-panel--interview" aria-labelledby="cl-interview-title">
        <div class="cl-interview-layout">
            {nav_block}
            <div class="cl-interview-body">
                <div class="cl-interview-badges">
                    <div>
                        <p class="cl-panel-eyebrow">Available Positions</p>
                        <h3>2</h3>
                    </div>
                    <div>
                        <p class="cl-panel-eyebrow">Personal Profile</p>
                        <span class="cl-badge is-success">Complete</span>
                    </div>
                    <div>
                        <p class="cl-panel-eyebrow">Interview Progress</p>
                        <strong>1/2</strong>
                    </div>
                </div>
                <div>
                    <h3 id="cl-interview-title">AI Mock Interview</h3>
                    <p class="cl-panel-subcopy">
                        Select the position you want to interview for to start the mock interview.
                    </p>
                </div>
                <div class="cl-form-group">
                    <label for="cl-interview-select">Select Interview Position</label>
                    <div class="cl-select-pill" id="cl-interview-select">
                        <span>#1 UX/UI Designer — CreativeDigital Agency</span>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="6 9 12 15 18 9"></polyline>
                        </svg>
                    </div>
                </div>
                <div class="cl-meta-grid" role="list">
                    <div role="listitem">
                        <p class="cl-panel-eyebrow">Position</p>
                        <strong>UX/UI Designer</strong>
                    </div>
                    <div role="listitem">
                        <p class="cl-panel-eyebrow">Company</p>
                        <strong>CreativeDigital Agency</strong>
                    </div>
                    <div role="listitem">
                        <p class="cl-panel-eyebrow">Industry</p>
                        <strong>Technology</strong>
                    </div>
                    <div role="listitem">
                        <p class="cl-panel-eyebrow">Experience Requirement</p>
                        <strong>10+ years</strong>
                    </div>
                    <div role="listitem">
                        <p class="cl-panel-eyebrow">Skill Requirements</p>
                        <strong>Figma, Adobe Creative Suite, Research, Prototyping</strong>
                    </div>
                </div>
                <div class="cl-question-card">
                    <div>
                        <p class="cl-panel-eyebrow">Question 1/2</p>
                        <h4>Can you describe a specific project...</h4>
                        <p>Please walk us through how you conducted user research, the tools you used for wireframing and prototyping, and how you collaborated with cross-functional teams to ensure the final design met user needs and business goals.</p>
                    </div>
                    <label for="cl-answer">Your Answer</label>
                    <textarea id="cl-answer" placeholder="Type your response here">hello</textarea>
                    <div class="cl-eval-banner">
                        <span>Evaluation result parsing failed</span>
                        <button type="button" class="cl-primary-btn">Submit Answer</button>
                    </div>
                    <div class="cl-progress-meta">
                        <span>Progress: 1/2 questions</span>
                        <span>Powered by GPT-4, Pinecone, RapidAPI</span>
                    </div>
                    <div class="cl-progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="2" aria-valuenow="1">
                        <span style="width:50%;"></span>
                    </div>
                </div>
            </div>
        </div>
    </article>
    """


def _build_activity_panel() -> str:
    """Right column: metrics, chart placeholder, and activity stream."""
    metrics_html = "".join(
        _render_metric_card(label, value, variant) for label, value, variant in _PLACEHOLDER_METRICS
    )
    activity_log = [
        ("09:45", "Resume parsed successfully", "Extracted 12 quantified achievements from CV_HK-market.pdf.", "positive"),
        ("09:32", "Mock interview answer saved", "Draft answer recorded for Question 1 to revisit later.", "info"),
        ("09:20", "Skill gaps identified", "UI motion systems, Journey orchestration flagged as growth areas.", "warning"),
    ]
    activity_html = "".join(
        f"""
        <div class="cl-activity-item {'is-positive' if status == 'positive' else 'is-warning' if status == 'warning' else ''}">
            <div>
                <p class="cl-activity-time">{time}</p>
                <p class="cl-activity-title">{title}</p>
                <p class="cl-activity-desc">{desc}</p>
            </div>
        </div>
        """
        for time, title, desc, status in activity_log
    )

    return f"""
    <article class="cl-panel cl-panel--insights" aria-labelledby="cl-insights-title">
        <div>
            <p class="cl-panel-eyebrow">Signal center</p>
            <h3 id="cl-insights-title">Recent Activity</h3>
            <p class="cl-panel-subcopy">Monitor what CareerLens processed in the last hour.</p>
        </div>
        <div class="cl-insight-metrics">
            {metrics_html}
        </div>
        <div class="cl-insight-chart">
            {_render_chart_panel()}
        </div>
        <div class="cl-activity-feed">
            {activity_html}
        </div>
    </article>
    """


def render_hero_banner(user_profile: Optional[dict], matched_jobs=None) -> None:
    """
    Render the CareerLens hero + placeholder dashboard chrome when no data
    has been generated yet. Once matched jobs are available, the full dashboard
    layout rendered elsewhere will take over, so we skip output to avoid
    duplicate hero sections.
    """
    if matched_jobs:
        return

    _inject_dashboard_styles()
    _inject_hero_banner_styles()

    user_name = (user_profile or {}).get("name") or (user_profile or {}).get("first_name") or "Alex"
    subtitle = "Your market value has increased by 5% since last month."

    hero_overview = _build_hero_overview(user_name, subtitle)
    onboarding_panel = _build_onboarding_panel()
    interview_panel = _build_ai_mock_interview_panel()
    activity_panel = _build_activity_panel()

    layout_html = f"""
    <div class="cl-dashboard-wrapper">
        <div class="cl-app-shell">
            {_render_sidebar_nav("Dashboard")}
            <main class="cl-main-area" role="main" aria-live="polite">
                {hero_overview}
                <section class="cl-panel-grid" aria-label="Getting started workspace">
                    {onboarding_panel}
                    {interview_panel}
                    {activity_panel}
                </section>
            </main>
        </div>
    </div>
    """

    st.markdown(layout_html, unsafe_allow_html=True)
