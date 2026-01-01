# Multi-judge LLM-as-judge

Why multi-judge?
- reduces judge drift
- exposes ambiguous rubric areas
- prioritizes cases for human review

Default combine rule (conservative):
- PASS only if both judges PASS
- disagreement flag if any criterion differs

Human review priorities:
1) disagreements
2) safety failures
3) "near-miss" topics (known risky areas)
