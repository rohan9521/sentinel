from __future__ import annotations

import argparse
import json
from pathlib import Path

from sentinel.config import settings
from sentinel.data.synthetic import build_demo_dataset
from sentinel.service import SentinelService


def _generate_demo_data() -> None:
    cases = build_demo_dataset()
    output = Path("results/demo_cases.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps([case.case_id for case in cases], indent=2), encoding="utf-8")
    print(f"Wrote {len(cases)} demo cases to {output}")


def _show_status() -> None:
    service = SentinelService()
    print({
        "provider": settings.llm_provider,
        "offline_mode": settings.llm_provider == "fake",
        "max_usd": settings.max_usd,
        "example_cases": len(service.list_cases()),
    })


def main() -> None:
    parser = argparse.ArgumentParser(description="Sentinel CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("generate-data", help="Write a demo dataset to results/")
    subparsers.add_parser("health", help="Print basic backend health information")

    args = parser.parse_args()

    if args.command == "generate-data":
        _generate_demo_data()
    elif args.command == "health":
        _show_status()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
