import os

from dotenv import load_dotenv

from sqlalchemy import BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


engine = create_async_engine(url=os.getenv('DB_URL'))
async_session =  async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    telegram_id = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100))  
    registration_date: Mapped[DateTime] = mapped_column(DateTime)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)

class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    telegram_id = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100))


async def async_main():
    load_dotenv()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)