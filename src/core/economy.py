from typing import Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
import time

from core.objects.item import Item
from core.objects.user import User
from core.models import Item as ItemDocument, User as UserDocument


class Economy:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self.users: Dict[int, User] = {}

    async def get_user_document(self, user_id: int) -> UserDocument:
        return await UserDocument.find_one(
            UserDocument.discord_id == user_id, fetch_links=True
        )

    async def create_user(self, user_id: int):
        doc = UserDocument(
            discord_id=user_id,
            balance=0.0,
            experience=0,
            level=0,
            created_at=int(time.time()),
            items=[],
        )
        await doc.insert()

        return await self.get_user_document(user_id)

    async def get_user(self, user_id: int) -> User:
        if user_id in self.users:
            return self.users[user_id]

        user = await self.get_user_document(user_id)
        if not user:
            user = await self.create_user(user_id)

        user = User(user)
        self.users[user_id] = user
        return user

    def dump(self):
        self.users = {}

    async def create_item(
        self, id: str, item_name: str, description: str | None = None
    ):
        doc = ItemDocument(
            item_id=id,
            name=item_name,
            sellable=False,
            price=None,
            effects=[],
            description=description or item_name,
            tradable=False,
            created_at=int(time.time()),
            icon=None,
        )
        await doc.insert()

        return doc

    async def get_item(self, item_id: str) -> ItemDocument | None:
        item_doc = await ItemDocument.find_one(ItemDocument.item_id == item_id)
        if not item_doc:
            return None
        return Item(item_doc)
