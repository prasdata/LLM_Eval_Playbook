# Release Gates

Release gates let you ship responsibly without freezing iteration.

Example thresholds (adjust to your context):
- Safety ≥ 0.98
- Instruction-following ≥ 0.90
- Correctness/groundedness ≥ 0.90
- Style consistency ≥ 0.90
- JSON validity ≥ 0.99 (if applicable)
- Disagreement rate ≤ 0.10 (or review disagreements)
- Latency p95 ≤ X sec

Always compare:
- baseline vs target
- same dataset
- same evaluation config
