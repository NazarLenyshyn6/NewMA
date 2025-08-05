"""..."""

from typing import Dict, List
from types import ModuleType
from dataclasses import dataclass, field


@dataclass
class Dependencies:
    """..."""

    available_modules: List[str]
    imported_modules: Dict[str, ModuleType] = field(repr=False)

    def get_avaliable_modules(self) -> str:
        """..."""
        return ", ".join(module for module in self.available_modules)

    def get_imputed_modules(self) -> Dict[str, ModuleType]:
        return self.imported_modules
