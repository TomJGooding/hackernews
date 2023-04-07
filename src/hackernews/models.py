from dataclasses import dataclass


@dataclass
class Item:
    id: int
    type: str
    title: str
    url: str | None
    score: int

    @classmethod
    def from_dict(cls, d):
        id: int = d["id"]
        type: str = d["type"]
        title: str = d["title"]
        url: str | None = d.get("url")
        score: int = d["score"]

        return cls(id, type, title, url, score)
