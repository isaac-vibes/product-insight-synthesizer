"""Output generation: Markdown report and PDF export."""

from datetime import datetime

from config import INPUT_CATEGORIES
from lib.models import OSTResult, Source


def generate_markdown_report(result: OSTResult, sources: list[Source]) -> str:
    """Generate the full OST markdown report.

    Follows the output specification from the vision doc Section 6.1:
    Executive summary, desired outcomes with opportunities, cross-cutting
    themes, evidence index, and methodology.
    """
    lines = []

    # Header
    total = result.sources_summary.get("total", len(sources))
    by_cat = result.sources_summary.get("by_category", {})
    breakdown_parts = []
    for cat_key, cat_data in by_cat.items():
        count = cat_data.get("count", 0)
        if count > 0:
            breakdown_parts.append(f"{count} {cat_data.get('label', cat_key)}")
    breakdown_str = ", ".join(breakdown_parts) if breakdown_parts else f"{total} sources"

    lines.append("# Strategic Opportunity Solution Tree")
    lines.append(f"**Generated from:** {total} sources ({breakdown_str})")
    lines.append(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    lines.append(f"**Processing time:** {result.processing_time_seconds:.1f} seconds")
    lines.append("**Tool:** Product Insight Synthesizer v1.0")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    total_opps = sum(len(o.opportunities) for o in result.desired_outcomes)
    total_problems = sum(
        len(opp.problems)
        for outcome in result.desired_outcomes
        for opp in outcome.opportunities
    )
    total_solutions = sum(
        len(opp.solutions)
        for outcome in result.desired_outcomes
        for opp in outcome.opportunities
    )

    lines.append("## Executive Summary")
    lines.append("")
    lines.append("**Key Findings:**")
    lines.append(f"- {total_opps} opportunity areas identified")
    lines.append(f"- {len(result.desired_outcomes)} desired outcomes mapped")
    lines.append(f"- {total_problems} problems/pain points extracted across sources")
    lines.append(f"- {total_solutions} solution options explored")
    lines.append("")

    # Top priorities
    all_opps = []
    for outcome in result.desired_outcomes:
        for opp in outcome.opportunities:
            all_opps.append(opp)
    all_opps.sort(key=lambda o: o.weighted_score, reverse=True)

    if all_opps:
        lines.append("**Top Priorities:**")
        for i, opp in enumerate(all_opps[:3], 1):
            lines.append(
                f"{i}. **{opp.name}** — {opp.evidence_strength} evidence "
                f"(score: {opp.weighted_score:.1f}, {opp.source_count} sources)"
            )
        lines.append("")

    # Cross-cutting themes in summary
    if result.cross_cutting_themes:
        lines.append("**Cross-Cutting Themes:**")
        for theme in result.cross_cutting_themes:
            lines.append(f"- **{theme.name}**: {theme.source_percentage:.0f}% of sources")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Desired Outcomes + Opportunities
    for i, outcome in enumerate(result.desired_outcomes, 1):
        lines.append(f"## Desired Outcome {i}: {outcome.statement}")
        lines.append("")

        for opp in outcome.opportunities:
            lines.append(f"### Opportunity: {opp.name}")
            lines.append(f"**Evidence Strength:** {opp.evidence_strength}")

            # Source breakdown
            breakdown_parts = []
            for cat_key, count in opp.source_breakdown.items():
                if count > 0:
                    label = INPUT_CATEGORIES.get(cat_key, {}).get("label", cat_key)
                    breakdown_parts.append(f"{count} {label}")
            if breakdown_parts:
                lines.append(f"**Sources:** {opp.source_count} ({', '.join(breakdown_parts)})")

            lines.append(f"**Weighted Score:** {opp.weighted_score:.1f}")
            lines.append("")

            if opp.description:
                lines.append(f"{opp.description}")
                lines.append("")

            # Problems
            if opp.problems:
                lines.append("**Problems/Pain Points:**")
                for prob in opp.problems:
                    severity = prob.get("severity", "medium").upper()
                    desc = prob.get("description", "")
                    source_id = prob.get("source_id", "")
                    lines.append(f"- [{severity}] {desc}")
                    if source_id:
                        lines.append(f"  - *Source: {source_id}*")
                lines.append("")

            # JTBD
            if opp.jobs_to_be_done:
                lines.append("**Jobs to be Done:**")
                for jtbd in opp.jobs_to_be_done:
                    lines.append(f"- {jtbd}")
                lines.append("")

            # Solutions
            if opp.solutions:
                lines.append("**Solution Options:**")
                lines.append("")
                for j, sol in enumerate(opp.solutions, 1):
                    lines.append(f"**Option {j}: {sol.get('name', 'Untitled')}**")
                    if sol.get("description"):
                        lines.append(f"- **Description:** {sol['description']}")
                    if sol.get("expected_impact"):
                        lines.append(f"- **Expected Impact:** {sol['expected_impact']}")
                    if sol.get("effort"):
                        lines.append(f"- **Effort:** {sol['effort']}")
                    if sol.get("evidence_sources"):
                        lines.append(f"- **Evidence:** {', '.join(sol['evidence_sources'])}")
                    lines.append("")

            # Next steps
            if opp.next_steps:
                lines.append("**Next Validation Steps:**")
                for step in opp.next_steps:
                    lines.append(f"- [ ] {step}")
                lines.append("")

            # Contributing patterns
            if opp.contributing_patterns:
                lines.append(f"*Contributing patterns: {', '.join(opp.contributing_patterns)}*")
                lines.append("")

            lines.append("---")
            lines.append("")

    # Cross-Cutting Themes
    if result.cross_cutting_themes:
        lines.append("## Cross-Cutting Themes")
        lines.append("")
        for theme in result.cross_cutting_themes:
            lines.append(f"### {theme.name}")
            lines.append(f"**Prevalence:** {theme.source_percentage:.0f}% of sources")
            lines.append(f"{theme.description}")
            if theme.category_breakdown:
                breakdown_parts = []
                for cat_key, count in theme.category_breakdown.items():
                    if count > 0:
                        label = INPUT_CATEGORIES.get(cat_key, {}).get("label", cat_key)
                        breakdown_parts.append(f"{label}: {count}")
                if breakdown_parts:
                    lines.append(f"**Breakdown:** {', '.join(breakdown_parts)}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Evidence Index
    lines.append("## Evidence Index")
    lines.append("")
    lines.append("All claims in this document are traceable to source materials.")
    lines.append("")

    # Group by category
    sources_by_cat = {}
    for source in sources:
        sources_by_cat.setdefault(source.category, []).append(source)

    for cat_key, cat_sources in sources_by_cat.items():
        label = INPUT_CATEGORIES.get(cat_key, {}).get("label", cat_key)
        lines.append(f"**{label} ({len(cat_sources)}):**")
        for j, s in enumerate(cat_sources, 1):
            lines.append(f"{j}. {s.filename} (ID: {s.id})")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Methodology
    lines.append("## Methodology")
    lines.append("")
    lines.append("**Synthesis Approach:**")
    lines.append("")
    lines.append(f"1. **Multi-Source Aggregation** — {total} sources across {len(sources_by_cat)} categories")
    lines.append("2. **Data Pyramid Processing:**")
    lines.append("   - Level 1: Raw signal ingestion")
    lines.append("   - Level 2: Content categorization (problems, JTBD, pain points)")
    lines.append("   - Level 3: Cross-source pattern identification")
    lines.append("   - Level 4: Opportunity-solution mapping")
    lines.append("3. **Framework Integration:**")
    lines.append("   - Jobs-to-be-Done (Clayton Christensen)")
    lines.append("   - Opportunity Solution Trees (Teresa Torres)")
    lines.append("   - Evidence-based synthesis")
    lines.append("4. **AI Processing:**")
    lines.append("   - Tool: Product Insight Synthesizer v1.0")
    lines.append("   - Model: Claude Opus 4.6")
    lines.append(f"   - Processing time: {result.processing_time_seconds:.1f}s")
    lines.append("")
    lines.append("**Confidence Levels:**")
    lines.append("- **HIGH:** Mentioned in 10+ sources with consistent messaging")
    lines.append("- **MEDIUM:** Mentioned in 5-9 sources with general agreement")
    lines.append("- **LOW:** Mentioned in 2-4 sources or conflicting signals")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by Product Insight Synthesizer*")

    return "\n".join(lines)


def generate_pdf_report(markdown_text: str) -> bytes:
    """Convert a markdown report to PDF bytes using fpdf2.

    Parses the markdown line-by-line and renders headings, bullets,
    bold text, and body copy into a clean PDF document.
    """
    import io
    import re
    from fpdf import FPDF

    class ReportPDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 6, "Product Insight Synthesizer", align="R")
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Sanitize Unicode characters unsupported by Helvetica
    markdown_text = _sanitize_for_pdf(markdown_text)

    for line in markdown_text.split("\n"):
        stripped = line.strip()

        # Skip empty lines (add small spacing)
        if not stripped:
            pdf.ln(3)
            continue

        # Horizontal rules
        if stripped.startswith("---"):
            y = pdf.get_y()
            pdf.set_draw_color(200, 200, 200)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(5)
            continue

        # Headings
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped.lstrip("#").strip()
            text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # strip bold markers

            if level == 1:
                pdf.set_font("Helvetica", "B", 20)
                pdf.set_text_color(26, 26, 46)
                pdf.ln(5)
            elif level == 2:
                pdf.set_font("Helvetica", "B", 15)
                pdf.set_text_color(22, 33, 62)
                pdf.ln(4)
            else:
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(15, 52, 96)
                pdf.ln(3)

            pdf.multi_cell(0, 7, text)
            pdf.ln(2)
            continue

        # Bullet points
        if stripped.startswith("- ") or stripped.startswith("* "):
            text = stripped[2:]
            _write_rich_line(pdf, f"  -  {text}", indent=5)
            continue

        # Numbered items
        num_match = re.match(r"^(\d+)\.\s+(.+)", stripped)
        if num_match:
            text = f"  {num_match.group(1)}.  {num_match.group(2)}"
            _write_rich_line(pdf, text, indent=5)
            continue

        # Checkbox items
        if stripped.startswith("- [ ] ") or stripped.startswith("- [x] "):
            checked = stripped.startswith("- [x]")
            marker = "[x]" if checked else "[ ]"
            text = stripped[6:]
            _write_rich_line(pdf, f"  {marker}  {text}", indent=5)
            continue

        # Italic standalone (e.g. *Contributing patterns: ...*)
        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 5, stripped.strip("*"))
            pdf.ln(2)
            continue

        # Regular paragraph
        _write_rich_line(pdf, stripped)

    buf = io.BytesIO()
    pdf.output(buf)
    return buf.getvalue()


def _sanitize_for_pdf(text: str) -> str:
    """Replace Unicode characters that Helvetica can't render."""
    replacements = {
        "\u2022": "-",   # bullet
        "\u2013": "-",   # en dash
        "\u2014": "--",  # em dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u00a0": " ",   # non-breaking space
        "\u2192": "->",  # right arrow
        "\u2713": "[x]", # check mark
        "\u2717": "[ ]", # ballot x
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    # Fallback: replace any remaining non-latin1 characters
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _write_rich_line(pdf, text: str, indent: float = 0):
    """Write a line with basic bold (**text**) support."""
    import re

    pdf.set_text_color(51, 51, 51)

    if indent:
        pdf.set_x(pdf.l_margin + indent)

    # Split on bold markers
    parts = re.split(r"(\*\*.*?\*\*)", text)
    line_height = 5

    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            pdf.set_font("Helvetica", "B", 10)
            pdf.write(line_height, part[2:-2])
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.write(line_height, part)

    pdf.ln(line_height + 1)
