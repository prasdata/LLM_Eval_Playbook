from __future__ import annotations
import argparse
import os
import random
import sys
import logging
from typing import Dict, Any

import pandas as pd
from tqdm import tqdm

from data import load_cases_jsonl
from model_adapter import TargetModelAdapter
from judge_adapter import JudgeAdapter, JudgeConfig
from scoring import combine_two_judges
from report import write_reports

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def mask_model_identity() -> str:
    # simple blinded label
    return random.choice(["Model A", "Model B", "Model C"])


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--cases", required=True, help="Path to jsonl cases")
        parser.add_argument("--outdir", required=True, help="Output directory")
        parser.add_argument("--target_model", required=True, help="Target model name (blinded for judges)")
        parser.add_argument("--judge_models", required=True, help="Comma-separated judge model names (2 recommended)")
        args = parser.parse_args()

        logger.info(f"Starting evaluation with target model: {args.target_model}")
        logger.info(f"Judge models: {args.judge_models}")
        logger.info(f"Output directory: {args.outdir}")

        # Create output directory
        try:
            os.makedirs(args.outdir, exist_ok=True)
            logger.info(f"Created output directory: {args.outdir}")
        except Exception as e:
            logger.error(f"Failed to create output directory {args.outdir}: {e}")
            sys.exit(1)

        # Load cases
        try:
            cases = load_cases_jsonl(args.cases)
            logger.info(f"Loaded {len(cases)} test cases from {args.cases}")
        except FileNotFoundError:
            logger.error(f"Case file not found: {args.cases}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to load cases from {args.cases}: {e}")
            sys.exit(1)

        # Initialize adapters
        try:
            target = TargetModelAdapter(args.target_model)
        except Exception as e:
            logger.error(f"Failed to initialize target model adapter: {e}")
            sys.exit(1)

        judge_names = [x.strip() for x in args.judge_models.split(",") if x.strip()]
        if len(judge_names) < 2:
            logger.error("Provide at least 2 judge models for multi-judge mode.")
            sys.exit(1)

        try:
            judge1 = JudgeAdapter(JudgeConfig(model_name=judge_names[0]))
            judge2 = JudgeAdapter(JudgeConfig(model_name=judge_names[1]))
        except Exception as e:
            logger.error(f"Failed to initialize judge adapters: {e}")
            sys.exit(1)

        rows = []
        errors = 0

        for case in tqdm(cases, desc="Evaluating"):
            try:
                case_dict: Dict[str, Any] = {
                    "id": case.id,
                    "task_type": case.task_type,
                    "language": case.language,
                    "topic": case.topic,
                    "inputs": case.inputs,
                    "constraints": case.constraints,
                    "risk_tags": case.risk_tags,
                }

                # 1) Generate target output
                try:
                    out = target.generate(case.inputs, case.constraints)
                except Exception as e:
                    logger.warning(f"Failed to generate output for case {case.id}: {e}")
                    # Create error row
                    row = {
                        "case_id": case.id,
                        "task_type": case.task_type,
                        "language": case.language,
                        "topic": case.topic,
                        "target_model": args.target_model,
                        "judge_1": judge_names[0],
                        "judge_2": judge_names[1],
                        "latency_s": None,
                        "input_tokens": None,
                        "output_tokens": None,
                        "model_output": f"ERROR: {str(e)}",
                        "j1_notes": "Generation failed",
                        "j2_notes": "Generation failed",
                        "pass_instruction": None,
                        "pass_correctness": None,
                        "pass_safety": None,
                        "pass_style": None,
                        "pass_json": None,
                        "disagreement": None,
                    }
                    rows.append(row)
                    errors += 1
                    continue

                # 2) Judge with blinded identity
                try:
                    blinded = mask_model_identity()
                    j1 = judge1.judge(case_dict, out.text, blinded_label=blinded)
                    j2 = judge2.judge(case_dict, out.text, blinded_label=blinded)
                    combined = combine_two_judges(j1, j2)
                except Exception as e:
                    logger.warning(f"Failed to judge case {case.id}: {e}")
                    combined = {
                        "pass_instruction": None,
                        "pass_correctness": None,
                        "pass_safety": None,
                        "pass_style": None,
                        "pass_json": None,
                        "disagreement": None,
                    }
                    j1_notes = f"Judgment failed: {str(e)}"
                    j2_notes = f"Judgment failed: {str(e)}"
                    errors += 1

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
                    "j1_notes": getattr(j1, 'notes', 'N/A') if 'j1' in locals() else j1_notes,
                    "j2_notes": getattr(j2, 'notes', 'N/A') if 'j2' in locals() else j2_notes,
                    **combined,
                }
                rows.append(row)

            except Exception as e:
                logger.error(f"Unexpected error processing case {case.id}: {e}")
                errors += 1
                continue

        # Generate reports
        try:
            df = pd.DataFrame(rows)
            write_reports(df, args.outdir)
            logger.info(f"Generated reports in: {args.outdir}")
            logger.info(f"Total cases: {len(cases)}, Errors: {errors}")
            print(f"Done. Outputs in: {args.outdir}")
        except Exception as e:
            logger.error(f"Failed to generate reports: {e}")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Evaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
