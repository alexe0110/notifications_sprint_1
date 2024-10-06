import asyncio
import aiosmtplib
from email.message import EmailMessage
from .abstract import AbstractTransport
from config import settings


class EmailTransport(AbstractTransport):
    def __init__(self, server_conf: dict, credentials: dict, from_addr: str) -> None:
        self.from_addr = from_addr
        self.client = aiosmtplib.SMTP(**server_conf)
        self.credentials = credentials

    async def get_user_email(self, user_uuid: str):
        # тут должен быть поход в auth сервис за имейлом пользователя
        return settings.notification.mock_email_to

    async def send(self, user_ids: list[str], message: str):
        to_addrs = await asyncio.gather(*[
            self.get_user_email(user_id)
            for user_id in user_ids
        ])

        email = EmailMessage()
        email["From"] = self.from_addr
        email.add_alternative(message, subtype='html')

        await self.client.login(self.credentials['username'], self.credentials['password'])

        try:
            await self.client.sendmail(self.from_addr, to_addrs, email.as_string())
        except aiosmtplib.SMTPException as exc:
            reason = f'{type(exc).__name__}: {exc}'
            print(f'Не удалось отправить письмо. {reason}')
        finally:
            self.client.close()
