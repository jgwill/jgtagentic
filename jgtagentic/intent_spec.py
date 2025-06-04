"""
📖🧠 IntentSpecParser — The Intent Mirror

Purpose: Parse `.jgtml-spec` YAML files to extract trading intent and signal definitions.
This is a minimal scaffold aligning with the Intent‑Driven Trading design.
"""

from typing import Any, Dict, List
import yaml


class IntentSpecParser:
    """Parse and transform intent specification files."""

    def load(self, path: str) -> Dict[str, Any]:
        """Load a YAML intent specification from ``path``."""
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data or {}

    def signals(self, spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return signal definitions from a loaded spec."""
        return spec.get("signals", [])
