"""File upload UI: 5-category file uploader with summary."""

import streamlit as st
from config import INPUT_CATEGORIES, SUPPORTED_EXTENSIONS


def render_upload_section() -> dict[str, list]:
    """Render the 5-category file upload interface.

    Each category gets an expandable section with a multi-file uploader.
    Returns a dict mapping category key -> list of UploadedFile objects.
    """
    st.subheader("Upload Your Sources")
    st.caption(
        "Upload files across the categories below. "
        "Customer-facing sources carry the most weight in synthesis."
    )

    uploaded = {}
    total_count = 0

    for cat_key, cat_info in INPUT_CATEGORIES.items():
        # Check session state for file count badge
        session_key = f"files_{cat_key}"
        current_files = st.session_state.get(session_key, [])
        count_badge = f" ({len(current_files)} files)" if current_files else ""

        with st.expander(
            f"{cat_info['icon']}  {cat_info['label']}{count_badge}",
            expanded=False,
        ):
            st.caption(f"{cat_info['description']} — Weight: {cat_info['weight']}x")

            files = st.file_uploader(
                f"Upload {cat_info['label']}",
                accept_multiple_files=True,
                type=SUPPORTED_EXTENSIONS,
                key=f"uploader_{cat_key}",
                label_visibility="collapsed",
            )

            if files:
                st.session_state[session_key] = files
                st.success(f"{len(files)} file(s) uploaded")

            uploaded[cat_key] = files or []
            total_count += len(uploaded[cat_key])

    # Summary bar
    if total_count > 0:
        st.divider()
        cols = st.columns(len(INPUT_CATEGORIES) + 1)
        cols[0].metric("Total Files", total_count)
        for i, (cat_key, cat_info) in enumerate(INPUT_CATEGORIES.items(), 1):
            count = len(uploaded[cat_key])
            if count > 0:
                cols[i].metric(cat_info["label"], count)
    else:
        st.info("Upload files to at least one category to get started.")

    return uploaded
