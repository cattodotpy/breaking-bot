from abc import ABC
from ..models import Item as ItemDocument


class Item(ABC):
    id: str
    name: str
    sellable: bool
    price: float | None
    effects: list[str]
    description: str
    tradable: bool
    created_at: int
    icon: str | None
    doc: ItemDocument

    def __init__(self, doc: ItemDocument):
        self.id = doc.item_id
        self.name = doc.name
        self.sellable = doc.sellable
        self.price = doc.price
        self.effects = doc.effects
        self.description = doc.description
        self.tradable = doc.tradable
        self.created_at = doc.created_at
        self.icon = doc.icon
        self.doc = doc

    def __repr__(self):
        return f"<Item {self.name=}, {self.price=}, {self.tradable=}>"

    def to_dict(self):
        return {
            "name": self.name,
            "sellable": self.sellable,
            "price": self.price,
            "effects": self.effects,
            "description": self.description,
            "tradable": self.tradable,
            "created_at": self.created_at,
        }

    def to_document(self):
        return ItemDocument(
            id=self.doc.id,
            name=self.name,
            sellable=self.sellable,
            price=self.price,
            effects=self.effects,
            description=self.description,
            tradable=self.tradable,
            created_at=self.created_at,
            icon=self.icon,
            item_id=self.id,
        )

    async def on_use(self, user):
        raise NotImplementedError("on_use method must be implemented in subclass")
