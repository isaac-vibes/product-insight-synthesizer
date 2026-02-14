"""Claude prompt templates for each level of the data pyramid."""

from config import INPUT_CATEGORIES

# ---------------------------------------------------------------------------
# Level 2: Categorization — extract structured insights from each source
# ---------------------------------------------------------------------------

LEVEL_2_SYSTEM = """You are a senior product strategist analyzing raw product signals.
You extract structured insights from source documents using Teresa Torres'
Opportunity Solution Tree framework and Clayton Christensen's Jobs-to-be-Done.

You are meticulous about preserving source attribution — every extraction
must reference the source it came from. You distinguish between problems
(what's broken), jobs-to-be-done (what users are trying to accomplish),
and solution requests (specific asks — note but do not prioritize)."""

LEVEL_2_USER = """<task>
Analyze each source document below. For EACH source, extract:

1. **Problems** — What is broken, painful, or inefficient? Include severity (high/medium/low) and a direct quote as evidence.
2. **Jobs-to-be-Done** — What is the user/customer trying to accomplish? Use format: "When [situation], I want to [motivation], so I can [outcome]"
3. **Pain points** — Impact and severity of friction points (high/medium/low).
4. **Desired outcomes** — What does success look like from this source's perspective?
5. **Solution requests** — Specific feature or product asks mentioned. Note these but do NOT prioritize them over problems/JTBD.

CRITICAL: Preserve the source ID exactly as given for every extraction.
If a source has no relevant content for a category, omit that category — do not fabricate.
</task>

{sources_xml}

<output_format>
Respond ONLY with valid JSON. No markdown code fences, no other text before or after.

[
  {{
    "source_id": "exact source id from input",
    "category": "category from input",
    "problems": [
      {{
        "description": "Clear description of the problem",
        "severity": "high|medium|low",
        "evidence": "Direct quote from the source"
      }}
    ],
    "jobs_to_be_done": [
      "When [situation], I want to [motivation], so I can [outcome]"
    ],
    "pain_points": [
      {{
        "description": "Description of friction",
        "severity": "high|medium|low"
      }}
    ],
    "desired_outcomes": [
      "What success looks like"
    ],
    "solution_requests": [
      "Specific ask mentioned"
    ]
  }}
]
</output_format>"""


# ---------------------------------------------------------------------------
# Level 3: Pattern Synthesis — find cross-source patterns
# ---------------------------------------------------------------------------

LEVEL_3_SYSTEM = """You are a senior product strategist performing cross-source
pattern analysis. You identify recurring themes and patterns across diverse
product signals, with special attention to patterns that span multiple
organizational levels (customers, internal teams, support).

The most valuable insight is when a problem appears across multiple source
categories — this signals a systemic issue, not an isolated complaint.
You weight sources by their importance to strategic decisions."""


def build_level_3_user(source_count: int, category_counts: dict) -> str:
    """Build the Level 3 user prompt with dynamic source counts."""
    breakdown_lines = []
    for cat_key, cat_info in INPUT_CATEGORIES.items():
        count = category_counts.get(cat_key, 0)
        breakdown_lines.append(
            f"- {cat_info['label']} (weight: {cat_info['weight']}x) — {count} sources"
        )
    breakdown = "\n".join(breakdown_lines)

    return f"""<task>
You have categorized insights from {source_count} sources across these
categories (with importance weights):

{breakdown}

Identify PATTERNS: problems, needs, or themes that appear across MULTIPLE
sources. The most powerful signal is when a pattern spans multiple
categories (e.g., customers AND internal teams AND support all mention
the same friction).

For each pattern:
1. Give it a clear, descriptive name
2. Count how many sources mention it (frequency)
3. Calculate weighted_score = sum of weights of all sources mentioning it
4. Assess severity (high/medium/low)
5. Describe business impact (revenue, churn, efficiency, etc.)
6. Flag if it's a cross-org signal (appears in 2+ categories)
7. List all evidence with source IDs and quotes

Prioritize patterns that:
- Appear in MULTIPLE categories (cross-org = strongest signal)
- Have high weighted scores
- Show high severity across sources

List ALL patterns, even those in only 2-3 sources.
</task>

{{insights_xml}}

<output_format>
Respond ONLY with valid JSON. No markdown code fences, no other text before or after.

[
  {{
    "name": "Short descriptive name",
    "description": "What this pattern represents",
    "frequency": 5,
    "weighted_score": 12.5,
    "severity": "high|medium|low",
    "business_impact": "Revenue/churn/efficiency impact",
    "cross_org_signal": true,
    "evidence": [
      {{
        "source_id": "...",
        "category": "...",
        "weight": 3.0,
        "quote": "Quote or summary from this source"
      }}
    ],
    "source_breakdown": {{
      "customer_calls": 2,
      "internal_meetings": 1,
      "support_tickets": 1,
      "other_sources": 1,
      "miscellaneous": 0
    }}
  }}
]
</output_format>"""


