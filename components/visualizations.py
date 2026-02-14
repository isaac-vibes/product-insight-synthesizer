"""Plotly visualizations: treemap overview and drill-down bar charts."""

import streamlit as st
import plotly.graph_objects as go

from config import INPUT_CATEGORIES, CATEGORY_COLORS, CATEGORY_LABELS
from lib.models import OSTResult, Opportunity


# Evidence strength to color intensity
STRENGTH_COLORS = {
    "HIGH": "#1a5276",
    "MEDIUM": "#2980b9",
    "LOW": "#85c1e9",
}


def render_visualization_section(result: OSTResult):
    """Main visualization entry point: treemap + drill-down."""
    st.subheader("Opportunity Landscape")
    st.caption(
        "Size represents weighted evidence strength. "
        "Select an opportunity below to see its cross-organizational breakdown."
    )

    # Render treemap
    _render_treemap(result)

    st.divider()

    # Drill-down selector
    all_opportunities = []
    for outcome in result.desired_outcomes:
        for opp in outcome.opportunities:
            all_opportunities.append(opp)

    if not all_opportunities:
        st.warning("No opportunities identified.")
        return

    opp_names = [opp.name for opp in all_opportunities]
    selected_name = st.selectbox(
        "Select an opportunity to explore its cross-org evidence:",
        options=opp_names,
        key="opp_drilldown",
    )

    selected_opp = next(
        (o for o in all_opportunities if o.name == selected_name), None
    )
    if selected_opp:
        _render_drilldown(selected_opp)


def _render_treemap(result: OSTResult):
    """Render the opportunity landscape treemap."""
    ids = ["root"]
    labels = ["Opportunity Landscape"]
    parents = [""]
    values = [0]
    colors = ["#ecf0f1"]
    custom_data = [{"sources": 0, "strength": ""}]

    for outcome in result.desired_outcomes:
        outcome_id = f"outcome_{outcome.statement[:40]}"
        ids.append(outcome_id)
        labels.append(outcome.statement)
        parents.append("root")
        values.append(0)
        colors.append("#d5e8f0")
        custom_data.append({"sources": 0, "strength": ""})

        for opp in outcome.opportunities:
            opp_id = f"opp_{opp.name[:40]}"
            ids.append(opp_id)
            labels.append(opp.name)
            parents.append(outcome_id)
            values.append(max(opp.weighted_score, 0.1))  # minimum size for visibility
            colors.append(STRENGTH_COLORS.get(opp.evidence_strength, STRENGTH_COLORS["MEDIUM"]))
            custom_data.append({
                "sources": opp.source_count,
                "strength": opp.evidence_strength,
            })

    fig = go.Figure(go.Treemap(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="remainder",
        marker=dict(
            colors=colors,
            line=dict(width=2, color="white"),
        ),
        textinfo="label+value",
        textfont=dict(size=14, color="white"),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Evidence Score: %{value:.1f}<br>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_drilldown(opportunity: Opportunity):
    """Render drill-down charts for a selected opportunity."""
    st.subheader(f"Deep Dive: {opportunity.name}")

    if opportunity.description:
        st.markdown(f"*{opportunity.description}*")

    # Prepare data
    categories = list(INPUT_CATEGORIES.keys())
    display_names = [INPUT_CATEGORIES[cat]["label"] for cat in categories]
    colors = [INPUT_CATEGORIES[cat]["color"] for cat in categories]

    counts = [opportunity.source_breakdown.get(cat, 0) for cat in categories]
    weights = [
        opportunity.source_breakdown.get(cat, 0) * INPUT_CATEGORIES[cat]["weight"]
        for cat in categories
    ]

    # Filter to categories that have data
    active = [(dn, c, w, col) for dn, c, w, col in zip(display_names, counts, weights, colors) if c > 0]

    if not active:
        st.info("No source breakdown data available for this opportunity.")
        return

    active_names, active_counts, active_weights, active_colors = zip(*active)

    # Chart 1: Source Count by Category
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Source Count by Category**")
        st.caption("How many sources from each category mention this opportunity")

        fig1 = go.Figure(go.Bar(
            x=list(active_names),
            y=list(active_counts),
            marker_color=list(active_colors),
            text=list(active_counts),
            textposition="auto",
        ))
        fig1.update_layout(
            xaxis_title="Source Category",
            yaxis_title="Number of Sources",
            height=350,
            margin=dict(t=10, b=40),
            showlegend=False,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("**Weighted Impact by Category**")
        st.caption("Count × category weight — shows why customer signals dominate")

        fig2 = go.Figure(go.Bar(
            x=list(active_names),
            y=list(active_weights),
            marker_color=list(active_colors),
            text=[f"{w:.1f}" for w in active_weights],
            textposition="auto",
        ))
        fig2.update_layout(
            xaxis_title="Source Category",
            yaxis_title="Weighted Score",
            height=350,
            margin=dict(t=10, b=40),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Cross-org insight callout
    categories_with_data = sum(1 for c in counts if c > 0)
    if categories_with_data >= 2:
        st.success(
            f"🔍 **Cross-Org Signal:** This opportunity surfaces across "
            f"**{categories_with_data} different source categories** — "
            f"it's not just one team's problem. "
            f"Total evidence score: **{opportunity.weighted_score:.1f}**"
        )
    elif categories_with_data == 1:
        st.info(
            f"This opportunity currently has evidence from 1 source category. "
            f"Consider investigating whether other teams experience similar friction."
        )

    # Evidence details in expander
    with st.expander("View detailed evidence"):
        if opportunity.problems:
            st.markdown("**Problems:**")
            for prob in opportunity.problems:
                severity = prob.get("severity", "medium").upper()
                st.markdown(f"- [{severity}] {prob.get('description', '')}")

        if opportunity.jobs_to_be_done:
            st.markdown("**Jobs to be Done:**")
            for jtbd in opportunity.jobs_to_be_done:
                st.markdown(f"- {jtbd}")

        if opportunity.solutions:
            st.markdown("**Proposed Solutions:**")
            for sol in opportunity.solutions:
                effort = sol.get("effort", "")
                st.markdown(
                    f"- **{sol.get('name', '')}** ({effort} effort): "
                    f"{sol.get('description', '')}"
                )
