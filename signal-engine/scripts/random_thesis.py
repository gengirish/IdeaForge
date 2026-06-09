"""Pick a random thesis topic and write config/thesis_<slug>.yaml."""

from __future__ import annotations

import random
import sys
from pathlib import Path

TOPICS = [
    {
        "slug": "podcast_production",
        "name": "Podcast Production — indie creator dogfood",
        "vertical": "podcast_production",
        "icp_titles": [
            "Podcast Host",
            "Indie Creator",
            "Content Producer",
            "Newsletter + podcast founder",
        ],
        "problem": (
            "Indie podcasters waste hours on editing, show notes, and repurposing each episode. "
            "They need faster post-production without hiring a full-time editor."
        ),
        "keywords": [
            "podcast editing",
            "audio editing",
            "show notes",
            "transcription",
            "Descript",
            "Riverside",
            "podcast workflow",
            "clip repurposing",
        ],
        "disqualifiers": [
            "listener asking which mic to buy",
            "student media class assignment",
            "pure music production (not podcast)",
        ],
        "reddit_subs": ["podcasting", "podcasts", "NewTubers"],
        "reddit_kw": ["podcast editing", "audio editing", "show notes", "transcription", "Descript"],
        "hn_query": "podcast editing transcription audio production",
        "competitors": [
            ("Descript", "https://www.g2.com/products/descript/reviews"),
            ("Riverside.fm", "https://www.g2.com/products/riverside-fm/reviews"),
        ],
    },
    {
        "slug": "field_service",
        "name": "Field Service — HVAC/plumbing scheduling dogfood",
        "vertical": "field_service",
        "icp_titles": ["Operations Manager", "Service Company Owner", "Dispatch Lead"],
        "problem": (
            "Small field service businesses lose revenue to no-shows, double-booked techs, "
            "and phone-tag dispatch. They need reliable scheduling without enterprise FSM cost."
        ),
        "keywords": [
            "field service",
            "dispatch software",
            "HVAC scheduling",
            "no-show",
            "service technician",
            "route optimization",
            "Jobber",
            "ServiceTitan",
        ],
        "disqualifiers": [
            "homeowner DIY repair question",
            "job seeker asking how to become a tech",
        ],
        "reddit_subs": ["HVAC", "Plumbing", "smallbusiness"],
        "reddit_kw": ["dispatch", "scheduling", "no-show", "field service", "ServiceTitan"],
        "hn_query": "field service dispatch scheduling HVAC",
        "competitors": [
            ("Jobber", "https://www.g2.com/products/jobber/reviews"),
            ("ServiceTitan", "https://www.g2.com/products/servicetitan/reviews"),
        ],
    },
    {
        "slug": "creator_monetization",
        "name": "Creator Monetization — paid newsletter/community dogfood",
        "vertical": "creator_monetization",
        "icp_titles": [
            "Solo Creator",
            "Newsletter Writer",
            "Community Builder",
            "Indie Hacker",
        ],
        "problem": (
            "Creators with audiences struggle to launch paid tiers, reduce churn, "
            "and prove ROI on community tools without bolting together five products."
        ),
        "keywords": [
            "paid newsletter",
            "creator monetization",
            "Substack",
            "Patreon",
            "community churn",
            "membership",
            "Beehiiv",
            "Gumroad",
        ],
        "disqualifiers": [
            "consumer asking how to start a blog",
            "affiliate spam",
        ],
        "reddit_subs": ["Entrepreneur", "passive_income", "Blogging"],
        "reddit_kw": ["paid newsletter", "Patreon", "monetization", "Substack", "churn"],
        "hn_query": "creator newsletter monetization Substack Patreon",
        "competitors": [
            ("Substack", "https://www.g2.com/products/substack/reviews"),
            ("Patreon", "https://www.g2.com/products/patreon/reviews"),
        ],
    },
]


def write_thesis(topic: dict) -> Path:
    config_dir = Path(__file__).resolve().parents[1] / "config"
    path = config_dir / f"thesis_{topic['slug']}.yaml"
    lines: list[str] = [
        f'name: "{topic["name"]}"',
        f"vertical: {topic['vertical']}",
        "",
        "icp:",
        "  titles:",
        *[f'    - "{t}"' for t in topic["icp_titles"]],
        '  company_size: "solo to 50 employees"',
        '  industries: ["Creator economy", "SMB"]',
        '  geography: "US / remote-first"',
        "",
        "problem_hypothesis: >",
        f"  {topic['problem']}",
        "",
        "keywords:",
        *[f"  - {k}" for k in topic["keywords"]],
        "",
        "competitors:",
    ]
    for name, url in topic["competitors"]:
        lines.append(f"  - name: {name}")
        lines.append(f'    g2_url: "{url}"')
    lines.extend(
        [
            "",
            "disqualifiers:",
            *[f'  - "{d}"' for d in topic["disqualifiers"]],
            "",
            "kill_criteria:",
            '  - description: "Zero interview-worthy signals for 14 days"',
            "    threshold: 0",
            "    window_days: 14",
            "",
            "score_max_signals: 30",
            "",
            "sources:",
            "  reddit:",
            "    subreddits:",
            *[f"      - {s}" for s in topic["reddit_subs"]],
            "    keywords:",
            *[f"      - {k}" for k in topic["reddit_kw"]],
            "    days_back: 14",
            "    fallback_listing: true",
            "  hn:",
            f'    query: "{topic["hn_query"]}"',
            "    days_back: 30",
            "    tags: story,comment",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    topic = random.choice(TOPICS)
    path = write_thesis(topic)
    print(path)
    print(topic["name"])


if __name__ == "__main__":
    main()
