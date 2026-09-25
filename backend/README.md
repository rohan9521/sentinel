# Sentinel backend

This package contains the Python service for the Sentinel fraud-triage demo. It is
designed to run offline and includes a deterministic heuristic scorer and a
synthetic data generator; it does not train or validate a production model.

## Evaluation

Run `uv run python -m sentinel.cli eval` from this directory to regenerate the
repository-root `results/baseline_demo.json`; evaluation and `/results` resolve
that same artifact independent of the current working directory. The reported
ranking/threshold metrics are descriptive statistics for the generated
synthetic cases only. They are not
evidence of model quality, and no quality claim is made. Synthetic labels are
randomly assigned; transaction memo text is generated independently of the
label. The scorer uses transaction features and never reads the target label.

Latency and per-case cost are `null` because this offline evaluation does not
measure either quantity. The `/results` API likewise returns unavailable
(`null`) values rather than illustrative measurements when values have not
been measured.
