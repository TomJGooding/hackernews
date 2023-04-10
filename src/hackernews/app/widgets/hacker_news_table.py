import webbrowser
from typing import Any
from urllib.parse import urlparse

from textual.widgets import DataTable

from hackernews.api import HackerNewsApi
from hackernews.app.widgets.vi_like_datatable import ViLikeDataTable
from hackernews.models import Item


class HackerNewsTable(ViLikeDataTable):
    BINDINGS = [("enter", "select_cursor", "Open URL")]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._items: list[Item] = []

    async def _get_items(self) -> None:
        api = HackerNewsApi()
        top_stories = await api.get_top_stories_ids()
        top_30_stories = top_stories[:30]
        items: list[Item] = await api.get_multiple_items(top_30_stories)

        self._items = items

    async def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns(*("Rank", "Score", "Title", "Site"))

        await self._get_items()

        for rank, item in enumerate(self._items, start=1):
            title: str = item.title
            url: str | None = item.url
            comments_url = f"https://news.ycombinator.com/item?id={item.id}"

            if not url:
                title = f"[link={comments_url}]{title}[/]"
                site: str = ""
            else:
                title = f"[link={url}]{title}[/]"
                site = urlparse(url).netloc
                if site.startswith("www."):
                    site = site[4:]

            self.add_row(*(rank, item.score, title, site))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        selected_item: Item = self._items[event.cursor_row]
        if not selected_item.url:
            url = f"https://news.ycombinator.com/item?id={selected_item.id}"
        else:
            url = selected_item.url

        webbrowser.open(url)
