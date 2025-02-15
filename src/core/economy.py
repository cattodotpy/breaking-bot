from typing import Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
import time

from core.user import User
from core.models import User as UserDocument


class Economy:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self.users: Dict[int, User] = {}

    async def create_user(self, user_id: int):
        doc = UserDocument(
            discord_id=user_id,
            balance=0.0,
            experience=0,
            level=0,
            created_at=int(time.time()),
        )
        await doc.insert()

        return doc

    async def get_user(self, user_id: int) -> User:
        if user_id in self.users:
            return self.users[user_id]

        user = await UserDocument.find_one(UserDocument.discord_id == user_id)
        if not user:
            user = await self.create_user(user_id)

        user = User(user)
        self.users[user_id] = user
        return user
