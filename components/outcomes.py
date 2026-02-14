"""Desired outcomes input component."""

import streamlit as st
from config import MAX_DESIRED_OUTCOMES


def render_outcomes_input() -> list[str]:
    """Render the desired outcomes input section.

    Users can either let the AI derive outcomes from their data (default)
    or specify 1-3 custom desired outcomes.

    Returns:
        List of outcome strings. Empty list means AI should derive them.
    """
    st.subheader("Desired Outcomes")

    ai_derive = st.checkbox(
        "Let AI identify outcomes from your data",
        value=True,
        help="When checked, the AI will infer strategic outcomes from the patterns "
             "it finds in your sources. Uncheck to specify your own.",
    )

    if ai_derive:
        st.caption(
            "The AI will analyze your sources and identify 2-4 strategic "
            "desired outcomes based on the strongest evidence patterns."
        )
        return []

    st.caption(
        f"Specify up to {MAX_DESIRED_OUTCOMES} desired outcomes. "
        "These guide how the AI organizes opportunities."
    )

    outcomes = []
    for i in range(MAX_DESIRED_OUTCOMES):
        placeholder = {
            0: "e.g., Reduce customer onboarding time by 50%",
            1: "e.g., Increase customer retention rate",
            2: "e.g., Improve internal team velocity",
        }.get(i, "")

        value = st.text_input(
            f"Outcome {i + 1}",
            placeholder=placeholder,
            key=f"outcome_{i}",
        )
        if value.strip():
            outcomes.append(value.strip())

    if not outcomes:
        st.warning("Enter at least one outcome, or check the box above to let AI decide.")

    return outcomes
