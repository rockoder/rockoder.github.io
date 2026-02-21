#!/usr/bin/env python3
"""
Local runner for the Beyond the Code content pipeline.
Provides a unified interface to run scraping, topic extraction, and content generation.

Usage:
    # Run full pipeline (dry-run mode - no PR, no git changes)
    python scripts/run_pipeline.py --all --dry-run

    # Run only scrapers
    python scripts/run_pipeline.py --scrape

    # Run only topic extraction (requires scraped data)
    python scripts/run_pipeline.py --extract

    # Run only content generation (requires topics)
    python scripts/run_pipeline.py --generate --dry-run

    # Run full pipeline and create actual PR
    python scripts/run_pipeline.py --all
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from: {env_path}")
except ImportError:
    print("Note: python-dotenv not installed. Using system environment variables only.")
    print("      Install with: pip install python-dotenv")

SCRIPT_DIR = Path(__file__).parent


def check_env_vars():
    """Check and report on required environment variables."""
    required = {
        "LLM API (at least one)": [
            ("ANTHROPIC_API_KEY", "Claude API"),
            ("OPENAI_API_KEY", "OpenAI GPT"),
        ],
        "Reddit OAuth (for reddit scraper)": [
            ("REDDIT_CLIENT_ID", "Reddit OAuth client ID"),
            ("REDDIT_CLIENT_SECRET", "Reddit OAuth client secret"),
        ],
    }

    optional = {
        "GOOGLE_API_KEY": "Gemini API (used for critiques, free tier)",
        "GROQ_API_KEY": "Groq API (optional fallback)",
    }

    print("\n=== Environment Check ===\n")

    all_good = True

    # Check required groups
    for group_name, vars_list in required.items():
        group_ok = any(os.environ.get(var) for var, _ in vars_list)
        status = "OK" if group_ok else "MISSING"
        print(f"{group_name}: {status}")
        for var, desc in vars_list:
            present = "set" if os.environ.get(var) else "not set"
            print(f"  - {var}: {present}")
        if not group_ok:
            all_good = False

    print()

    # Check optional
    print("Optional:")
    for var, desc in optional.items():
        present = "set" if os.environ.get(var) else "not set"
        print(f"  - {var} ({desc}): {present}")

    print()

    if not all_good:
        print("WARNING: Some required environment variables are missing!")
        print("         Create a .env file from .env.example and fill in your keys.")
        print()

    return all_good


def run_script(script_name: str, args: list = None, continue_on_error: bool = True) -> bool:
    """Run a Python script and return success status."""
    script_path = SCRIPT_DIR / script_name
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n{script_name}: SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{script_name}: FAILED (exit code {e.returncode})")
        if not continue_on_error:
            sys.exit(1)
        return False


def check_data_exists(pattern: str) -> bool:
    """Check if data files matching pattern exist for today."""
    today = datetime.now().strftime("%Y-%m-%d")
    data_dir = SCRIPT_DIR.parent / "data"
    matches = list(data_dir.glob(f"*{today}*.json"))
    return len(matches) > 0


def check_topic_bank() -> tuple[bool, int]:
    """Check if topic bank exists and has unused topics."""
    bank_path = SCRIPT_DIR.parent / "data" / "topic_bank.json"
    if not bank_path.exists():
        return False, 0

    import json
    with open(bank_path) as f:
        bank = json.load(f)

    unused = [t for t in bank.get("topics", []) if not t.get("used")]
    return True, len(unused)


def main():
    parser = argparse.ArgumentParser(
        description="Run the Beyond the Code content pipeline locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test the full pipeline without creating PR
  python scripts/run_pipeline.py --all --dry-run

  # Run just the scrapers
  python scripts/run_pipeline.py --scrape

  # Generate content (requires existing topics)
  python scripts/run_pipeline.py --generate --dry-run
        """
    )

    # Stage selection
    parser.add_argument("--scrape", action="store_true", help="Run all scrapers (HN, Reddit, newsletters)")
    parser.add_argument("--extract", action="store_true", help="Run topic extraction")
    parser.add_argument("--generate", action="store_true", help="Run content generation")
    parser.add_argument("--all", action="store_true", help="Run full pipeline (scrape -> extract -> generate)")

    # Options
    parser.add_argument("--dry-run", action="store_true", help="Save draft locally instead of creating PR")
    parser.add_argument("--skip-topic-update", action="store_true", help="Don't mark topic as used")
    parser.add_argument("--check-env", action="store_true", help="Only check environment variables")
    parser.add_argument("--fail-fast", action="store_true",
                        help="Stop pipeline on first error (default: continue on error)")

    args = parser.parse_args()

    # Default to --all if no stage specified
    if not any([args.scrape, args.extract, args.generate, args.all, args.check_env]):
        print("No stage specified. Use --help for usage.")
        print("\nQuick start:")
        print("  python scripts/run_pipeline.py --all --dry-run  # Full pipeline test")
        sys.exit(1)

    # Check environment
    env_ok = check_env_vars()

    if args.check_env:
        sys.exit(0 if env_ok else 1)

    # Determine what to run
    run_scrape = args.scrape or args.all
    run_extract = args.extract or args.all
    run_generate = args.generate or args.all

    results = {"scrape": {}, "extract": False, "generate": False}

    # Stage 1: Scraping
    if run_scrape:
        print("\n" + "="*60)
        print("STAGE 1: SCRAPING")
        print("="*60)

        # Scrapers default to continue-on-error (one source failing shouldn't stop others)
        # But --fail-fast overrides this behavior
        scrape_continue = not args.fail_fast
        results["scrape"]["hn"] = run_script("hn_scraper_btc.py", continue_on_error=scrape_continue)
        results["scrape"]["reddit"] = run_script("reddit_scraper.py", continue_on_error=scrape_continue)
        results["scrape"]["newsletters"] = run_script("newsletter_monitor.py", continue_on_error=scrape_continue)

        success_count = sum(results["scrape"].values())
        print(f"\nScraping complete: {success_count}/3 sources succeeded")

    # Stage 2: Topic Extraction
    if run_extract:
        print("\n" + "="*60)
        print("STAGE 2: TOPIC EXTRACTION")
        print("="*60)

        results["extract"] = run_script("topic_extractor.py", continue_on_error=not args.fail_fast)

    # Stage 3: Content Generation
    if run_generate:
        print("\n" + "="*60)
        print("STAGE 3: CONTENT GENERATION")
        print("="*60)

        # Check prerequisites
        bank_exists, unused_count = check_topic_bank()
        if not bank_exists:
            print("\nERROR: No topic bank found. Run with --extract first.")
            if args.fail_fast:
                sys.exit(1)
        elif unused_count == 0:
            print("\nWARNING: No unused topics in bank. Consider running with --extract to add new topics.")
            if args.fail_fast:
                sys.exit(1)
        else:
            print(f"\nTopic bank has {unused_count} unused topic(s)")

            gen_args = []
            if args.dry_run:
                gen_args.append("--dry-run")
            if args.skip_topic_update:
                gen_args.append("--skip-topic-update")

            results["generate"] = run_script(
                "content_generator.py",
                args=gen_args if gen_args else None,
                continue_on_error=not args.fail_fast
            )

    # Summary
    print("\n" + "="*60)
    print("PIPELINE SUMMARY")
    print("="*60)

    if run_scrape:
        print(f"\nScraping:")
        for source, success in results["scrape"].items():
            status = "SUCCESS" if success else "FAILED"
            print(f"  - {source}: {status}")

    if run_extract:
        status = "SUCCESS" if results["extract"] else "FAILED"
        print(f"\nTopic Extraction: {status}")

    if run_generate:
        status = "SUCCESS" if results["generate"] else "FAILED/SKIPPED"
        print(f"\nContent Generation: {status}")
        if args.dry_run and results["generate"]:
            print(f"  Draft saved to: data/drafts/")

    print()


if __name__ == "__main__":
    main()
