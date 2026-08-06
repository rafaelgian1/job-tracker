from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_engine("postgresql+psycopg://postgres_user:postgres_password@localhost:5432/postgres_db", echo=True)


class Base(DeclarativeBase):
    pass