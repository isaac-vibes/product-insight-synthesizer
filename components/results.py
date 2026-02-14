"""Results display component: summary, downloads, and full report."""

import streamlit as st

from lib.models import OSTResult
from lib.output import generate_pdf_report


def render_results(result: OSTResult, markdown_report: str):
    """Render the results section with summary stats and download buttons."""
    st.divider()
    st.header("Synthesis Results")

    # Summary metrics row
    total_opps = sum(len(o.opportunities) for o in result.desired_outcomes)
    total_problems = sum(
        len(opp.problems)
        for outcome in result.desired_outcomes
        for opp in outcome.opportunities
    )
    cross_org_opps = sum(
        1
        for outcome in result.desired_outcomes
        for opp in outcome.opportunities
        if sum(1 for v in opp.source_breakdown.values() if v > 0) >= 2
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Desired Outcomes", len(result.desired_outcomes))
    col2.metric("Opportunities", total_opps)
    col3.metric("Problems Found", total_problems)
    col4.metric("Cross-Org Signals", cross_org_opps)
    col5.metric("Processing Time", f"{result.processing_time_seconds:.1f}s")

    st.divider()

    # Download buttons
    st.subheader("Download Report")
    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        st.download_button(
            label="📄 Download Markdown Report",
            data=markdown_report,
            file_name="opportunity_solution_tree.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with dl_col2:
        try:
            pdf_bytes = generate_pdf_report(markdown_report)
            st.download_button(
                label="📑 Download PDF Report",
                data=pdf_bytes,
                file_name="opportunity_solution_tree.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.warning(f"PDF generation unavailable: {e}")
            st.caption("The markdown report is still available for download.")

    st.divider()

    # Full report in expander
    with st.expander("📋 View Full Report", expanded=False):
        st.markdown(markdown_report)
