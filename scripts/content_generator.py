#!/usr/bin/env python3
"""
Content generator orchestrator for Beyond the Code pipeline.
Handles topic selection, outline generation, critique loop, and PR creation.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

# Import our LLM client
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from llm_client import LLMClient

# Timeliness hooks for topic selection
TIMELINESS_HOOKS = {
    1: "Q1 - New year energy, layoffs season, job market anxiety",
    2: "Q1 - Layoffs continue, PIPs, job search season",
    3: "Q1 - Promotion cycle results, annual review fallout",
    4: "Q2 - Mid-year planning, spring energy, new projects",
    5: "Q2 - Promotion decisions, summer planning begins",
    6: "Q2 - Mid-year reviews, H1 reflections, summer slowdown starting",
    7: "Q3 - Summer slowdown, vacation coverage, quiet patterns",
    8: "Q3 - Back-to-work energy, H2 planning, new initiatives",
    9: "Q3 - Fall energy, Q4 prep, year-end push begins",
    10: "Q4 - Performance review prep, calibration season starts",
    11: "Q4 - Calibration meetings, stack ranking, promotion packets",
    12: "Q4 - Year-end reflections, holiday politics, planning for next year"
}


def load_topic_bank(data_dir: Path) -> dict:
    """Load the topic bank."""
    bank_path = data_dir / "topic_bank.json"
    if bank_path.exists():
        with open(bank_path, "r") as f:
            return json.load(f)
    return {"topics": [], "last_updated": None}


def save_topic_bank(data_dir: Path, bank: dict):
    """Save the topic bank."""
    bank_path = data_dir / "topic_bank.json"
    with open(bank_path, "w") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)


def select_topic(bank: dict, month: int) -> Optional[dict]:
    """
    Select the best unused topic from the bank.
    Considers score and timeliness.
    """
    unused = [t for t in bank.get("topics", []) if not t.get("used")]
    if not unused:
        return None

    # Get current timeliness context
    timeliness = TIMELINESS_HOOKS.get(month, "")

    # Score boost for timeliness match
    def adjusted_score(topic):
        base = topic.get("score", 0)
        timeliness_fit = topic.get("timeliness_fit", "").lower()
        boost = 10 if any(kw in timeliness.lower() for kw in timeliness_fit.split()) else 0
        return base + boost

    # Sort by adjusted score
    unused.sort(key=adjusted_score, reverse=True)
    return unused[0]


def load_prompt(prompt_name: str) -> str:
    """Load a prompt template."""
    prompt_path = script_dir / "prompts" / f"{prompt_name}.txt"
    with open(prompt_path, "r") as f:
        return f.read()


def generate_outline(client: LLMClient, topic: dict, timeliness: str) -> str:
    """Generate an outline using Claude."""
    prompt_template = load_prompt("outline")
    prompt = prompt_template.format(
        topic=topic["theme"],
        contrarian_angle=topic.get("contrarian_angle", ""),
        sources=", ".join(topic.get("sources", [])),
        timeliness=timeliness
    )

    return client.generate("outline_generation", prompt)


def critique_artifact(client: LLMClient, artifact_type: str, content: str) -> dict:
    """Critique an outline or draft using Gemini."""
    prompt_template = load_prompt("critique")
    prompt = prompt_template.format(
        artifact_type=artifact_type,
        content=content
    )

    response = client.generate("outline_critique" if artifact_type == "outline" else "draft_critique", prompt)

    # Parse JSON from response
    if "```json" in response:
        json_str = response.split("```json")[1].split("```")[0]
    elif "```" in response:
        json_str = response.split("```")[1].split("```")[0]
    else:
        json_str = response

    return json.loads(json_str.strip())


def generate_draft(client: LLMClient, outline: str, date_str: str) -> str:
    """Generate a full draft from the outline."""
    prompt_template = load_prompt("draft")
    prompt = prompt_template.format(
        outline=outline,
        date=date_str
    )

    return client.generate("draft_writing", prompt)


def apply_revisions(client: LLMClient, draft: str, critique: dict) -> str:
    """Apply critique feedback to revise the draft."""
    critical_issues = critique.get("critical_issues", [])
    minor_suggestions = critique.get("minor_suggestions", [])

    if not critical_issues and not minor_suggestions:
        return draft

    prompt = f"""Revise this blog post draft based on the following feedback:

