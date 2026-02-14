"""Configuration constants for Product Insight Synthesizer."""

MODEL_ID = "claude-opus-4-6"
MAX_TOKENS_OUTPUT = 16384

# Input categories with display metadata and synthesis weights.
# Higher weight = more influence on pattern scoring and opportunity ranking.
INPUT_CATEGORIES = {
    "customer_calls": {
        "label": "Customer-Facing Calls",
        "description": "Sales calls, discovery calls, CS calls — direct customer voice",
        "weight": 3.0,
        "icon": "📞",
        "color": "#2ecc71",
    },
    "internal_meetings": {
        "label": "Internal Meetings",
        "description": "Planning, retros, standups, strategy sessions",
        "weight": 2.0,
        "icon": "👥",
        "color": "#3498db",
    },
    "support_tickets": {
        "label": "Support Tickets",
        "description": "CS tickets, bug reports, feature requests",
        "weight": 1.5,
        "icon": "🎫",
        "color": "#e67e22",
    },
    "other_sources": {
        "label": "Other Sources",
        "description": "Slack threads, emails, documents",
        "weight": 1.0,
        "icon": "💬",
        "color": "#9b59b6",
    },
    "miscellaneous": {
        "label": "Miscellaneous",
        "description": "Catch-all for anything else",
        "weight": 1.0,
        "icon": "📄",
        "color": "#95a5a6",
    },
}

SUPPORTED_EXTENSIONS = ["txt", "docx", "pdf", "csv"]

MAX_DESIRED_OUTCOMES = 3

# Token budget per source (rough: 4 chars ≈ 1 token)
MAX_CHARS_PER_SOURCE = 16000  # ~4000 tokens

# Total token budget before batching kicks in
MAX_TOTAL_CHARS = 600000  # ~150K tokens

CATEGORY_COLORS = {k: v["color"] for k, v in INPUT_CATEGORIES.items()}
CATEGORY_LABELS = {k: v["label"] for k, v in INPUT_CATEGORIES.items()}
