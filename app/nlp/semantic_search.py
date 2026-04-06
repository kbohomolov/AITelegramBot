from sentence_transformers import SentenceTransformer, util
from app.database.knowledge import get_knowledge_base
from app.database.models import KnowledgeBase

model = SentenceTransformer('all-MiniLM-L6-v2')

async def find_best_answer(user_query: str) -> str:
    kb_records = await get_knowledge_base()
    if not kb_records:
        return "База знань порожня."

    questions = [rec.question for rec in kb_records]
    answers = [rec.answer for rec in kb_records]
    question_embeddings = model.encode(questions, convert_to_tensor=True)
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, question_embeddings)
    best_idx = scores.argmax()

    return answers[best_idx]