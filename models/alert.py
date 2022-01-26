import uuid
from typing import Dict
from dataclasses import dataclass, field

from libs.mailgun import Mailgun
from models.item import Item
from models.model import Model
from models.user import User

# using DATACLASS to remove __init__ functions
# dont need to call the super class super().__init the Dataclass does this
# superclass does not need to be a dataclass
# super().__ini just to get rid of a warning from the Model Class inheritance



@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default='Alerts')
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    # used because Dataclass can't access values in itself
    # self.item = Item.get_by_id(item_id) can't get the item_id
    # it runs after the initial __init__
    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "user_email": self.user_email,
            "price_limit": self.price_limit
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}.")
            print(Mailgun.send_mail(
                [self.user_email],
                f'Notification for {self.name}',
                f'Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address ti check your item: {self.item.url}.',
                f'<p> Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}.</p><p>Click <a href="{self.item.url}">here</a> to purchase your item. </p>.'
            ))



