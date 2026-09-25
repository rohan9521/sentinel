from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from sentinel.data.synthetic import build_demo_dataset
from sentinel.evaluation import EVALUATION_RESULTS_PATH, write_evaluation_results


def _run_generate_data() -> None:
    cases = build_demo_dataset()
    output = Path("results/demo_cases.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            [
                {
                    "case_id": case.case_id,
                    "account_id": case.account_id,
                    "merchant": case.transaction.merchant,
                    "amount": case.transaction.amount,
                    "label": case.label,
                    "timestamp": case.transaction.timestamp.isoformat(),
                }
                for case in cases
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Generated {len(cases)} demo cases -> {output}")


def _run_train() -> None:
    cases = build_demo_dataset()
    print(f"Training baseline on {len(cases)} demo cases using a deterministic scorer.")


def _run_eval() -> None:
    result = write_evaluation_results()
    print(json.dumps(asdict(result), indent=2))


def _run_report() -> None:
    path = EVALUATION_RESULTS_PATH
    if path.exists():
        result: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    else:
        result = asdict(write_evaluation_results())
    print(f"PR-AUC: {result['pr_auc']}")
    print(f"Recall@Precision 90%: {result['recall_at_precision_90']}")
    print(f"Precision@0.5: {result['precision_at_threshold']}")
    print(f"Recall@0.5: {result['recall_at_threshold']}")
    print("Latency and cost: unavailable (not measured)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sentinel evaluation CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(
        "generate-data",
        help="Generate a small synthetic dataset for demo and validation use",
    )
    subparsers.add_parser("train", help="Run a deterministic training stub for the demo baseline")
    subparsers.add_parser(
        "eval",
        help="Run the baseline evaluation and write a JSON result file",
    )
    subparsers.add_parser(
        "report",
        help="Render the evaluation summary from the demo results file",
    )

    args = parser.parse_args()
    if args.command == "generate-data":
        _run_generate_data()
    elif args.command == "train":
        _run_train()
    elif args.command == "eval":
        _run_eval()
    elif args.command == "report":
        _run_report()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
