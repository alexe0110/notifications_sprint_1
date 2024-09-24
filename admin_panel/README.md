# Admin panel



### Миграции

Автогенерация миграций

    alembic revision --autogenerate -m "Added new table"

Создать новую миграцию вручную

    alembic revision -m "create kek table"

Применить миграцию 

    alembic upgrade head