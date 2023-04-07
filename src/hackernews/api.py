import asyncio
from typing import Any

import aiohttp

from hackernews.models import Item


class HackerNewsApi:
    BASE_URL: str = "https://hacker-news.firebaseio.com/v0/"

    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def __aenter__(self) -> aiohttp.ClientSession:
        return self._session

    async def __aexit__(self, *errs: Any) -> None:
        await self._session.close()

    async def get_top_stories_ids(self) -> dict:
        resource: str = "topstories.json"
        return await self._get(resource)

    async def get_item(self, id: int) -> Item:
        resource: str = f"item/{id}.json"
        data: dict = await self._get(resource)
        item: Item = Item.from_dict(data)
        return item

    async def get_multiple_items(self, item_ids: list[int]) -> list[Item]:
        tasks = []
        for id in item_ids:
            tasks.append(asyncio.ensure_future(self.get_item(id)))

        item_list = await asyncio.gather(*tasks)
        return item_list

    async def _get(self, resource: str) -> dict:
        data = dict()
        async with self._session.get(f"{self.BASE_URL}{resource}") as resp:
            try:
                data = await resp.json()
            except aiohttp.ContentTypeError as e:
                raise e

            return data
