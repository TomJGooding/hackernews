from urllib.parse import urlparse

from rich.console import RenderableType
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Static

from hackernews.api import HackerNewsApi
from hackernews.models import Item

HEADER = "[b][bright_white][Y][/bright_white][grey0]Hacker News[/grey0][/b]"
COLUMN_HEADERS = ("Rank", "Score", "Title", "Site")


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


class HackerNewsTUI(App):
    CSS_PATH = "app.css"

    def compose(self) -> ComposeResult:
        yield CustomHeader(HEADER)
        yield DataTable(show_cursor=False)

    async def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*COLUMN_HEADERS)

        api = HackerNewsApi()
        top_stories = await api.get_top_stories_ids()
        top_30_stories = top_stories[:30]
        items: list[Item] = await api.get_multiple_items(top_30_stories)
        for rank, item in enumerate(items, start=1):
            title: str = item.title
            url: str | None = item.url

            if not url:
                url = f"https://news.ycombinator.com/item?id={item.id}"
                title = f"[link={url}]{title}[/]"
                site: str = ""
            else:
                title = f"[link={url}]{title}[/]"
                site = urlparse(url).netloc

            table.add_row(*(rank, item.score, title, site))


if __name__ == "__main__":
    app = HackerNewsTUI()
    app.run()
