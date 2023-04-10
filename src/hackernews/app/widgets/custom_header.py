from rich.console import RenderableType
from textual.widgets import Static


class CustomHeader(Static):
    DEFAULT_CSS = """
        CustomHeader {
            dock: top;
            width: 100%;
            height: auto;
            content-align: center middle;
        }
    """

    def __init__(self, renderable: RenderableType = "") -> None:
        super().__init__(renderable)
