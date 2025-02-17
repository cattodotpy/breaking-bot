from core.bot import DeckBot
from core.config import Config
import asyncio
import json
import dotenv

dotenv.load_dotenv()

CONFIG_FILE = "config.json"


async def main():
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    config = Config(**config)
    bot = DeckBot(config)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
