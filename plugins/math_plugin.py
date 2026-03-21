from plugin_system import Plugin, PluginMetadata


class MathPlugin(Plugin):
    """Plugin that provides basic math operations."""

    metadata = PluginMetadata(
        name="math",
        version="1.0.0",
        description="Performs basic arithmetic operations",
    )

    def activate(self) -> None:
        print(f"[{self.metadata.name}] activated")

    def deactivate(self) -> None:
        print(f"[{self.metadata.name}] deactivated")

    def execute(self, operation: str, a: float, b: float) -> float:
        ops = {
            "add": a + b,
            "sub": a - b,
            "mul": a * b,
            "div": a / b,
        }
        if operation not in ops:
            raise ValueError(f"Unknown operation '{operation}'. Choose from: {list(ops)}")
        result = ops[operation]
        print(f"{a} {operation} {b} = {result}")
        return result
