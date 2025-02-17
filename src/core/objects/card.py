import json
import os

from attr import dataclass

CARDS_FILE = os.path.join(os.path.dirname(__file__), "../../data/cards.json")
CARDS = json.load(open(CARDS_FILE, "r"))["cards"]


@dataclass
class CardReward:
    amount: int
    item: str
    interval: int


class Card:
    def __init__(self, id: str):
        self.id = id
        self.name = CARDS[id]["name"]
        self.description = CARDS[id]["description"]
        self.rarity = CARDS[id]["rarity"]
        self.attack = CARDS[id]["attack"]
        self.defense = CARDS[id]["defense"]
        self.health = CARDS[id]["health"]
        self.reward = CardReward(**CARDS[id]["reward"])
        self.effects = CARDS[id]["effects"]
        self.cost = CARDS[id]["cost"]
        self.icon = CARDS[id]["icon"]

    def __repr__(self):
        return f"<Card {self.name=}, {self.rarity=}, {self.cost=}, {self.icon=}>"

    @staticmethod
    def get_card(id: str) -> "Card":
        return Card(id)

    @staticmethod
    def all_cards() -> list["Card"]:
        return [Card(id) for id in CARDS.keys()]

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "rarity": self.rarity,
            "attack": self.attack,
            "defense": self.defense,
            "health": self.health,
            "reward": self.reward,
            "effects": self.effects,
            "cost": self.cost,
            "icon": self.icon,
        }
