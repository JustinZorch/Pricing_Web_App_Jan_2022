import uuid
import re
from typing import Dict
from dataclasses import  dataclass, field
from models.model import Model


@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="Stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _uid: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query,
            "_id": self._id
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by("name", store_name)

    #$regex allows to search with the url_prefix starting but could have more in the URL
    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)




