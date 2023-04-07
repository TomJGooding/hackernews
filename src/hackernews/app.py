from urllib.parse import urlparse

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header

from hackernews.api import HackerNewsApi

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
            item = api.get_item(id)
            score = item.get("score")
            title = item.get("title")
            url = item.get("url")
            site = ""

            if url:
                title = f"[link={url}]{title}[/]"
                site = urlparse(url).netloc

            table.add_row(*(rank, score, title, site))


if __name__ == "__main__":
    app = HackerNewsTUI()
    app.run()
