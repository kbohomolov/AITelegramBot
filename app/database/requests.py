from app.database.models import async_session, User
from sqlalchemy import select


async def add_user(telegram_id, username, registration_date, is_admin):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))

        if not user:
            new_user = User(
                telegram_id=telegram_id,
                username=username or 'None',
                registration_date=registration_date,
                is_admin=is_admin
            )
            session.add(new_user)
            await session.commit()
        return user

async def update_user_language(telegram_id: int, language: str) -> bool:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user_language = user.scalar_one_or_none()
        if user_language:
            user_language.language = language
            await session.commit()
            return True
        return False

async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user_information = user.scalar_one_or_none()
        return user_information


async def activate_user(telegram_id: int) -> bool:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user_information = user.scalar_one_or_none()
        if user_information:
            user_information.is_active = True
            await session.commit()
            return True
        return False

async def deactivate_user(telegram_id: int) -> bool:
    async with async_session() as session:
        user = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user_information = user.scalar_one_or_none()
        if user_information:
            user_information.is_active = False
            await session.commit()
            return True
        return False
