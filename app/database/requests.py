from app.database.models import async_session
from app.database.models import User, Admin
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