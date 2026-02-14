"""Data models for the Product Insight Synthesizer pipeline."""

from dataclasses import dataclass, field


@dataclass
class Source:
    """A single parsed input document."""
    id: str                     # e.g. "customer_calls_001"
    filename: str
    category: str               # key from INPUT_CATEGORIES
    content: str                # extracted text
    weight: float               # from category weight


@dataclass
class ExtractedInsight:
    """Level 2 output: categorized insight from a single source."""
    source_id: str
    category: str
    problems: list[dict] = field(default_factory=list)
    # Each: {"description": str, "severity": "high"|"medium"|"low", "evidence": str}
    jobs_to_be_done: list[str] = field(default_factory=list)
    pain_points: list[dict] = field(default_factory=list)
    # Each: {"description": str, "severity": "high"|"medium"|"low"}
    desired_outcomes: list[str] = field(default_factory=list)
    solution_requests: list[str] = field(default_factory=list)


@dataclass
class Pattern:
    """Level 3 output: a cross-source pattern."""
    name: str
    description: str
    frequency: int                              # number of sources mentioning it
    severity: str                               # "high" | "medium" | "low"
    weighted_score: float                       # sum of source weights
    business_impact: str
    cross_org_signal: bool                      # appears in 2+ categories
    evidence: list[dict] = field(default_factory=list)
    # Each: {"source_id": str, "category": str, "weight": float, "quote": str}
    source_categories: dict = field(default_factory=dict)
    # {"customer_calls": 3, "internal_meetings": 2, ...}


@dataclass
class Opportunity:
    """Level 4 output: one opportunity in the OST."""
    name: str
    description: str
    evidence_strength: str      # "HIGH" | "MEDIUM" | "LOW"
    weighted_score: float
    source_count: int
    source_breakdown: dict = field(default_factory=dict)
    # category -> count
    problems: list[dict] = field(default_factory=list)
    jobs_to_be_done: list[str] = field(default_factory=list)
    solutions: list[dict] = field(default_factory=list)
    # Each: {"name": str, "description": str, "expected_impact": str,
    #         "effort": str, "evidence_sources": list[str]}
    next_steps: list[str] = field(default_factory=list)
    contributing_patterns: list[str] = field(default_factory=list)


@dataclass
class DesiredOutcome:
    """A desired outcome (user-provided or AI-inferred)."""
    statement: str
    opportunities: list[Opportunity] = field(default_factory=list)


@dataclass
class CrossCuttingTheme:
    """A theme that cuts across multiple opportunities."""
    name: str
    description: str
    source_percentage: float
    category_breakdown: dict = field(default_factory=dict)


@dataclass
class OSTResult:
    """The complete synthesis result."""
    desired_outcomes: list[DesiredOutcome] = field(default_factory=list)
    cross_cutting_themes: list[CrossCuttingTheme] = field(default_factory=list)
    evidence_index: list[dict] = field(default_factory=list)
    sources_summary: dict = field(default_factory=dict)
    processing_time_seconds: float = 0.0
    raw_markdown: str = ""
