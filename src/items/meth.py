from core.objects.item import Item


class Meth(Item):
    def __init__(self, doc):
        super().__init__(doc)

    async def on_use(self, user):
        user.balance += 1000
        return user.balance