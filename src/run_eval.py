from __future__ import annotations
import argparse
import os
import random
from typing import Dict, Any

import pandas as pd
from tqdm import tqdm

from data import load_cases_jsonl
from model_adapter import TargetModelAdapter
from judge_adapter import JudgeAdapter, JudgeConfig
from scoring import combine_two_judges
from report import write_reports


def mask_model_identity() -> str:
    # simple blinded label
    return random.choice(["Model A", "Model B", "Model C"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True, help="Path to jsonl cases")
    parser.add_argument("--outdir", required=True, help="Output directory")
    parser.add_argument("--target_model", required=True, help="Target model name (blinded for judges)")
    parser.add_argument("--judge_models", required=True, help="Comma-separated judge model names (2 recommended)")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    cases = load_cases_jsonl(args.cases)
    target = TargetModelAdapter(args.target_model)

    judge_names = [x.strip() for x in args.judge_models.split(",") if x.strip()]
    if len(judge_names) < 2:
        raise ValueError("Provide at least 2 judge models for multi-judge mode.")

    judge1 = JudgeAdapter(JudgeConfig(model_name=judge_names[0]))
    judge2 = JudgeAdapter(JudgeConfig(model_name=judge_names[1]))

    rows = []

    for case in tqdm(cases, desc="Evaluating"):
        case_dict: Dict[str, Any] = {
            "id": case.id,
            "task_type": case.task_type,
            "language": case.language,
            "topic": case.topic,
            "inputs": case.inputs,
            "constraints": case.constraints,
            "risk_tags": case.risk_tags,
        }

        # 1) Generate target output (single API call style)
        out = target.generate(case.inputs, case.constraints)

        # 2) Judge with blinded identity
        blinded = mask_model_identity()
        j1 = judge1.judge(case_dict, out.text, blinded_label=blinded)
        j2 = judge2.judge(case_dict, out.text, blinded_label=blinded)

        combined = combine_two_judges(j1, j2)

        row = {
            "case_id": case.id,
            "task_type": case.task_type,
            "language": case.language,
            "topic": case.topic,
            "target_model": args.target_model,
            "judge_1": judge_names[0],
            "judge_2": judge_names[1],
            "latency_s": out.latency_s,
            "input_tokens": out.input_tokens,
            "output_tokens": out.output_tokens,
            "model_output": out.text,
            "j1_notes": j1.notes,
            "j2_notes": j2.notes,
            **combined,
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    write_reports(df, args.outdir)
    print(f"Done. Outputs in: {args.outdir}")


if __name__ == "__main__":
    main()
