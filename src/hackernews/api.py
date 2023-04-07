import requests

from hackernews.models import Item


class HackerNewsApi:
    BASE_URL: str = "https://hacker-news.firebaseio.com/v0/"

    def get_top_stories(self) -> dict:
        resource: str = "topstories.json"
        return self._request(resource)

    def get_item(self, id: int) -> Item:
        resource: str = f"item/{id}.json"
        data: dict = self._request(resource)
        item: Item = Item.from_dict(data)
        return item

    def _request(self, resource: str) -> dict:
        # TODO: handle this properly!
        data = dict()
        resp = requests.get(f"{self.BASE_URL}{resource}")
        data = resp.json()
        return data
