# Sample run

```bash
python src/run_eval.py \
  --cases examples/synthetic_eval_cases.jsonl \
  --outdir reports/run_001 \
  --target_model "MODEL_X" \
  --judge_models "JUDGE_A,JUDGE_B"
```

Expected outputs:

* reports/run_001/results.csv
* reports/run_001/summary.md
* reports/run_001/charts/*.png
