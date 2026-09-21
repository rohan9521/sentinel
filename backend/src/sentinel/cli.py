from __future__ import annotations

import argparse
import json
from pathlib import Path

from sentinel.evaluation import evaluate_baseline_dataset, write_evaluation_results


def _run_eval() -> None:
    result = write_evaluation_results()
    print(json.dumps(result.__dict__, indent=2))


def _run_report() -> None:
    path = Path("results/baseline_demo.json")
    if not path.exists():
        result = write_evaluation_results()
    else:
        result = json.loads(path.read_text(encoding="utf-8"))
    print(f"PR-AUC: {result['pr_auc']}")
    print(f"Recall@Precision 90%: {result['recall_at_precision_90']}")
    print(f"Precision@0.5: {result['precision_at_threshold']}")
    print(f"Recall@0.5: {result['recall_at_threshold']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sentinel evaluation CLI")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("eval", help="Run the baseline evaluation and write a JSON result file")
    subparsers.add_parser("report", help="Render the evaluation summary from the demo results file")

    args = parser.parse_args()
    if args.command == "eval":
        _run_eval()
    elif args.command == "report":
        _run_report()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
