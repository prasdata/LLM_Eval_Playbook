# Principles (AI PM)

## Bulk testing
- Aim for 100s of cases from de-identified logs
- Cover typical + edge + high-risk flows
- Track regressions across iterations

## Pass/fail rubrics
- Fast to interpret
- Easy to gate releases
- Force clarity on what "good" means

## LLM-as-judge, but calibrated
- Judges scale evaluation
- Humans keep it honest:
  - define criteria
  - review sampled outputs
  - adjust rubrics when judges drift

## Multi-judge
- Two judges reduce single-model bias
- Exposes ambiguous rubric areas
- Prioritizes cases for human review
