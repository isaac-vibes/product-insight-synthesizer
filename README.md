# Product Insight Synthesizer

AI-powered tool that synthesizes multi-source product signals into Opportunity Solution Trees with interactive visualizations. Upload customer calls, support tickets, internal meetings, and other documents — get a structured strategic analysis showing where problems span across your organization.

## What It Does

1. **Upload** product signals across 5 weighted categories (customer calls, internal meetings, support tickets, other sources, miscellaneous)
2. **Synthesize** using a 4-level data pyramid powered by Claude Opus 4.6:
   - Level 1: Source ingestion and parsing
   - Level 2: Structured extraction (problems, JTBD, pain points)
   - Level 3: Cross-source pattern identification
   - Level 4: Opportunity-solution mapping
3. **Visualize** results as an interactive treemap and drill-down bar charts showing cross-organizational evidence
4. **Download** a full strategic report (Markdown or PDF)

## The "Aha" Moment

> "I knew that was a problem, but I didn't know it was a problem across so many levels of the org — and that working in one or two specific opportunity spaces would achieve the desired outcome."

The tool surfaces patterns that span multiple organizational levels — when customers, internal teams, and support all mention the same friction, that's the strongest signal for where to invest.

## Quick Start

```bash
# Clone and set up
git clone https://github.com/yourusername/product-insight-synthesizer.git
cd product-insight-synthesizer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run
streamlit run app.py
```

## Supported File Types

- `.txt` — Call transcripts, meeting notes, Slack exports
- `.csv` — Support ticket exports, survey data
- `.pdf` — Reports, documents
- `.docx` — Word documents

## Input Categories & Weights

| Category | Weight | Rationale |
|----------|--------|-----------|
| Customer-Facing Calls | 3.0x | Direct customer voice — highest signal |
| Internal Meetings | 2.0x | Strategic context and team perspective |
| Support Tickets | 1.5x | Quantifiable pain points at scale |
| Other Sources | 1.0x | Slack, emails, documents |
| Miscellaneous | 1.0x | Catch-all |

## Frameworks Used

- **Opportunity Solution Trees** (Teresa Torres) — structuring outcomes, opportunities, and solutions
- **Jobs-to-be-Done** (Clayton Christensen) — understanding what users are trying to accomplish

## Tech Stack

- **Frontend:** Streamlit
- **AI:** Claude Opus 4.6 (Anthropic API)
- **Visualization:** Plotly (treemap + grouped bar charts)
- **PDF:** fpdf2
- **Parsing:** python-docx, PyPDF2, pandas

## Sample Data

The `sample_data/` directory contains realistic test files for a fleet emissions SaaS company, spanning all 5 input categories with cross-organizational patterns to discover.

## License

MIT
