from typing import List
from beanie import Document, Indexed, Link


class Item(Document):
    item_id: str = Indexed(unique=True)
    name: str
    sellable: bool = False
    price: float | None = None
    effects: List[str] = []
    description: str
    tradable: bool = False
    created_at: int = 0
    icon: str | None = None


class User(Document):
    discord_id: int = Indexed(unique=True)
    balance: float = 0.0
    experience: int = 0
    level: int = 0
    inventory: List[Link[Item]] = []
    created_at: int = 0


MODELS = [User, Item]