## Current Draft
{draft}

## Critical Issues to Address
{json.dumps(critical_issues, indent=2)}

## Minor Suggestions (optional)
{json.dumps(minor_suggestions, indent=2)}

Apply the feedback while maintaining the voice and structure. Return the complete revised draft.
"""

    return client.generate("final_revision", prompt)


def generate_headlines(client: LLMClient, draft: str) -> list[str]:
    """Generate multiple headline options."""
    prompt = f"""Based on this blog post, generate 5 headline options:

{draft[:2000]}...

Generate headlines in these styles:
1. Curiosity hook - makes reader want to know more
2. Controversy hook - challenges assumption
3. Utility hook - promises value
4. Pattern-naming hook - introduces a named concept
5. Question hook - poses the central question

Return as a JSON list of strings:
```json
["Headline 1", "Headline 2", "Headline 3", "Headline 4", "Headline 5"]
```
"""

    response = client.generate("final_revision", prompt)

    if "```json" in response:
        json_str = response.split("```json")[1].split("```")[0]
    elif "```" in response:
        json_str = response.split("```")[1].split("```")[0]
    else:
        json_str = response

    return json.loads(json_str.strip())


def detect_series(draft: str, topic: dict) -> dict:
    """Detect if topic warrants a series treatment."""
    # Simple heuristic: long draft with multiple distinct angles
    word_count = len(draft.split())
    has_multiple_patterns = draft.count("##") > 5

    needs_series = word_count > 2500 or has_multiple_patterns

    return {
        "needs_series": needs_series,
        "word_count": word_count,
        "suggestion": "Consider splitting into a 2-3 part series" if needs_series else None
    }


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:60]


def create_pr(
    draft: str,
    headlines: list[str],
    topic: dict,
    series_info: dict,
    critique: dict
) -> str:
    """Create a GitHub PR with the draft."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Create slug from first headline
    slug = slugify(headlines[0] if headlines else topic["theme"])
    branch_name = f"beyondthecode/{today}-{slug}"

    # File path
    file_path = f"src/content/beyondthecode/{slug}.md"

    # Extract markdown content from draft
    if "```markdown" in draft:
        content = draft.split("```markdown")[1].split("```")[0]
    elif "```" in draft:
        content = draft.split("```")[1].split("```")[0]
    else:
        content = draft

    # Create branch
    subprocess.run(["git", "checkout", "-b", branch_name], check=True, capture_output=True)

    # Write file
    full_path = script_dir.parent / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content.strip())

    # Stage and commit
    subprocess.run(["git", "add", str(full_path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"Add Beyond the Code draft: {slug}"],
        check=True,
        capture_output=True
    )

    # Push branch
    subprocess.run(["git", "push", "-u", "origin", branch_name], check=True, capture_output=True)

    # Build PR description
    headline_options = "\n".join(f"- [ ] {h}" for h in headlines)

    pr_body = f"""## Beyond the Code Draft

**Topic:** {topic['theme']}

**Contrarian Angle:** {topic.get('contrarian_angle', 'N/A')}

### Headline Options (pick one)
{headline_options}

### Quality Scores
- Overall: {critique.get('overall_score', 'N/A')}/100
- Voice Consistency: {critique.get('scores', {}).get('voice_consistency', 'N/A')}/25
- Senior Resonance: {critique.get('scores', {}).get('senior_resonance', 'N/A')}/25
- Contrarian Strength: {critique.get('scores', {}).get('contrarian_strength', 'N/A')}/25

### Pull Quote Candidates
{chr(10).join('> ' + q for q in critique.get('pull_quote_candidates', []))}

### Series Detection
{series_info.get('suggestion', 'Single post - no series needed')}

### Source References
{', '.join(topic.get('sources', ['No sources tracked']))}

---
*Generated by Beyond the Code content pipeline*
"""

    # Create PR
    result = subprocess.run(
        ["gh", "pr", "create",
         "--title", f"[Draft] {headlines[0] if headlines else topic['theme']}",
         "--body", pr_body,
         "--draft"],
        check=True,
        capture_output=True,
        text=True
    )

    # Return to master
    subprocess.run(["git", "checkout", "master"], check=True, capture_output=True)

    # Extract PR URL from output
    pr_url = result.stdout.strip()
    return pr_url


def main():
    """Main orchestrator function."""
    today = datetime.now(timezone.utc)
    date_str = today.strftime("%Y-%m-%d")
    month = today.month
    timeliness = TIMELINESS_HOOKS.get(month, "")

    print("=== Beyond the Code Content Generator ===\n")

    # Setup paths
    data_dir = script_dir.parent / "data"
    client = LLMClient()

    # Step 1: Select topic
    print("Step 1: Selecting topic...")
    bank = load_topic_bank(data_dir)
    topic = select_topic(bank, month)

    if not topic:
        print("No unused topics in bank. Run topic_extractor.py first.")
        sys.exit(1)

    print(f"  Selected: {topic['theme']}")
    print(f"  Score: {topic.get('score', 'N/A')}")

    # Step 2: Generate outline
    print("\nStep 2: Generating outline...")
    outline = generate_outline(client, topic, timeliness)
    print("  Outline generated")

    # Step 3: Critique outline
    print("\nStep 3: Critiquing outline...")
    outline_critique = critique_artifact(client, "outline", outline)
    print(f"  Score: {outline_critique.get('overall_score', 'N/A')}/100")
    print(f"  Verdict: {outline_critique.get('verdict', 'N/A')}")

    if outline_critique.get("verdict") == "REJECT":
        print("  Outline rejected. Trying next topic...")
        # Mark topic as problematic and try again
        topic["used"] = True
        topic["rejection_reason"] = "Outline rejected by critique"
        save_topic_bank(data_dir, bank)
        sys.exit(1)

    # Step 4: Generate draft
    print("\nStep 4: Generating draft...")
    draft = generate_draft(client, outline, date_str)
    print(f"  Draft generated ({len(draft.split())} words)")

    # Step 5: Critique draft
    print("\nStep 5: Critiquing draft...")
    draft_critique = critique_artifact(client, "draft", draft)
    print(f"  Score: {draft_critique.get('overall_score', 'N/A')}/100")
    print(f"  Verdict: {draft_critique.get('verdict', 'N/A')}")

    # Step 6: Apply revisions if needed
    if draft_critique.get("verdict") in ["REVISE_MINOR", "REVISE_MAJOR"]:
        print("\nStep 6: Applying revisions...")
        draft = apply_revisions(client, draft, draft_critique)
        print("  Revisions applied")
    else:
        print("\nStep 6: No revisions needed")

    # Step 7: Generate headlines
    print("\nStep 7: Generating headline options...")
    headlines = generate_headlines(client, draft)
    print(f"  Generated {len(headlines)} headline options")
    for i, h in enumerate(headlines, 1):
        print(f"    {i}. {h}")

    # Step 8: Detect series potential
    print("\nStep 8: Checking series potential...")
    series_info = detect_series(draft, topic)
    if series_info["needs_series"]:
        print(f"  {series_info['suggestion']}")
    else:
        print("  Single post - no series needed")

    # Step 9: Create PR
    print("\nStep 9: Creating PR...")
    try:
        pr_url = create_pr(draft, headlines, topic, series_info, draft_critique)
        print(f"  PR created: {pr_url}")
    except subprocess.CalledProcessError as e:
        print(f"  Failed to create PR: {e}")
        print(f"  Stderr: {e.stderr}")
        sys.exit(1)

    # Step 10: Update topic bank
    print("\nStep 10: Updating topic bank...")
    topic["used"] = True
    topic["used_date"] = date_str
    topic["pr_url"] = pr_url
    save_topic_bank(data_dir, bank)
    print("  Topic marked as used")

    print("\n=== Generation Complete ===")
    print(f"PR URL: {pr_url}")
    print("\nNext steps:")
    print("1. Review the PR")
    print("2. Pick a headline and update the title")
    print("3. Edit the draft as needed")
    print("4. Mark as ready for review and merge")


if __name__ == "__main__":
    main()
