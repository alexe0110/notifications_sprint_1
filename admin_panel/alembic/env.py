from logging.config import fileConfig
from alembic import context
from src.models import metadata
from src.database import engine  # Импортируем движок из database.py

# это объект конфигурации Alembic, который предоставляет
# доступ к значениям в используемом .ini файле.
config = context.config

# Интерпретируем файл конфигурации для логирования.
# Эта строка настраивает логгирование.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Добавляем объект MetaData вашей модели сюда
# для поддержки 'autogenerate'
target_metadata = metadata


def run_migrations_offline() -> None:
    """Запускаем миграции в 'offline' режиме.

    Это конфигурирует контекст только с URL
    и без Engine, хотя Engine тоже допустим
    здесь. Пропуская создание Engine,
    нам даже не нужно доступное DBAPI.

    Вызовы к context.execute() здесь выводят
    данную строку на скрипт.
    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запускаем миграции в 'online' режиме.

    В этом сценарии нам нужно создать Engine
    и ассоциировать соединение с контекстом.
    """
    with engine.connect() as connection:  # Используем импортированный движок
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
