# PRODUCT INSIGHT SYNTHESIZER
**Vision & Technical Specification**

**AI-Powered Multi-Source Synthesis for Strategic Product Decisions**

---

## 1. EXECUTIVE SUMMARY

**What It Is:**
A self-service tool that automatically synthesizes meeting transcripts, customer calls, CS tickets, and team discussions into evidence-based Opportunity Solution Trees.

**Core Problem It Solves:**
Product insights are scattered across dozens of meetings, hundreds of customer conversations, and thousands of support tickets. Nobody has time to manually synthesize them. Strategic decisions get made without comprehensive evidence because the synthesis work is too time-consuming.

**What Makes It Different:**
- Multi-source aggregation (not just meetings)
- Evidence-based synthesis (every claim traceable to source)
- Opportunity-first thinking (problems before solutions)
- Self-service (no data sharing required)
- Productized (tool, not consulting service)

**Primary Use Case:**
FleetEnergies PoC demonstrating how AI can compress product discovery from quarterly manual synthesis to on-demand strategic insights.

**Document Version:** 2.0 (Complete Revision)
**Created:** February 13, 2026
**Author:** Isaac Goldstein
**Status:** Ready to build

---

## 2. VISION

### 2.1 The Problem

**Senior Product Managers face a synthesis challenge at scale:**

**Scenario:**
- 50+ meetings per quarter (product planning, stakeholder alignment, team discussions)
- 100+ customer conversations (sales calls, CS calls, discovery interviews)
- 500+ support tickets
- Dozens of Slack threads with product feedback
- Multiple sources of market/competitive intelligence

**Current State:**
PMs manually synthesize insights quarterly (or never):
- Read through meeting notes
- Re-listen to customer calls
- Scan support tickets
- Try to remember what was said 6 weeks ago
- Manually connect patterns across sources
- **Time required: 2-3 weeks of focused work**
- **Frequency: Once per quarter (if lucky)**
- **Coverage: Maybe 20% of available sources**

**Result:**
- Strategic decisions made without comprehensive evidence
- Problems buried in support tickets never reach product roadmap
- Customer pain points mentioned in sales calls never connect to engineering discussions
- Opportunities identified too late (market already moved)
- PMs spend time synthesizing instead of strategizing

### 2.2 The Opportunity

**AI can now do what humans can't at scale:**
- Process 1000+ sources in minutes (not weeks)
- Identify cross-source patterns (same problem in meeting + ticket + call)
- Maintain perfect source attribution (evidence trails)
- Update continuously (not quarterly)
- Surface opportunities buried in noise

**But only if designed for product thinking:**
- Opportunity-first (problems before solutions)
- Evidence-based (traceable to sources)
- Outcome-oriented (maps to business goals)
- Framework-integrated (JTBD, OST, Teresa Torres methods)

### 2.3 The Solution

**Product Insight Synthesizer:**

A tool that takes scattered product signals and generates strategic Opportunity Solution Trees with complete evidence trails.

**Input:** Meeting transcripts, customer calls, CS tickets, team discussions
**Process:** Multi-source synthesis using data pyramid + RAG
**Output:** Opportunity Solution Tree with evidence attribution

**Value Proposition:**
"Turn 3 weeks of quarterly synthesis into 3 hours of on-demand strategic insight."

### 2.4 Why Now?

**Three forces converge:**

1. **AI Capability Threshold**
   - LLMs can now understand nuanced product discussions
   - Context windows large enough (200K tokens) for multi-source processing
   - Retrieval-augmented generation enables source attribution
   - Quality sufficient for strategic work (not just tactical automation)

2. **Market Maturity**
   - Tools like Earmark validate AI-powered PM productivity
   - Teresa Torres' Continuous Discovery framework widely adopted
   - Product teams understand Opportunity Solution Trees
   - "Just now possible" moment (podcast title was correct)

3. **Operational Pressure**
   - Product teams expected to move faster (FleetEnergies: 2-year window)
   - Data volume growing (more meetings, more customers, more tickets)
   - Remote work = everything is recorded (transcript availability)
   - Strategic synthesis bottleneck more acute

**This is the moment to build it.**

---

## 3. CORE PRINCIPLES

### 3.1 Self-Service First

**Not consulting:**
"Send me your transcripts, I'll analyze them"

**But product:**
"Here's a tool. Load your transcripts. Get results."

**Why:**
- No trust barrier (data stays private)
- Instant value (on-demand processing)
- Repeatable (use quarterly, monthly, weekly)
- Scalable (not limited by consultant hours)

### 3.2 Opportunity-First Thinking

**Not feature factory:**
"Customer requested X → Build X"

