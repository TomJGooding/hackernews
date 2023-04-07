from urllib.parse import urlparse

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header

from hackernews.api import HackerNewsApi
from hackernews.models import Item

COLUMN_HEADERS = ("Rank", "Score", "Title", "Site")


class HackerNewsTUI(App):
    TITLE = "Hacker News"
    CSS_PATH = "app.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(show_cursor=False)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*COLUMN_HEADERS)

        api = HackerNewsApi()
        top_30_stories = api.get_top_stories()[:30]
        for rank, id in enumerate(top_30_stories, start=1):
            item: Item = api.get_item(id)

            title: str = item.title
            url: str | None = item.url
            site: str = ""

            if url:
                title = f"[link={url}]{title}[/]"
                site = urlparse(url).netloc

            table.add_row(*(rank, item.score, title, site))


if __name__ == "__main__":
    app = HackerNewsTUI()
    app.run()
