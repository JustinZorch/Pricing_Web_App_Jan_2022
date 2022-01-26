import re
from typing import Dict
import requests
from bs4 import BeautifulSoup
import uuid
from dataclasses import dataclass, field

from models.model import Model


# eq=False so objects can't be compared agaisnt each other
@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default='Items')
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        response = requests.get(self.url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        print(soup)
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d*\.\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }

    # "Item" is to signal you are returning an object of your current class
    # @classmethod
    # def get_by_id(cls,_id: str) -> "Item":
    ##maybe error here did it one line
    # return cls(** Database.find_one("Items", query={"_id" : _id}))
