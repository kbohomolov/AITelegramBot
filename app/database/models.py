import os

from dotenv import load_dotenv

from sqlalchemy import BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


load_dotenv()

engine = create_async_engine(url=os.getenv('DB_URL'))
async_session =  async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    telegram_id = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(100))  
    registration_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    language = mapped_column(String(20), default='ukrainian', nullable=False)
    ai_model = mapped_column(String(50), default='Mistral AI', nullable=False)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)