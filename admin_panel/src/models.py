import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = sa.MetaData()


class Base(DeclarativeBase):
    metadata = metadata


class Templates(Base):
    __tablename__ = 'template'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, doc='Название шаблона')
    content: Mapped[str] = mapped_column(sa.Text, nullable=True, doc='Jinja шаблон')