# ---------------------------------------------------------------------------
# Level 4: Opportunity Mapping — build the OST
# ---------------------------------------------------------------------------

LEVEL_4_SYSTEM = """You are a senior product strategist creating an Opportunity
Solution Tree following Teresa Torres' framework. You map validated patterns
into strategic opportunity spaces with actionable solution options.

Your output drives both a structured report AND interactive visualizations,
so you must return well-formed JSON with numeric scores and complete
source breakdowns.

Key principle: Opportunities represent problem/need spaces — NOT solutions.
Solutions are options to explore within each opportunity space."""


def build_level_4_user(source_count: int, desired_outcomes: list[str]) -> str:
    """Build the Level 4 user prompt with optional desired outcomes."""
    if desired_outcomes:
        outcomes_section = (
            "Map opportunities to these user-specified desired outcomes:\n"
            + "\n".join(f"- {o}" for o in desired_outcomes)
            + "\n\nYou may also identify additional outcomes if strongly supported by the data."
        )
    else:
        outcomes_section = (
            "Infer 2-4 desired outcomes from the strongest patterns. "
            "These should be strategic goals that the evidence supports, "
            "stated as measurable outcomes (e.g., 'Reduce customer onboarding time by 50%')."
        )

    return f"""<task>
Using the patterns identified across {source_count} sources, create an
Opportunity Solution Tree.

**Desired Outcomes:**
{outcomes_section}

For EACH desired outcome:
1. Group related patterns into OPPORTUNITY SPACES (problem/need clusters)
2. For each opportunity, propose 2-3 SOLUTION OPTIONS
3. Rank opportunities by weighted_score (higher = more evidence = higher priority)
4. Include a source_breakdown showing how many sources from each category contribute

CRITICAL: The source_breakdown per opportunity is essential — it powers the
visualization that shows users how problems span across organizational levels.

The "aha moment" we want to create: "I knew this was a customer problem,
but I didn't realize internal teams and support are also struggling with
the same thing — fixing this one area has outsized impact."
</task>

{{patterns_xml}}

<output_format>
Respond ONLY with valid JSON. No markdown, no code fences, no other text.

{{{{
  "desired_outcomes": [
    {{{{
      "statement": "Measurable outcome statement",
      "opportunities": [
        {{{{
          "name": "Opportunity Space Name",
          "description": "What problem/need space this represents",
          "evidence_strength": "HIGH|MEDIUM|LOW",
          "weighted_score": 12.5,
          "source_count": 8,
          "source_breakdown": {{{{
            "customer_calls": 3,
            "internal_meetings": 2,
            "support_tickets": 2,
            "other_sources": 1,
            "miscellaneous": 0
          }}}},
          "problems": [
            {{{{"description": "...", "source_id": "...", "severity": "high"}}}}
          ],
          "jobs_to_be_done": ["When..., I want..., so I can..."],
          "solutions": [
            {{{{
              "name": "Solution name",
              "description": "What this solution does",
              "expected_impact": "Quantified if possible",
              "effort": "HIGH|MEDIUM|LOW",
              "evidence_sources": ["source_id_1", "source_id_2"]
            }}}}
          ],
          "next_steps": ["Interview X customers about...", "Prototype Y..."],
          "contributing_patterns": ["pattern_name_1", "pattern_name_2"]
        }}}}
      ]
    }}}}
  ],
  "cross_cutting_themes": [
    {{{{
      "name": "Theme name",
      "description": "What this theme represents",
      "source_percentage": 45,
      "category_breakdown": {{{{"customer_calls": 5, "internal_meetings": 3}}}}
    }}}}
  ]
}}}}
</output_format>"""
