from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, List
import time

from .rubric import build_judge_prompt
from .scoring import JudgeResult


@dataclass
class JudgeConfig:
    model_name: str


class JudgeAdapter:
    """
    Provider-agnostic judge adapter.

    You can run multiple judges (different models or same model multiple passes)
    and surface disagreements for human review.
    """

    def __init__(self, config: JudgeConfig):
        self.config = config

    def judge(self, case: Dict[str, Any], model_output: str, blinded_label: str) -> JudgeResult:
        start = time.time()

        prompt = build_judge_prompt(
            case=case,
            model_output=model_output,
            blinded_label=blinded_label,
        )

        # TODO: Replace with real judge call. Must return JSON dict matching JudgeResult.
        # For now, placeholder "all pass".
        result = JudgeResult(
            pass_instruction=1,
            pass_correctness=1,
            pass_safety=1,
            pass_style=1,
            pass_json=1 if case.get("task_type") == "json_generation" else None,
            notes="PLACEHOLDER: implement judge call",
        )

        latency = time.time() - start
        result.judge_latency_s = latency
        return result
