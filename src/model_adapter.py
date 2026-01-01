from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
import time


@dataclass
class ModelOutput:
    text: str
    latency_s: float
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None


class TargetModelAdapter:
    """
    Provider-agnostic adapter.
    Replace generate() with your actual model call (OpenAI/Anthropic/local/etc).
    Keep proprietary prompts outside this public repo (e.g., in a private module).
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, case_inputs: Dict[str, Any], constraints: Dict[str, Any]) -> ModelOutput:
        start = time.time()

        # TODO: Replace with real model call.
        # For public repo safety: return a placeholder response.
        text = f"[PLACEHOLDER OUTPUT] task={constraints.get('style','')}"

        latency = time.time() - start
        return ModelOutput(text=text, latency_s=latency)
