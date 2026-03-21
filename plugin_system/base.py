from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PluginMetadata:
    name: str
    version: str
    description: str
    author: str = ""
    dependencies: list[str] = field(default_factory=list)


class Plugin(ABC):
    """Base class for all plugins."""

    metadata: PluginMetadata

    @abstractmethod
    def activate(self) -> None:
        """Called when the plugin is activated."""

    @abstractmethod
    def deactivate(self) -> None:
        """Called when the plugin is deactivated."""

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the plugin's main functionality."""
        raise NotImplementedError(f"Plugin '{self.metadata.name}' does not implement execute()")
