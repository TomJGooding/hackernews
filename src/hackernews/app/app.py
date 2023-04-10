from textual.app import App, ComposeResult
from textual.widgets import Footer

from hackernews.app.widgets.custom_header import CustomHeader
from hackernews.app.widgets.hacker_news_table import HackerNewsTable

HEADER = "[b][bright_white][Y][/bright_white][grey0]Hacker News[/grey0][/b]"


class HackerNewsTUI(App):
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        yield CustomHeader(HEADER)
        yield HackerNewsTable()
        yield Footer()

    async def on_mount(self) -> None:
        table = self.query_one(HackerNewsTable)
        table.focus()


if __name__ == "__main__":
    app = HackerNewsTUI()
    app.run()
