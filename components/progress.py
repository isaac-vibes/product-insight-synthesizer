"""Processing progress display component."""

import streamlit as st


# Synthesis pipeline stages in order
STAGES = [
    "Loading and structuring sources...",
    "Categorizing content from each source...",
    "Identifying cross-source patterns...",
    "Mapping opportunity spaces...",
    "Synthesis complete!",
]


def create_progress_container():
    """Create and return a Streamlit container for progress updates.

    Returns a (container, callback) tuple. Pass the callback to
    Synthesizer.run() as progress_callback.
    """
    container = st.empty()
    progress_bar = st.progress(0)
    status = st.status("Starting synthesis...", expanded=True)

    completed_stages = []

    def progress_callback(stage: str, percent: int):
        progress_bar.progress(min(percent, 100) / 100)

        # Track completed stages
        if stage not in completed_stages:
            completed_stages.append(stage)

        with status:
            for completed in completed_stages[:-1]:
                st.write(f"✅ {completed}")
            if percent < 100:
                st.write(f"⏳ {stage}")
            else:
                st.write(f"✅ {stage}")

        if percent >= 100:
            status.update(label="Synthesis complete!", state="complete")

    return container, progress_bar, status, progress_callback
