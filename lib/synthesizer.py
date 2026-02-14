"""Core synthesis engine: runs the 4-level data pyramid via Claude API."""

import json
import re

import anthropic

from config import MODEL_ID, MAX_TOKENS_OUTPUT, INPUT_CATEGORIES, MAX_TOTAL_CHARS
from lib.models import (
    Source, ExtractedInsight, Pattern, Opportunity,
    DesiredOutcome, CrossCuttingTheme, OSTResult,
)
from lib.xml_builder import build_sources_xml, build_insights_xml, build_patterns_xml
from lib.prompts import (
    LEVEL_2_SYSTEM, LEVEL_2_USER,
    LEVEL_3_SYSTEM, build_level_3_user,
    LEVEL_4_SYSTEM, build_level_4_user,
)


class SynthesisError(Exception):
    """Raised when synthesis fails at any level."""


class Synthesizer:
    """Orchestrates the 4-level data pyramid synthesis pipeline."""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def run(
        self,
        sources: list[Source],
        desired_outcomes: list[str],
        progress_callback=None,
    ) -> OSTResult:
        """Execute the full 4-level synthesis pipeline.

        Args:
            sources: Parsed Source objects from all categories.
            desired_outcomes: User-specified outcomes (empty = AI derives).
            progress_callback: Optional fn(stage: str, percent: int) for UI.

        Returns:
            Complete OSTResult ready for visualization and report generation.
        """
        if progress_callback:
            progress_callback("Loading and structuring sources...", 5)

        # Build source summary
        category_counts = {}
        for s in sources:
            category_counts[s.category] = category_counts.get(s.category, 0) + 1

        sources_summary = {
            "total": len(sources),
            "by_category": {
                cat: {
                    "count": category_counts.get(cat, 0),
                    "label": info["label"],
                }
                for cat, info in INPUT_CATEGORIES.items()
            },
        }

        # Level 2: Categorization
        if progress_callback:
            progress_callback("Categorizing content from each source...", 10)
        insights = self._categorize(sources)

        # Level 3: Pattern Synthesis
        if progress_callback:
            progress_callback("Identifying cross-source patterns...", 40)
        patterns = self._find_patterns(sources, insights, category_counts)

        # Level 4: Opportunity Mapping
        if progress_callback:
            progress_callback("Mapping opportunity spaces...", 70)
        result = self._map_opportunities(sources, patterns, desired_outcomes)

        # Build evidence index
        evidence_index = self._build_evidence_index(sources)

        result.evidence_index = evidence_index
        result.sources_summary = sources_summary

        if progress_callback:
            progress_callback("Synthesis complete!", 100)

        return result

    # ----- Claude API -----

    def _call_claude(self, system: str, user: str) -> str:
        """Make a single Claude API call."""
        response = self.client.messages.create(
            model=MODEL_ID,
            max_tokens=MAX_TOKENS_OUTPUT,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        if response.stop_reason == "max_tokens":
            raise SynthesisError(
                "Claude's response was truncated (hit max_tokens limit). "
                "Try uploading fewer files or contact support."
            )
        return response.content[0].text

    # ----- Level 2: Categorization -----

    # Max sources per Level 2 batch — keeps output well under MAX_TOKENS_OUTPUT.
    # ~900 output tokens per source; 10 sources ≈ 9K tokens (safe under 16K).
    _L2_BATCH_SIZE = 10

    def _categorize(self, sources: list[Source]) -> list[ExtractedInsight]:
        """Level 2: Extract structured insights from each source."""
        if len(sources) <= self._L2_BATCH_SIZE:
            return self._categorize_batch(sources)

        # Batch to stay within output token limits
        all_insights = []
        for i in range(0, len(sources), self._L2_BATCH_SIZE):
            batch = sources[i : i + self._L2_BATCH_SIZE]
            all_insights.extend(self._categorize_batch(batch))
        return all_insights

    def _categorize_batch(self, sources: list[Source]) -> list[ExtractedInsight]:
        """Categorize a single batch of sources."""
        sources_xml = build_sources_xml(sources)
        user_prompt = LEVEL_2_USER.format(sources_xml=sources_xml)
        raw = self._call_claude(LEVEL_2_SYSTEM, user_prompt)
        return self._parse_level_2_response(raw)

    def _parse_level_2_response(self, raw: str) -> list[ExtractedInsight]:
        """Parse Level 2 JSON response into ExtractedInsight objects."""
        data = self._parse_json_response(raw, "Level 2")

        if not isinstance(data, list):
            raise SynthesisError("Level 2 response is not a JSON array")

        insights = []
        for item in data:
            insights.append(ExtractedInsight(
                source_id=item.get("source_id", "unknown"),
                category=item.get("category", "unknown"),
                problems=item.get("problems", []),
                jobs_to_be_done=item.get("jobs_to_be_done", []),
                pain_points=item.get("pain_points", []),
                desired_outcomes=item.get("desired_outcomes", []),
                solution_requests=item.get("solution_requests", []),
            ))

        return insights

    # ----- Level 3: Pattern Synthesis -----

    def _find_patterns(
        self,
        sources: list[Source],
        insights: list[ExtractedInsight],
        category_counts: dict,
    ) -> list[Pattern]:
        """Level 3: Identify cross-source patterns."""
        insights_xml = build_insights_xml(insights)
        user_template = build_level_3_user(len(sources), category_counts)
        user_prompt = user_template.replace("{insights_xml}", insights_xml)
        raw = self._call_claude(LEVEL_3_SYSTEM, user_prompt)
        return self._parse_level_3_response(raw)

    def _parse_level_3_response(self, raw: str) -> list[Pattern]:
        """Parse Level 3 JSON response into Pattern objects."""
        data = self._parse_json_response(raw, "Level 3")

        if not isinstance(data, list):
            raise SynthesisError("Level 3 response is not a JSON array")

        patterns = []
        for item in data:
            patterns.append(Pattern(
                name=item.get("name", ""),
                description=item.get("description", ""),
                frequency=int(item.get("frequency", 0)),
                severity=item.get("severity", "medium"),
                weighted_score=float(item.get("weighted_score", 0)),
                business_impact=item.get("business_impact", ""),
                cross_org_signal=bool(item.get("cross_org_signal", False)),
                evidence=item.get("evidence", []),
                source_categories=item.get("source_breakdown", {}),
            ))

        return patterns

    # ----- Level 4: Opportunity Mapping -----

    def _map_opportunities(
        self,
        sources: list[Source],
        patterns: list[Pattern],
        desired_outcomes: list[str],
    ) -> OSTResult:
        """Level 4: Map patterns to OST structure."""
        patterns_xml = build_patterns_xml(patterns)
        user_template = build_level_4_user(len(sources), desired_outcomes)
        user_prompt = user_template.replace("{patterns_xml}", patterns_xml)
        raw = self._call_claude(LEVEL_4_SYSTEM, user_prompt)
        return self._parse_level_4_response(raw)

    def _parse_level_4_response(self, raw: str) -> OSTResult:
        """Parse Level 4 JSON response into OSTResult."""
        data = self._parse_json_response(raw, "Level 4")

        result = OSTResult()

        for outcome_data in data.get("desired_outcomes", []):
            outcome = DesiredOutcome(statement=outcome_data.get("statement", ""))

            for opp_data in outcome_data.get("opportunities", []):
                opp = Opportunity(
                    name=opp_data.get("name", ""),
                    description=opp_data.get("description", ""),
                    evidence_strength=opp_data.get("evidence_strength", "MEDIUM"),
                    weighted_score=float(opp_data.get("weighted_score", 0)),
                    source_count=int(opp_data.get("source_count", 0)),
                    source_breakdown=opp_data.get("source_breakdown", {}),
                    problems=opp_data.get("problems", []),
                    jobs_to_be_done=opp_data.get("jobs_to_be_done", []),
                    solutions=opp_data.get("solutions", []),
                    next_steps=opp_data.get("next_steps", []),
                    contributing_patterns=opp_data.get("contributing_patterns", []),
                )
                outcome.opportunities.append(opp)

            result.desired_outcomes.append(outcome)

        for theme_data in data.get("cross_cutting_themes", []):
            theme = CrossCuttingTheme(
                name=theme_data.get("name", ""),
                description=theme_data.get("description", ""),
                source_percentage=float(theme_data.get("source_percentage", 0)),
                category_breakdown=theme_data.get("category_breakdown", {}),
            )
            result.cross_cutting_themes.append(theme)

        return result

    # ----- Helpers -----

    def _build_evidence_index(self, sources: list[Source]) -> list[dict]:
        """Build an evidence index grouping sources by category."""
        index = []
        for source in sources:
            index.append({
                "id": source.id,
                "filename": source.filename,
                "category": source.category,
                "category_label": INPUT_CATEGORIES.get(source.category, {}).get("label", source.category),
            })
        return index

    @staticmethod
    def _parse_json_response(raw: str, level_name: str):
        """Strip markdown fences and parse JSON from Claude's response."""
        cleaned = raw.strip()
        # Remove markdown code fences
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?\s*```\s*$", "", cleaned)
        cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise SynthesisError(f"Failed to parse {level_name} JSON response: {e}")
