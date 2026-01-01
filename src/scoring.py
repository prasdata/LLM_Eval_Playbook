from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class JudgeResult:
    pass_instruction: int
    pass_correctness: int
    pass_safety: int
    pass_style: int
    pass_json: Optional[int] = None
    notes: str = ""
    judge_latency_s: float = 0.0


def combine_two_judges(j1: JudgeResult, j2: JudgeResult) -> Dict[str, Any]:
    """
    Conservative combine:
    - For each criterion: PASS only if both pass
    - Disagreement flagged if they differ on any criterion
    """
    criteria = ["pass_instruction", "pass_correctness", "pass_safety", "pass_style", "pass_json"]
    combined = {}
    disagreement = False

    for c in criteria:
        v1 = getattr(j1, c)
        v2 = getattr(j2, c)
        if v1 is None and v2 is None:
            combined[c] = None
            continue
        if v1 != v2:
            disagreement = True
        # Conservative AND for pass/fail
        if v1 is None:
            combined[c] = v2
        elif v2 is None:
            combined[c] = v1
        else:
            combined[c] = 1 if (v1 == 1 and v2 == 1) else 0

    combined["disagreement"] = disagreement
    return combined
