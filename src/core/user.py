import asyncio
from .models import User as UserDocument
from motor.motor_asyncio import AsyncIOMotorDatabase


class User:
    discord_id: int
    balance: float
    experience: int
    level: int
    created_at: int
    lock: asyncio.Lock
    doc: UserDocument

    def __init__(self, obj: UserDocument):
        self.discord_id = obj.discord_id
        self.balance = obj.balance
        self.experience = obj.experience
        self.level = obj.level
        self.created_at = obj.created_at
        self.lock = asyncio.Lock()  # Lock for user operations
        self.doc = obj

    def __repr__(self):
        return f"<User {self.discord_id=}, {self.balance=}, {self.experience=}, {self.level=}, {self.created_at=}>"

    def __eq__(self, other: "User"):
        return self.discord_id == other.discord_id

    def __hash__(self):
        return hash(self.discord_id)

    def to_dict(self):
        return {
            "discord_id": self.discord_id,
            "balance": self.balance,
            "experience": self.experience,
            "level": self.level,
            "created_at": self.created_at,
        }

    async def save(self):
        await self.doc.update(
            {
                "$set": self.to_dict(),
            }
        )

    async def add_balance(self, amount: float):
        self.balance += amount
        await self.save()

    async def remove_balance(self, amount: float):
        self.balance -= amount
        await self.save()

    async def add_experience(self, amount: int):
        self.experience += amount
        await self.save()

    async def add_level(self, amount: int):
        self.level += amount
        await self.save()