**But strategic synthesis:**
"Customer mentioned problem Y (which underlies request X) → Explore opportunity space → Consider solutions"

**Framework integration:**
- Teresa Torres: Desired Outcome → Opportunities → Solutions
- Clayton Christensen: Jobs-to-be-Done (not feature requests)
- Evidence-based: Every opportunity traceable to sources

### 3.3 Evidence Over Assumptions

**Every claim must be traceable:**
- "Deployment complexity mentioned 34 times" → Show 34 sources
- "Impacts enterprise deals" → Show which sales calls mentioned it
- "CS team overwhelmed" → Show support ticket frequency

**No synthesis without attribution.**

### 3.4 Multi-Source Aggregation

**Single-source tools already exist:**
- Earmark: Meetings → Deliverables
- Otter: Meetings → Transcripts + summaries
- Gong: Sales calls → insights

**Gap: Nobody connects dots across sources**
- Same problem mentioned in: meeting + customer call + support ticket
- Nobody sees the pattern because sources are siloed

**This tool bridges sources.**

### 3.5 Privacy-First Design

**Data never leaves user control:**
- Runs locally (Streamlit app on localhost)
- Or deployed privately (user's infrastructure)
- No data sent to external servers (except Claude API for processing)
- No storage (processes on-demand, downloads result)

**Critical for enterprise trust.**

---

## 4. USER EXPERIENCE

### 4.1 Target User: Senior Product Manager

**Profile:**
- Managing product at Series A/B company (20-100 people)
- Responsible for strategic direction, not just feature execution
- Drowning in meetings, customer feedback, and support requests
- Wants data-driven decisions but no time to synthesize
- Familiar with Opportunity Solution Trees (Teresa Torres reader)
- Technical enough to run local tools (can follow README)

**Example: Robbin at FleetEnergies**
- CEO managing product direction
- 60→30 team reduction (less bandwidth)
- 2-year window to productize (time pressure)
- Wants AI acceleration (explicitly stated)
- Needs to make strategic bets (can't build everything)

### 4.2 User Flow

**Step 1: Gather Sources (5 minutes)**
```
User exports/collects:
- Meeting transcripts from Zoom/Google Meet (last quarter)
- Customer call recordings from Gong (recent calls)
- CS tickets from Intercom (CSV export)
- Slack threads (copy-paste relevant discussions)
- Any other text sources (emails, documents, notes)
```

**Step 2: Upload to Tool (2 minutes)**
```
User opens Product Insight Synthesizer (web interface)

Interface shows:
┌─────────────────────────────────────────┐
│ Product Insight Synthesizer             │
├─────────────────────────────────────────┤
│                                         │
│  Drop files here or click to upload    │
│                                         │
│  Supported formats:                    │
│  • .txt (transcripts, notes)           │
│  • .csv (tickets, structured data)     │
│  • .docx (meeting notes)               │
│  • .pdf (documents)                     │
│                                         │
│  [Drop Zone]                            │
│                                         │
├─────────────────────────────────────────┤
│ Files uploaded: 47                      │
│ • 32 meeting transcripts               │
│ • 10 customer calls                     │
│ • 5 CS tickets                          │
│                                         │
│ [Configure Settings ▼]                  │
│   Desired Outcomes (optional):         │
│   □ Reduce onboarding time             │
│   □ Increase customer satisfaction     │
│   □ Improve product velocity           │
│                                         │
│ [Synthesize Insights] ← Main CTA       │
└─────────────────────────────────────────┘
```

**Step 3: Processing (3-5 minutes)**
```
System processes:

Progress indicator shows:
┌─────────────────────────────────────────┐
│ Synthesizing insights...                │
├─────────────────────────────────────────┤
│ ████████████░░░░░░░░░░░░░░░░ 45%       │
│                                         │
│ ✓ Loaded 47 sources                    │
│ ✓ Categorized content (Level 2)        │
│ → Identifying patterns (Level 3)        │
│   Mapping opportunities (Level 4)       │
│                                         │
│ Processing with:                        │
│ • Multi-source synthesis                │
│ • Cross-source pattern recognition      │
│ • Evidence aggregation                  │
│ • Opportunity-solution mapping          │
└─────────────────────────────────────────┘
```

**Step 4: Download Results (1 minute)**
```
Synthesis complete!

┌─────────────────────────────────────────┐
│ Results Ready                           │
├─────────────────────────────────────────┤
│ Generated Opportunity Solution Tree:    │
│                                         │
│ • 5 opportunity areas identified        │
│ • 3 desired outcomes mapped             │
│ • 127 problems/pain points extracted    │
│ • Evidence from 47 sources              │
│                                         │
│ [Download Markdown Report]              │
│ [Download PDF Report]                   │
│ [View in Browser]                       │
│                                         │
│ Preview:                                │
│ ┌─────────────────────────────────┐   │
│ │ DESIRED OUTCOME 1: Reduce       │   │
│ │ onboarding time by 50%          │   │
│ │                                 │   │
│ │ Opportunity: Manual Emissions   │   │
│ │ Calculation Bottleneck          │   │
│ │ Evidence: 12 sources            │   │
│ │ [Expand to see details...]      │   │
│ └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Step 5: Use Results (Ongoing)**
```
User reviews Opportunity Solution Tree:
- Identifies strategic priorities
- Validates with team/stakeholders
- Makes product decisions
- Tracks outcomes

Repeat process:
- Weekly: Add new meetings/calls
- Monthly: Full re-synthesis
- Quarterly: Strategic review
```

### 4.3 Total Time Investment

**Traditional quarterly synthesis:**
- 2-3 weeks of focused PM time
- Incomplete (maybe 20% of sources reviewed)
- Quarterly cadence (slow feedback)

**With Product Insight Synthesizer:**
- 10 minutes to upload sources
- 5 minutes processing time
- On-demand (any time, any frequency)
- Comprehensive (100% of sources processed)

**Time savings: 95%+ reduction in synthesis effort**

---

## 5. TECHNICAL ARCHITECTURE

### 5.1 Technology Stack

**Frontend:**
- Streamlit (Python web framework)
- Simple, clean UI
- File upload components
- Progress indicators
- Results display

**Backend:**
- Python 3.11+
- Anthropic Claude API (Sonnet 4.5 or Opus 4.6)
- Document processing libraries:
  - python-docx (Word docs)
  - PyPDF2 (PDFs)
  - pandas (CSV processing)

**Data Processing:**
- RAG-style source structuring (XML tags)
- Data pyramid synthesis levels
- Evidence attribution tracking
- Cross-source pattern recognition

**Deployment:**
- Local execution (primary): `streamlit run app.py`
- Optional cloud deployment: Streamlit Cloud / Vercel
- No database required (stateless processing)

**Privacy:**
- All processing happens in-memory
- No data persistence (optional local save)
- Claude API calls only (no other external services)
- User data never stored on servers

### 5.2 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                       │
│                     (Streamlit)                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  File Upload  →  Processing  →  Results Display        │
│                                                         │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ▼                            ▼
    ┌────────────────┐          ┌────────────────┐
    │  FILE PARSER   │          │ RESULT RENDERER│
    │                │          │                │
    │ • .txt → text  │          │ • Markdown     │
    │ • .csv → table │          │ • PDF export   │
    │ • .docx → text │          │ • Web preview  │
    │ • .pdf → text  │          │                │
    └────────┬───────┘          └────────────────┘
             │
             ▼
    ┌─────────────────────────────────────┐
    │      DATA PYRAMID PROCESSOR         │
    │                                     │
    │  Level 1: Raw Signal Ingestion     │
    │  Level 2: Categorization           │
    │  Level 3: Pattern Synthesis        │
    │  Level 4: Opportunity Mapping      │
    │                                     │
    └────────┬────────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────┐
    │        CLAUDE API LAYER             │
    │                                     │
    │  • RAG-style XML structuring        │
    │  • ReAct prompting                  │
    │  • Evidence attribution             │
    │  • Cross-source synthesis           │
    │                                     │
    └────────┬────────────────────────────┘
             │
             ▼
    ┌─────────────────────────────────────┐
    │      OUTPUT GENERATOR               │
    │                                     │
    │  • Opportunity Solution Tree        │
    │  • Evidence index                   │
    │  • Cross-cutting themes             │
    │  • Markdown/PDF formatting          │
    │                                     │
    └─────────────────────────────────────┘
```

### 5.3 Data Flow

**Phase 1: Ingestion**
```
User uploads files
    ↓
File parser extracts text
    ↓
Tag with metadata:
- Source type (meeting, call, ticket)
- Date
- Participants (if available)
- Original filename
    ↓
Store in memory as structured XML
```

**Phase 2: Data Pyramid Processing**

**Level 1: Raw Signals**
```xml
<sources>
  <meeting date="2025-01-15" type="product_planning">
    <participants>Robbin, Team</participants>
    <content>
      [Full meeting transcript]
    </content>
  </meeting>
  
  <customer_call date="2025-02-01" type="sales">
    <customer>Enterprise A</customer>
    <content>
      [Full call transcript]
    </content>
  </customer_call>
  
  <cs_ticket id="234" date="2025-01-20">
    <customer>Customer B</customer>
    <content>
      [Ticket details]
    </content>
  </cs_ticket>
</sources>
```

**Level 2: Categorization**
```
Prompt Claude to extract from each source:
- Problems mentioned
- Solutions requested
- Jobs-to-be-done
- Pain points
- Feature requests (note but don't prioritize)
- Desired outcomes
- Constraints

Output: Categorized content per source
```

**Level 3: Pattern Synthesis**
```
Prompt Claude to identify patterns across sources:
- Same problem mentioned in multiple sources?
- Frequency of mentions
- Severity indicators
- Business impact signals
- Cross-source validation

Output: Aggregated patterns with evidence
```

**Level 4: Opportunity Mapping**
```
Prompt Claude to map to OST structure:
- Desired outcomes (from user config or inferred)
- Opportunity spaces (problems clustered)
- Solution options (explore multiple approaches)
- Evidence trails (which sources support what)

Output: Complete Opportunity Solution Tree
```

**Phase 3: Output Generation**
```
Format as markdown:
- Opportunity Solution Tree structure
- Evidence index (source attribution)
- Cross-cutting themes
- Recommendations

Generate PDF version

Return to user
```

### 5.4 RAG Implementation (Simplified)

**Instead of full vector database:**

Use Claude's extended context window (200K tokens) with structured XML:

```python
def synthesize_sources(sources):
    """
    sources: List of parsed documents with metadata
    """
    
    # Structure sources with XML tags for retrieval
    structured_input = build_xml_structure(sources)
    
    # Multi-stage prompting (data pyramid levels)
    level_2 = categorize_sources(structured_input)
    level_3 = identify_patterns(level_2)
    level_4 = map_opportunities(level_3)
    
    return level_4

def build_xml_structure(sources):
    """Convert sources to XML with metadata for Claude"""
    xml = "<sources>\n"
    
    for source in sources:
        xml += f"<{source.type} "
        xml += f"date='{source.date}' "
        xml += f"id='{source.id}'>\n"
        xml += f"<content>{source.text}</content>\n"
        xml += f"</{source.type}>\n"
    
    xml += "</sources>"
    return xml
```

**Why this works:**
- Claude can semantically search within XML structure
- Source attribution maintained via XML tags
- No separate vector DB needed for PoC
- Can scale to real RAG later if needed

### 5.5 Prompt Engineering (ReAct Structure)

**Level 2 Prompt (Categorization):**
```
You are analyzing product signals from multiple sources to identify strategic opportunities.

Sources provided: {count} sources ({breakdown by type})

For EACH source, extract:

THOUGHT: What is being discussed in this source?
ACTION: Identify the key content
OBSERVATION: [Your categorization]

Extract:
- Problems mentioned (what's broken/painful)
- Jobs-to-be-done (what user is trying to accomplish)
- Requested solutions (specific asks - note but don't prioritize)
- Pain points (impact/severity)
- Desired outcomes (what success looks like)

Format each source as:

<source id="{id}" type="{type}" date="{date}">
  <problems>
    <problem severity="high/medium/low">
      [Description]
      <evidence>[Direct quote]</evidence>
    </problem>
  </problems>
  
  <jobs_to_be_done>
    <jtbd>
      When [situation], I want to [motivation], so I can [outcome]
    </jtbd>
  </jobs_to_be_done>
  
  <pain_points>
    <pain severity="high/medium/low">
      [Description]
    </pain>
  </pain_points>
</source>

Now process all {count} sources.
```

**Level 3 Prompt (Pattern Synthesis):**
```
You now have categorized content from {count} sources.

Identify PATTERNS across sources:

THOUGHT: What problems appear in multiple sources?
ACTION: Cross-reference sources
OBSERVATION: [Pattern identification]

For each pattern found:

<pattern>
  <name>[Short descriptive name]</name>
  <frequency>{number} sources mention this</frequency>
  <evidence>
    <source id="{id}" type="{type}" date="{date}">
      [Quote or summary]
    </source>
    [Repeat for all sources]
  </evidence>
  <severity>high/medium/low</severity>
  <business_impact>
    [What's the impact? Revenue? Churn? Efficiency?]
  </business_impact>
</pattern>

List ALL patterns you identify, even if only mentioned in 2-3 sources.
```

**Level 4 Prompt (Opportunity Mapping):**
```
You have identified {count} patterns across sources.

Now map these to an Opportunity Solution Tree structure following Teresa Torres' framework.

DESIRED OUTCOMES (provided by user or infer from patterns):
{outcomes if provided, else "Infer from patterns"}

For each desired outcome, identify:

OPPORTUNITY SPACES (problems/needs that affect this outcome)
  ↓
SOLUTION OPTIONS (multiple approaches to address opportunity)
  ↓
EVIDENCE (which sources support this opportunity)

Output format:

## DESIRED OUTCOME: {outcome statement}

### Opportunity: {Opportunity Name}
**Evidence:** {X} sources ({breakdown by type})
**Business Impact:** {description}

**Problems/Pain Points:**
- {problem 1} (Source: {type}, {date})
- {problem 2} (Source: {type}, {date})

**Jobs to be Done:**
- When {situation}, I need to {motivation}, so I can {outcome}

**Solution Options:**
1. {Solution approach 1}
   - Impact: {expected impact}
   - Effort: {estimated effort}
   - Evidence: {which sources suggest this}
   
2. {Solution approach 2}
   [...]

**Recommended Next Step:**
{What to validate with customers/stakeholders}

Generate complete Opportunity Solution Tree for all identified opportunities.
```

---

## 6. OUTPUT SPECIFICATION

### 6.1 Opportunity Solution Tree Format

**Generated markdown structure:**

```markdown
# Strategic Opportunity Solution Tree
**Generated from:** {X} sources ({breakdown})
**Period:** {date range from sources}
**Generated:** {timestamp}
**Tool:** Product Insight Synthesizer v1.0

---

## EXECUTIVE SUMMARY

**Key Findings:**
- {X} opportunity areas identified
- {Y} desired outcomes mapped
- {Z} problems/pain points extracted across sources
- {N} solution options explored

**Top Priorities:**
1. {Opportunity name} - {Impact} - {Evidence strength}
2. {Opportunity name} - {Impact} - {Evidence strength}
3. {Opportunity name} - {Impact} - {Evidence strength}

**Cross-Cutting Themes:**
- {Theme 1}: Mentioned in {X}% of sources
- {Theme 2}: Mentioned in {Y}% of sources

---

## DESIRED OUTCOME 1: {Outcome Statement}

### Opportunity Area: {Name}
**Evidence Strength:** HIGH/MEDIUM/LOW
**Sources:** {count} ({breakdown by type})
**Business Impact:** {description}

**Problems/Pain Points:**
1. "{Quote from source}" 
   - Source: Product Planning Meeting, Jan 15, 2025
   - Context: Discussion about onboarding process
   
2. "{Quote from source}"
   - Source: Customer Call - Enterprise A, Feb 1, 2025
   - Context: Customer feedback on setup experience
   
3. "{Quote from source}"
   - Source: CS Ticket #234, Jan 20, 2025
   - Context: Support request about feature X

[List all problems with evidence]

**Jobs to be Done:**
- When {situation}, I need to {motivation}, so I can {outcome}
  - Evidence: {which sources describe this job}
  
- When {situation}, I need to {motivation}, so I can {outcome}
  - Evidence: {which sources describe this job}

**Solution Options:**

**Option 1: {Solution Name}**
- **Description:** {what this solution does}
- **Expected Impact:** {quantified if possible}
  - Example: "Could reduce onboarding from 3 days to 3 hours"
- **Estimated Effort:** HIGH/MEDIUM/LOW
  - Context: {why this effort level}
- **Evidence:** 
  - {source 1} mentioned: "{quote}"
  - {source 2} suggested: "{quote}"
- **Risks:** {potential downsides or challenges}

**Option 2: {Solution Name}**
[Same structure]

**Option 3: {Solution Name}**
[Same structure]

**Recommended Priority:** {Which solution to pursue and why}

**Next Validation Steps:**
- [ ] Interview {X} customers about {specific hypothesis}
- [ ] Prototype {Y} to test {assumption}
- [ ] Analyze {Z} metric to validate {impact}

---

### Opportunity Area: {Name}
[Repeat structure for each opportunity under this outcome]

---

## DESIRED OUTCOME 2: {Outcome Statement}
[Repeat structure for each outcome]

---

## CROSS-CUTTING THEMES

**Theme 1: {Theme Name}**
- Mentioned in: {X}/{total} sources ({percentage}%)
- Pattern: {description of what this theme represents}
- Sources:
  - {type}: {count} mentions
  - {type}: {count} mentions
- Key insight: {what this tells us strategically}

**Theme 2: {Theme Name}**
[Same structure]

---

## EVIDENCE INDEX

All claims in this document are traceable to source materials.
Sources processed:

**Meetings ({count}):**
1. Product Planning, Jan 15, 2025 - {filename}
2. Team Discussion, Jan 20, 2025 - {filename}
[...]

**Customer Calls ({count}):**
1. Enterprise A Sales Call, Feb 1, 2025 - {filename}
2. Customer B Support Call, Feb 5, 2025 - {filename}
[...]

**CS Tickets ({count}):**
1. Ticket #234, Jan 20, 2025
2. Ticket #256, Jan 25, 2025
[...]

**Other Sources ({count}):**
[List any other source types]

---

## METHODOLOGY

**Synthesis Approach:**
This Opportunity Solution Tree was generated using:

1. **Multi-Source Aggregation**
   - {count} sources across {timeframe}
   - Types: {breakdown}
   
2. **Data Pyramid Processing**
   - Level 1: Raw signal ingestion
   - Level 2: Content categorization (problems, JTBD, pain points)
   - Level 3: Cross-source pattern identification
   - Level 4: Opportunity-solution mapping

3. **Framework Integration**
   - Jobs-to-be-Done (Clayton Christensen)
   - Opportunity Solution Trees (Teresa Torres)
   - Evidence-based synthesis

4. **AI Processing**
   - Tool: Product Insight Synthesizer v1.0
   - Model: Claude Sonnet 4.5 / Opus 4.6
   - Processing time: {duration}

**Limitations:**
- Based only on sources provided (does not include: {what's missing})
- Time period: {date range}
- Recommendations require validation with customers and stakeholders
- Strategic decisions should consider additional context: financial data, market research, competitive analysis

**Confidence Levels:**
- HIGH: Mentioned in 10+ sources with consistent messaging
- MEDIUM: Mentioned in 5-9 sources with general agreement
- LOW: Mentioned in 2-4 sources or conflicting signals

---

## RECOMMENDED ACTIONS

**Immediate (This Week):**
1. {Action based on highest-priority opportunity}
2. {Action based on second priority}

**Short-Term (This Month):**
1. {Validation activities for top opportunities}
2. {Additional discovery needed}

**Strategic (This Quarter):**
1. {Larger initiatives to address opportunity spaces}
2. {Organizational changes or resource allocation}

---

**Document generated by Product Insight Synthesizer**
**For questions or feedback: [contact info]**
```

### 6.2 Alternative Output Formats

**PDF Version:**
- Same content as markdown
- Formatted with clean typography
- Table of contents
- Hyperlinked evidence index

**JSON Export (Optional):**
```json
{
  "generated_at": "2026-02-13T14:30:00Z",
  "sources_processed": {
    "total": 47,
    "meetings": 32,
    "customer_calls": 10,
    "cs_tickets": 5
  },
  "desired_outcomes": [
    {
      "id": "outcome_1",
      "statement": "Reduce customer onboarding time by 50%",
      "opportunities": [
        {
          "id": "opp_1",
          "name": "Manual Emissions Calculation Bottleneck",
          "evidence_strength": "HIGH",
          "source_count": 12,
          "problems": [...],
          "jobs_to_be_done": [...],
          "solutions": [...]
        }
      ]
    }
  ],
  "themes": [...],
  "evidence_index": [...]
}
```

---

## 7. BUILD PLAN

### 7.1 Phase 1: Core Engine (Days 1-2)

**Goal:** Prove synthesis actually works

**Deliverables:**
- Python script for file parsing
- Claude API integration
- Data pyramid processing (all 4 levels)
- Basic markdown output generation

**Test with:**
- 5 dummy meeting transcripts (create fake product discussions)
- Verify output quality
- Iterate on prompts until synthesis is good

**Success criteria:**
- Can process 10 text files
- Generates coherent opportunity map
- Evidence attribution works

### 7.2 Phase 2: UI Layer (Days 3-4)

**Goal:** Make it usable (not just a script)

**Deliverables:**
- Streamlit app interface
- File upload component
- Progress indicators
- Results display
- Download buttons (markdown + PDF)

**Test with:**
- Dummy data from Phase 1
- Verify UX flow
- Polish interface

**Success criteria:**
- Non-technical user can run it
- Clear instructions
- Error handling

### 7.3 Phase 3: Polish & Package (Day 5)

**Goal:** Ship-ready PoC

**Deliverables:**
- README with setup instructions
- Example output (using dummy data)
- 2-minute demo video
- Deployment guide (local + optional cloud)

**Test with:**
- Fresh install on clean machine
- Follow README to verify it works
- Record demo video

**Success criteria:**
- Can send to Robbin with confidence
- Clear value demonstration
- Easy to try

### 7.4 Build Timeline

**Day 1 (Thursday):**
- Set up project structure
- Build file parsers (.txt, .csv, .docx, .pdf)
- Claude API integration
- Level 1-2 processing (ingestion + categorization)

**Day 2 (Friday):**
- Level 3-4 processing (patterns + opportunities)
- Markdown output generation
- Test with dummy data
- Iterate on prompt quality

**Day 3 (Saturday):**
- Streamlit UI build
- File upload component
- Processing workflow
- Results display

**Day 4 (Sunday):**
- PDF export
- Error handling
- UI polish
- Testing

**Day 5 (Monday):**
- README documentation
- Demo video creation
- Example output generation
- Package for delivery

**Ship:** Monday evening or Tuesday morning

---

## 8. SUCCESS METRICS

### 8.1 PoC Success (FleetEnergies)

**Primary Goal:** Robbin tries it and finds value

**Metrics:**
- Does he upload his data?
- Does he find insights he didn't know?
- Does he want to use it again?
- Does it influence his decision on working with you?

**Success Looks Like:**
"This is exactly what I meant by AI-accelerating product development. Let's talk about how to implement this at FleetEnergies."

### 8.2 Product Quality Metrics

**Synthesis Quality:**
- Are identified opportunities actually strategic?
- Is evidence attribution accurate?
- Do patterns reflect real cross-source signals?
- Are solutions thoughtful (not just feature requests)?

**Validation:**
- Show to 2-3 experienced PMs
- "Would you use this?" → Yes/No
- "Is output useful?" → Rate 1-10

### 8.3 Technical Performance

**Processing Speed:**
- 50 sources in < 5 minutes
- Real-time progress updates
- No crashes or errors

**Output Quality:**
- Markdown properly formatted
- PDF readable and professional
- Evidence links work

---

## 9. COMPETITIVE ANALYSIS

### 9.1 Direct Competitors

**Earmark (Meeting → Work):**
- **Their strength:** Meetings to deliverables (PRDs, specs)
- **Their gap:** Single source (just meetings)
- **Our differentiation:** Multi-source synthesis (meetings + calls + tickets)

**Dovetail (Research Repository):**
- **Their strength:** Store and tag research insights
- **Their gap:** Manual synthesis still required
- **Our differentiation:** Automatic cross-source pattern recognition

**Productboard AI:**
- **Their strength:** Product management platform with AI features
- **Their gap:** Requires buying full platform, AI is add-on
- **Our differentiation:** Standalone tool, synthesis-first design

### 9.2 Indirect Competitors

**Claude/ChatGPT (General AI):**
- **Their strength:** Can summarize individual meetings
- **Their gap:** No multi-source aggregation, no OST structure
- **Our differentiation:** Purpose-built for product synthesis

**Gong/Chorus (Sales Intelligence):**
- **Their strength:** Deep sales call analysis
- **Their gap:** Sales-only, doesn't connect to product/support
- **Our differentiation:** Cross-functional synthesis

### 9.3 Our Unique Position

**We're the only tool that:**
1. Synthesizes across multiple source types (meetings + calls + tickets)
2. Outputs Opportunity Solution Trees (not just summaries)
3. Maintains complete evidence attribution (traceable to sources)
4. Uses product frameworks (JTBD, Teresa Torres)
5. Self-service (no consulting required)
6. Privacy-first (local execution)

**Positioning:**
"Multi-source product synthesis. Turn scattered signals into strategic opportunity maps."

---

## 10. FUTURE ROADMAP

### 10.1 If PoC Succeeds

**V1.1 (Add Integrations):**
- Gong API (auto-import sales calls)
- Intercom API (auto-import CS tickets)
- Slack integration (monitor channels)
- Zoom/Google Meet auto-transcription

**V1.2 (Continuous Processing):**
- Weekly auto-synthesis
- Diff/change detection (what's new this week?)
- Trend analysis (is problem growing or shrinking?)

**V1.3 (Collaboration Features):**
- Share opportunity maps with team
- Comment/discussion threads
- Vote on priorities
- Track decisions

**V2.0 (Full Platform):**
- Multi-user accounts
- Historical tracking
- Custom frameworks
- API for integration

### 10.2 Business Model Evolution

**PoC (Now):**
- Free tool to demonstrate capability
- Position Isaac's consulting/fractional PM services

**V1 (If Demand):**
- Productized tool ($99-$299/month)
- Self-service for small teams
- Isaac focuses on strategic work (not building tools)

**V2 (Scale):**
- Enterprise tier ($999-$2999/month)
- Custom deployments
- Professional services
- Partner with Isaac for implementation

**Philosophy:**
Start with tool to demonstrate capability → Scale to product if demand exists → Use as lead gen for high-value consulting regardless

---

## 11. GO-TO-MARKET

### 11.1 FleetEnergies PoC

**Timeline:**
- Build: Feb 13-17 (5 days)
- Send to Robbin: Feb 18
- Follow-up: Feb 19-20
- Decision: End of week (Feb 21)

**Messaging:**
"Here's a tool I built to demonstrate AI-accelerated product development. Load your meeting transcripts and see what synthesis looks like. Your data stays private - nothing gets sent to me."

**Call to action:**
"If this resonates, let's talk about how we could work together - either as Head of Product building this into FleetEnergies' workflow, or as a consulting engagement where I help implement this approach."

### 11.2 Broader Market (If FleetEnergies Works)

**Target Audience:**
- Series A/B product leaders
- B2B SaaS in regulated industries
- 20-100 person companies
- Product-led growth companies

**Distribution:**
1. Product Hunt launch
2. LinkedIn posts (before/after examples)
3. Teresa Torres community
4. Lenny's Newsletter sponsorship
5. Product management Slack communities

**Positioning:**
"Turn 3 weeks of quarterly synthesis into 3 hours of on-demand insight. Multi-source product synthesis for strategic decisions."

---

## 12. RISKS & MITIGATIONS

### 12.1 Technical Risks

**Risk:** Claude API output quality inconsistent
**Mitigation:** 
- Test extensively with dummy data first
- Iterate on prompts until stable
- Add human review step in PoC
- Fall back to simpler extraction if complex synthesis fails

**Risk:** Processing takes too long (>10 min for 50 sources)
**Mitigation:**
- Batch processing
- Progressive results (show partial while processing)
- Optimize prompts for conciseness
- Use Sonnet 4.5 (faster) vs Opus 4.6 (slower but higher quality)

**Risk:** File parsing fails on various formats
**Mitigation:**
- Support limited formats initially (.txt, .csv)
- Clear error messages
- Graceful degradation (skip unparsable files)

### 12.2 Product Risks

**Risk:** Output is too generic / not actionable
**Mitigation:**
- Focus on evidence trails (specificity comes from quotes)
- Prompt for concrete examples
- Include "next validation steps" in every opportunity
- Test with real PM users before shipping

**Risk:** Robbin doesn't find value
**Mitigation:**
- Set expectations correctly (this is synthesis, not strategy)
- Emphasize time savings over insights
- Show before/after comparison
- Position as starting point (not final answer)

**Risk:** Privacy concerns prevent use
**Mitigation:**
- Local execution (data never leaves user machine)
- Clear documentation on data handling
- Option to self-host
- No cloud storage required

### 12.3 Market Risks

**Risk:** Market too small (only PMs at specific company stage)
**Mitigation:**
- Start with PoC (prove concept first)
- If valuable, expand target audience
- If not, use as Isaac's personal tool
- Either way, demonstrates capability

**Risk:** Competitors move faster
**Mitigation:**
- Speed to market (ship in 5 days)
- Focus on quality (better synthesis)
- Vertical focus (regulated industries)
- Personal brand (Isaac's domain expertise)

---

## 13. OPEN QUESTIONS

**To Validate:**
1. Will Robbin actually upload his data? (Trust/privacy concern)
2. Is Opportunity Solution Tree the right output format? (Or simpler?)
3. Should desired outcomes be user-configured or AI-inferred?
4. Is Streamlit UI sufficient or need web app?
5. Should we store processing history or stay stateless?

**To Decide:**
1. Which Claude model? (Sonnet 4.5 faster, Opus 4.6 better quality)
2. How much to show in progress indicator? (Transparency vs simplicity)
3. Include JSON export? (For programmatic use)
4. Add chat interface? (Ask questions about synthesis)
5. Support audio files directly? (Or require transcription first)

---

## 14. CONCLUSION

**Product Insight Synthesizer is:**
- **Focused:** Multi-source → Opportunity Solution Tree (one job, done well)
- **Fast:** 5-day build to working PoC
- **Valuable:** Solves real problem (synthesis at scale)
- **Differentiating:** Proves Isaac can ship, thinks strategically, uses AI effectively
- **Flexible:** Works as PoC, personal tool, or product

**Success looks like:**
Robbin tries it, finds value, wants to work together (consulting or full-time).

**Even if FleetEnergies doesn't work out:**
Tool demonstrates capability, reusable for other opportunities, valuable for Isaac's own PM work.

**Next step:**
Build it this week. Ship to Robbin by Monday.

---

**END OF SPECIFICATION**

---

**Document created:** February 13, 2026
**Version:** 2.0 (Complete revision from original Product Copilot concept)
**Status:** Ready to build
**Build start:** Thursday, February 13, 2026
**Target ship:** Monday, February 17, 2026
