from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class ModelParser(Generic[T]):

    def __init__(self, lines: str | None = None):
        self.lines: [str] = lines

    @abstractmethod
    def parse_from_file(self, filename: str) -> T:
        pass

    @abstractmethod
    def parse_from_string(self, content: str, new_line_ctrl: str = "\n") -> T:
        pass

    @abstractmethod
    def parse(self) -> T:
        pass

