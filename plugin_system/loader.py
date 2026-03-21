import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Type

from .base import Plugin
from .manager import PluginManager


class PluginLoader:
    """Discovers and loads Plugin subclasses from files or packages."""

    def __init__(self, manager: PluginManager) -> None:
        self._manager = manager

    def load_from_module(self, module_name: str) -> int:
        """Load all plugins from an importable module. Returns count loaded."""
        module = importlib.import_module(module_name)
        return self._register_from_module(module)

    def load_from_file(self, path: str | Path) -> int:
        """Load all plugins from a .py file. Returns count loaded."""
        path = Path(path)
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load module from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return self._register_from_module(module)

    def load_from_directory(self, directory: str | Path) -> int:
        """Load all plugins from every .py file in a directory. Returns count loaded."""
        directory = Path(directory)
        total = 0
        for py_file in sorted(directory.glob("*.py")):
            if not py_file.name.startswith("_"):
                total += self.load_from_file(py_file)
        return total

    def _register_from_module(self, module) -> int:
        count = 0
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Plugin) and obj is not Plugin and not inspect.isabstract(obj):
                self._manager.register(obj)
                count += 1
        return count
