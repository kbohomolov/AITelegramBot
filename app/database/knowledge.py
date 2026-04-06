from sqlalchemy import select
from app.database.models import async_session, KnowledgeBase
from typing import List

async def get_knowledge_base() -> List[KnowledgeBase]:
    async with async_session() as session:
        result = await session.execute(select(KnowledgeBase))
        records = result.scalars().all()
        return records