import requests


class HackerNewsApi:
    BASE_URL: str = "https://hacker-news.firebaseio.com/v0/"

    def get_top_stories(self) -> dict:
        resource: str = "topstories.json"
        return self._request(resource)

    def get_item(self, id: int) -> dict:
        resource: str = f"item/{id}.json"
        return self._request(resource)

    def _request(self, resource: str) -> dict:
        # TODO: handle this properly!
        data = dict()
        resp = requests.get(self.BASE_URL, resource)
        data = resp.json()
        return data
