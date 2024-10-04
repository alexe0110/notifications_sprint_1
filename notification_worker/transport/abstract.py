from abc import ABC


class AbstractTransport(ABC):
    async def send(self, user_ids, message):
        raise NotImplementedError
