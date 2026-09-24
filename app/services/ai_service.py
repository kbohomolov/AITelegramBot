from openrouter import OpenRouter
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))


async def get_ai_response(user_text: str, locale: str = "uk") -> str:
    try:
        system_prompt = (
            f"You are a helpful IT assistant.\n\n"

            f"Your task is to provide clear, structured, and practical answers to IT-related questions.\n\n"

            f"Guidelines:\n"
            f"- Start with a short definition\n"
            f"- Then explain in simple terms\n"
            f"- Add an example if relevant\n"
            f"- Use bullet points when helpful\n"
            f"- Keep answers concise (5-8 sentences max)\n"
            f"- When showing code, always wrap it in triple backticks ```\n"
            f"- Format code properly with indentation\n"
            f"- **Do NOT use ### headings**; use bold or bullet points instead\n\n"

            f"Avoid unnecessary complexity and focus on clarity.\n\n"

            f"IMPORTANT: Answer in {'Ukrainian' if locale == 'uk' else 'English'} language."
        )

        response = client.chat.send(
            model="openai/gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)
        return (
            "⚠️ Виникла помилка при зверненні до AI. Спробуйте пізніше."
            if locale == "uk"
            else "⚠️ An error occurred while contacting AI. Please try again later."
        )