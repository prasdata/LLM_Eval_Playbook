# LLM Eval Playbook (AI PM Edition)

A practical, **docs-first** playbook + minimal harness for **shipping LLM features** with:
- **bulk testing** across a wide scope (100s of real-world cases)
- **LLM-as-judge** with **human-defined pass/fail criteria**
- **human-in-the-loop calibration & qualitative feedback** (sampled)
- **multi-judge** setup to reduce judge drift and surface disagreements
- reporting that supports **fast iteration** + **release gating**

This repo is designed for **AI Product Managers** building real products (not benchmark chasing).

> Public-safe by design: includes templates, schemas, and a runnable harness.
> You plug in your own prompts + proprietary logic via adapters.

---

## Core principles

1) **Bulk scope beats anecdote**  
   Evaluate across a sufficiently wide slice of real, de-identified usage.

2) **Pass/Fail criteria for speed**  
   Define clear-cut checks (0/1) to enable fast iteration and release gates.

3) **LLM-as-judge, calibrated**  
   Use LLM judges to scale evaluation, and validate with sampled human review.

4) **Human-in-the-loop is not optional**  
   Humans define criteria, review samples, and add qualitative feedback.

5) **Multi-judge reduces false confidence**  
   Run two judges (or two passes) and surface disagreements for review.

---

## What this supports (example task types)

- **Human–AI conversation** (brainstorming, role-play, facilitation)
- **Natural language data analysis** (e.g., clustering qualitative responses)
- **Structured JSON generation** (consistent schema outputs for downstream systems)

Languages: **English, Malay, Chinese, Tamil** (extendable)

---

## Quick start

### Install
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
````

### Run a sample eval (synthetic dataset)

```bash
python src/run_eval.py \
  --cases examples/synthetic_eval_cases.jsonl \
  --outdir reports/run_001 \
  --target_model "YOUR_TARGET_MODEL" \
  --judge_models "JUDGE_MODEL_A,JUDGE_MODEL_B"
```

Outputs:

* `results.csv` (row-level)
* `summary.md` (pass rates, breakdowns)
* `charts/` (basic charts)

> Provider-agnostic: implement your own adapters in `src/model_adapter.py` and `src/judge_adapter.py`.

---

## Release gates (example)

Typical "ship/no-ship" checks (tune to your org & risk profile):

* Safety pass rate ≥ **0.98**
* Instruction-following pass rate ≥ **0.90**
* JSON validity pass rate ≥ **0.99** (for structured outputs)
* p95 latency ≤ **X sec** and cost within budget

See: `docs/06_release_gates.md`

---

## How to use this in a real product

1. Build a **coverage matrix** (tasks × risks × languages × topics)
2. Pull **100s of de-identified cases** from logs, stratified by topic
3. Write a **pass/fail rubric** and get humans to agree on it
4. Run bulk eval each iteration + compare against baseline
5. Sample cases for **human review** (random by topic + disagreements)
6. Track regressions + use release gates for launch readiness

---

## Files to start with

* Principles: `docs/01_principles.md`
* Coverage: `docs/02_coverage_matrix.md`
* Rubric: `docs/03_rubric_pass_fail.md`
* Multi-judge: `docs/04_llm_as_judge_multi.md`
* HITL protocol: `docs/05_hitl_protocol.md`
* Release gates: `docs/06_release_gates.md`
* Reporting: `docs/07_reporting.md`

---

## License

Apache-2.0 (see `LICENSE`).
