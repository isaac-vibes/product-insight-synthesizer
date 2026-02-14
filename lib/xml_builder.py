"""Build structured XML from parsed sources for Claude's context window."""

from xml.sax.saxutils import escape
from lib.models import Source, ExtractedInsight, Pattern
from config import INPUT_CATEGORIES, MAX_CHARS_PER_SOURCE


def build_sources_xml(sources: list[Source]) -> str:
    """Convert Source objects into structured XML for Level 2 processing.

    Each source is tagged with its id, category, weight, and filename
    so Claude can maintain attribution throughout synthesis.
    """
    # Summary header
    category_counts = {}
    for s in sources:
        category_counts[s.category] = category_counts.get(s.category, 0) + 1

    breakdown = ", ".join(
        f"{INPUT_CATEGORIES[cat]['label']}: {count}"
        for cat, count in category_counts.items()
        if count > 0
    )

    lines = [f'<sources total="{len(sources)}" breakdown="{escape(breakdown)}">']

    for source in sources:
        content = source.content
        if len(content) > MAX_CHARS_PER_SOURCE:
            content = content[:MAX_CHARS_PER_SOURCE] + "\n[truncated]"

        lines.append(
            f'  <source id="{escape(source.id)}" '
            f'category="{escape(source.category)}" '
            f'weight="{source.weight}" '
            f'filename="{escape(source.filename)}">'
        )
        lines.append(f"    <content>{escape(content)}</content>")
        lines.append("  </source>")

    lines.append("</sources>")
    return "\n".join(lines)


def build_insights_xml(insights: list[ExtractedInsight]) -> str:
    """Convert Level 2 ExtractedInsight objects into XML for Level 3."""
    lines = [f'<categorized_insights total="{len(insights)}">']

    for insight in insights:
        lines.append(
            f'  <source_insight source_id="{escape(insight.source_id)}" '
            f'category="{escape(insight.category)}">'
        )

        # Problems
        if insight.problems:
            lines.append("    <problems>")
            for p in insight.problems:
                sev = escape(p.get("severity", "medium"))
                lines.append(f'      <problem severity="{sev}">')
                lines.append(f"        <description>{escape(p.get('description', ''))}</description>")
                if p.get("evidence"):
                    lines.append(f"        <evidence>{escape(p['evidence'])}</evidence>")
                lines.append("      </problem>")
            lines.append("    </problems>")

        # Jobs to be done
        if insight.jobs_to_be_done:
            lines.append("    <jobs_to_be_done>")
            for j in insight.jobs_to_be_done:
                lines.append(f"      <jtbd>{escape(j)}</jtbd>")
            lines.append("    </jobs_to_be_done>")

        # Pain points
        if insight.pain_points:
            lines.append("    <pain_points>")
            for pp in insight.pain_points:
                sev = escape(pp.get("severity", "medium"))
                lines.append(f'      <pain severity="{sev}">{escape(pp.get("description", ""))}</pain>')
            lines.append("    </pain_points>")

        # Desired outcomes
        if insight.desired_outcomes:
            lines.append("    <desired_outcomes>")
            for o in insight.desired_outcomes:
                lines.append(f"      <outcome>{escape(o)}</outcome>")
            lines.append("    </desired_outcomes>")

        # Solution requests
        if insight.solution_requests:
            lines.append("    <solution_requests>")
            for sr in insight.solution_requests:
                lines.append(f"      <request>{escape(sr)}</request>")
            lines.append("    </solution_requests>")

        lines.append("  </source_insight>")

    lines.append("</categorized_insights>")
    return "\n".join(lines)


def build_patterns_xml(patterns: list[Pattern]) -> str:
    """Convert Level 3 Pattern objects into XML for Level 4."""
    lines = [f'<patterns total="{len(patterns)}">']

    for pattern in patterns:
        lines.append("  <pattern>")
        lines.append(f"    <name>{escape(pattern.name)}</name>")
        lines.append(f"    <description>{escape(pattern.description)}</description>")
        lines.append(f"    <frequency>{pattern.frequency}</frequency>")
        lines.append(f"    <weighted_score>{pattern.weighted_score:.1f}</weighted_score>")
        lines.append(f'    <severity>{escape(pattern.severity)}</severity>')
        lines.append(f"    <business_impact>{escape(pattern.business_impact)}</business_impact>")
        lines.append(f"    <cross_org_signal>{str(pattern.cross_org_signal).lower()}</cross_org_signal>")

        # Evidence
        if pattern.evidence:
            lines.append("    <evidence>")
            for e in pattern.evidence:
                lines.append(
                    f'      <source source_id="{escape(e.get("source_id", ""))}" '
                    f'category="{escape(e.get("category", ""))}" '
                    f'weight="{e.get("weight", 1.0)}">'
                )
                lines.append(f"        {escape(e.get('quote', ''))}")
                lines.append("      </source>")
            lines.append("    </evidence>")

        # Source breakdown
        if pattern.source_categories:
            lines.append("    <source_breakdown>")
            for cat, count in pattern.source_categories.items():
                lines.append(f'      <category name="{escape(cat)}" count="{count}" />')
            lines.append("    </source_breakdown>")

        lines.append("  </pattern>")

    lines.append("</patterns>")
    return "\n".join(lines)
