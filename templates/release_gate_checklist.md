# Release Gate Checklist (Template)

## Baseline
- Baseline run id:
- Target run id:
- Compared on same dataset? (Y/N)

## Gates (example thresholds)
- Safety pass rate ≥ 0.98  ✅/❌
- Instruction-following pass rate ≥ 0.90 ✅/❌
- Correctness/groundedness pass rate ≥ 0.90 ✅/❌
- Style consistency pass rate ≥ 0.90 ✅/❌
- JSON validity pass rate ≥ 0.99 (if applicable) ✅/❌
- Latency p95 ≤ ____ sec ✅/❌
- Cost per 100 cases ≤ ____ ✅/❌

## Disagreements & HITL
- Multi-judge disagreement rate ≤ ____ ✅/❌
- Human-reviewed sample size: ____ (random by topic)
- Major failure modes captured + mitigations filed ✅/❌

## Decision
- Ship ✅ / No-ship ❌ / Ship with constraints ⚠️
- Notes:
