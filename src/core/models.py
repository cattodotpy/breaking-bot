from beanie import Document, Indexed


class User(Document):
    discord_id: int = Indexed(unique=True)
    balance: float = 0.0
    experience: int = 0
    level: int = 0
    created_at: int = 0


MODELS = [User]
