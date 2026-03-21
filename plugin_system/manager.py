from typing import Type
from .base import Plugin


class PluginManager:
    """Registry and lifecycle manager for plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}
        self._active: set[str] = set()

    def register(self, plugin_class: Type[Plugin]) -> None:
        """Register a plugin class and activate it."""
        instance = plugin_class()
        name = instance.metadata.name
        if name in self._plugins:
            raise ValueError(f"Plugin '{name}' is already registered")
        self._plugins[name] = instance
        instance.activate()
        self._active.add(name)

    def unregister(self, name: str) -> None:
        """Deactivate and remove a plugin by name."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found")
        self._plugins[name].deactivate()
        self._active.discard(name)
        del self._plugins[name]

    def get(self, name: str) -> Plugin:
        """Return an active plugin by name."""
        if name not in self._active:
            raise KeyError(f"Plugin '{name}' is not active")
        return self._plugins[name]

    def list_plugins(self) -> list[dict]:
        """Return metadata for all registered plugins."""
        return [
            {
                "name": p.metadata.name,
                "version": p.metadata.version,
                "description": p.metadata.description,
                "active": p.metadata.name in self._active,
            }
            for p in self._plugins.values()
        ]
