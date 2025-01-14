import os

from dotenv import load_dotenv

from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


engine = create_async_engine(url=os.getenv('DB_URL'))
async_session =  async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)  
    registration_date: Mapped[DateTime] = mapped_column(DateTime)

class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)


async def async_main():
    load_dotenv()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)