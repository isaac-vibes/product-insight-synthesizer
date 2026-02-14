"""File parsing: convert uploaded files into Source objects."""

import io
import pandas as pd
from lib.models import Source
from config import INPUT_CATEGORIES, MAX_CHARS_PER_SOURCE


def parse_file(uploaded_file, category: str, index: int) -> Source:
    """Parse an uploaded file and return a Source object.

    Args:
        uploaded_file: Streamlit UploadedFile object.
        category: Key from INPUT_CATEGORIES (e.g. "customer_calls").
        index: Index within this category for ID generation.

    Returns:
        Source with extracted text content.
    """
    filename = uploaded_file.name
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    raw_bytes = uploaded_file.read()

    parsers = {
        "txt": _parse_txt,
        "docx": _parse_docx,
        "pdf": _parse_pdf,
        "csv": _parse_csv,
    }

    parser = parsers.get(ext)
    if parser is None:
        content = f"[Unsupported file format: .{ext}]"
    else:
        try:
            content = parser(raw_bytes)
        except Exception as e:
            content = f"[Error parsing {filename}: {e}]"

    # Truncate if too long
    if len(content) > MAX_CHARS_PER_SOURCE:
        content = content[:MAX_CHARS_PER_SOURCE] + "\n\n[... content truncated ...]"

    weight = INPUT_CATEGORIES[category]["weight"]
    source_id = f"{category}_{index:03d}"

    return Source(
        id=source_id,
        filename=filename,
        category=category,
        content=content,
        weight=weight,
    )


def _parse_txt(raw_bytes: bytes) -> str:
    """Decode plain text bytes."""
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return raw_bytes.decode(encoding).strip()
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace").strip()


def _parse_docx(raw_bytes: bytes) -> str:
    """Extract text from a Word document."""
    from docx import Document

    doc = Document(io.BytesIO(raw_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def _parse_pdf(raw_bytes: bytes) -> str:
    """Extract text from a PDF."""
    from PyPDF2 import PdfReader

    reader = PdfReader(io.BytesIO(raw_bytes))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())
    return "\n\n".join(pages)


def _parse_csv(raw_bytes: bytes) -> str:
    """Parse CSV into readable text blocks.

    Detects common content columns (description, body, content, summary,
    comment, text, notes) and formats each row as a readable entry.
    Falls back to full DataFrame string representation.
    """
    df = pd.read_csv(io.BytesIO(raw_bytes))

    # Look for content-bearing columns
    content_columns = []
    for col in df.columns:
        if col.lower() in (
            "description", "body", "content", "summary",
            "comment", "text", "notes", "message", "details",
        ):
            content_columns.append(col)

    # Also grab metadata columns if present
    meta_columns = []
    for col in df.columns:
        if col.lower() in (
            "subject", "title", "status", "priority", "created_at",
            "date", "category", "type", "id", "ticket_id",
        ):
            meta_columns.append(col)

    if content_columns:
        entries = []
        for _, row in df.iterrows():
            parts = []
            for mc in meta_columns:
                val = row.get(mc)
                if pd.notna(val):
                    parts.append(f"{mc}: {val}")
            for cc in content_columns:
                val = row.get(cc)
                if pd.notna(val):
                    parts.append(str(val))
            if parts:
                entries.append("\n".join(parts))
        return "\n\n---\n\n".join(entries)

    # Fallback: stringify the whole DataFrame
    return df.to_string(index=False)
