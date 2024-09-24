from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


metadata = Base.metadata


class Todo(Base):
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    title2: Mapped[str] = mapped_column(default='kek', nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, doc='Время обновления')
    done: Mapped[bool]
