import uuid
from abc import ABC
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

metadata = sa.MetaData()


class UUIDString(TypeDecorator, ABC):
    impl = PG_UUID(as_uuid=True)

    def process_bind_param(self, value, dialect) -> sa.UUID | None:
        if value == '':
            return None
        return value


class Base(DeclarativeBase):
    metadata = metadata


class Template(Base):
    __tablename__ = 'template'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)

    notifications: Mapped[list['Notification']] = relationship(back_populates='template')


class Notification(Base):
    __tablename__ = 'notification'

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    template_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), sa.ForeignKey('template.id'), nullable=False)
    content_id: Mapped[uuid.UUID | None] = mapped_column(UUIDString, nullable=True)
    content_value: Mapped[str] = mapped_column(sa.String, nullable=True)
    last_update: Mapped[sa.DateTime] = mapped_column(sa.DateTime, nullable=False, default=datetime.now)
    cron: Mapped[str] = mapped_column(sa.String, nullable=True)
    users: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=False)

    template: Mapped['Template'] = relationship(back_populates='notifications')
