"""..."""

from typing import Dict, List
from types import ModuleType
from dataclasses import dataclass, field


@dataclass
class Dependencies:
    """..."""

    available_modules: List[str]
    imported_modules: Dict[str, ModuleType] = field(repr=False)
