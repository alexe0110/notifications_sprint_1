from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://app:qwe123@localhost:5432/notificationsdb')
