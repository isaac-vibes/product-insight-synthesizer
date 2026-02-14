"""Product Insight Synthesizer — Main Streamlit Application.

Turn scattered product signals into strategic Opportunity Solution Trees
with complete evidence attribution and interactive visualizations.
"""

import os
import time

import streamlit as st
from dotenv import load_dotenv

from lib.parser import parse_file
from lib.synthesizer import Synthesizer, SynthesisError
from lib.output import generate_markdown_report
from components.upload import render_upload_section
from components.outcomes import render_outcomes_input
from components.progress import create_progress_container
from components.results import render_results
from components.visualizations import render_visualization_section


def main():
    st.set_page_config(
        page_title="Product Insight Synthesizer",
        page_icon="🔺",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    load_dotenv()

    # Header
    st.title("🔺 Product Insight Synthesizer")
    st.caption(
        "Turn scattered product signals into strategic Opportunity Solution Trees. "
        "Upload meeting transcripts, customer calls, support tickets, and more — "
        "get evidence-based opportunity maps in minutes."
    )

    # API Key
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.warning("No `ANTHROPIC_API_KEY` found in environment. Enter it below or add it to a `.env` file.")
        api_key = st.text_input("Anthropic API Key:", type="password", key="api_key_input")
        if not api_key:
            st.stop()

    st.divider()

    # ---- Upload Section ----
    uploaded_files = render_upload_section()
    total_files = sum(len(files) for files in uploaded_files.values())

    st.divider()

    # ---- Desired Outcomes ----
    desired_outcomes = render_outcomes_input()

    st.divider()

    # ---- Synthesize Button ----
    if total_files == 0:
        st.button(
            "Synthesize Insights",
            type="primary",
            use_container_width=True,
            disabled=True,
            help="Upload files to at least one category first.",
        )
        st.stop()

    if st.button("🔍 Synthesize Insights", type="primary", use_container_width=True):
        # Parse all uploaded files
        sources = []
        parse_errors = []

        for category, files in uploaded_files.items():
            for i, uploaded_file in enumerate(files):
                try:
                    source = parse_file(uploaded_file, category, i)
                    sources.append(source)
                except Exception as e:
                    parse_errors.append(f"{uploaded_file.name}: {e}")

        if parse_errors:
            st.warning(
                f"Could not parse {len(parse_errors)} file(s):\n"
                + "\n".join(f"- {err}" for err in parse_errors)
            )

        if not sources:
            st.error("No files could be parsed. Please check your uploads.")
            st.stop()

        # Run synthesis
        st.divider()
        _, progress_bar, status_container, progress_callback = create_progress_container()

        synthesizer = Synthesizer(api_key)
        start_time = time.time()

        try:
            result = synthesizer.run(sources, desired_outcomes, progress_callback)
            result.processing_time_seconds = time.time() - start_time

            # Generate markdown report
            markdown_report = generate_markdown_report(result, sources)
            result.raw_markdown = markdown_report

            # Store in session state
            st.session_state["result"] = result
            st.session_state["markdown_report"] = markdown_report
            st.session_state["sources"] = sources

        except SynthesisError as e:
            st.error(f"Synthesis failed: {e}")
            st.caption("Try with fewer sources or check your API key.")
            st.stop()
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.stop()

    # ---- Display Results (persisted in session state) ----
    if "result" in st.session_state:
        render_results(
            st.session_state["result"],
            st.session_state["markdown_report"],
        )
        render_visualization_section(st.session_state["result"])


if __name__ == "__main__":
    main()
