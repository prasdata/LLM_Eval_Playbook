from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class EvalCase:
    id: str
    task_type: str
    language: str
    topic: str
    inputs: Dict[str, Any]
    constraints: Dict[str, Any]
    risk_tags: List[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EvalCase":
        return EvalCase(
            id=d["id"],
            task_type=d["task_type"],
            language=d["language"],
            topic=d.get("topic", "unknown"),
            inputs=d["inputs"],
            constraints=d.get("constraints", {}),
            risk_tags=d.get("risk_tags", []),
        )


def load_cases_jsonl(path: str) -> List[EvalCase]:
    cases: List[EvalCase] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cases.append(EvalCase.from_dict(json.loads(line)))
    return cases
