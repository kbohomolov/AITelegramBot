import os

from dotenv import load_dotenv

from sqlalchemy import BigInteger, String, DateTime, Boolean, Text
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
    language = mapped_column(String(5), default='uk', nullable=False)
    is_admin = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[Boolean] = mapped_column(Boolean, default=True, nullable=False)

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    keywords: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)