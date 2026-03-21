from plugin_system import Plugin, PluginMetadata


class HelloPlugin(Plugin):
    """A simple greeting plugin."""

    metadata = PluginMetadata(
        name="hello",
        version="1.0.0",
        description="Greets the user by name",
    )

    def activate(self) -> None:
        print(f"[{self.metadata.name}] activated")

    def deactivate(self) -> None:
        print(f"[{self.metadata.name}] deactivated")

    def execute(self, name: str = "World") -> str:
        message = f"Hello, {name}!"
        print(message)
        return message
