import discord
from discord.ext import commands
from typing import Dict
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie

from core.economy import Economy
from .models import MODELS
from .config import Config
import os

REQUIRED_ENVS = ["MONGO_URI", "BOT_TOKEN"]
COGS = ["cogs.profile", "cogs.trading", "jishaku", "cogs.developer"]


class BreakingBot(commands.Bot):
    db_client: AsyncIOMotorClient
    database: AsyncIOMotorDatabase
    config: Config
    env: Dict[str, str]
    economy: Economy

    def __init__(self, config: Config, *args, **kwargs):
        discord.utils.setup_logging()

        self.config = config
        self.env = self.get_env()

        super().__init__(
            command_prefix=config.prefix,
            intents=discord.Intents.all(),
            owner_ids=config.owner_ids,
            *args,
            **kwargs,
        )

    def get_env(self) -> Dict[str, str]:
        envs = {}
        for env in REQUIRED_ENVS:
            if env not in os.environ:
                raise ValueError(f"Missing required environment variable: {env}")

            envs[env] = os.environ[env]

        return envs

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        for cog in COGS:
            await self.load_extension(cog)

        print(f"Loaded { len(COGS)} cogs")

    async def connect_db(self):
        self.db_client = AsyncIOMotorClient(self.env["MONGO_URI"])
        self.database = self.db_client["breakingbot"]
        await init_beanie(self.database, document_models=MODELS)

        self.economy = Economy(self.database)

    async def start(self):
        await self.connect_db()
        await super().start(self.env["BOT_TOKEN"])
