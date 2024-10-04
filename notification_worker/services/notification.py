from jinja2 import Environment, BaseLoader, select_autoescape
from jinja2.exceptions import TemplateError
from transport.abstract import AbstractTransport
from logging import Logger
from schemas.notification import NotificationSchemaIn


class NotificationService():
    def __init__(self, transport: AbstractTransport, logger: Logger) -> None:
        self.transport = transport
        self.logger = logger
        self.env = Environment(loader=BaseLoader(), autoescape=select_autoescape())

    def _render_template(self, template: str, payload: dict):
        loaded_template = self.env.from_string(source=template)
        return loaded_template.render(payload)

    async def notify(self, raw_data: bytes):
        data = NotificationSchemaIn.model_validate_json(raw_data.decode('utf-8'))
        try:
            rendered_template = self._render_template(
                template=data.template_content,
                payload=data.payload_for_template
            )
        except TemplateError:
            self.logger.error('Invalid template')
            return

        await self.transport.send(data.user_ids, rendered_template)
