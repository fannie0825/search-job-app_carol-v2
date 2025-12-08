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


def _build_recent_activity_section() -> str:
    """Return the Recent Activity section with placeholder metrics + chart."""
    metric_cards = [
        _render_metric_card(label, value, variant)
        for label, value, variant in _PLACEHOLDER_METRICS
    ]
    metrics_html = f'<div class="cl-metric-grid">{"".join(metric_cards)}</div>'
    chart_html = _render_chart_panel()
    return _render_section("Recent Activity", metrics_html + chart_html)


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

    user_name = (user_profile or {}).get("name") or (user_profile or {}).get("first_name") or "Alex"
    subtitle = "Your market value has increased by 5% since last month."

    layout_html = f"""
    <div class="cl-dashboard-wrapper">
        <div class="cl-app-shell">
            {_render_sidebar_nav("Dashboard")}
            <main class="cl-main-area" role="main" aria-live="polite">
                {_render_hero_header(user_name, subtitle)}
                {_build_recent_activity_section()}
            </main>
        </div>
    </div>
    """

    st.markdown(layout_html, unsafe_allow_html=True)
