from __future__ import annotations


class LTLModel:
    def __init__(self, formula: str | None = None):
        self.formula: str = formula
