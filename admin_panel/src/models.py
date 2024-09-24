from datetime import datetime

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata=MetaData()


class Base(DeclarativeBase):
    metadata = metadata


class Todo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, doc='Время обновления')
    done: Mapped[bool]
