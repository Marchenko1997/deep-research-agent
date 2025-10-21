# deep_research/__init__.py
import os
from dotenv import load_dotenv

# Загружаем .env из корня проекта
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path, override=True)

print("✅ .env preloaded successfully")
print(
    "🔑 OPENAI_API_KEY starts with:",
    os.getenv("OPENAI_API_KEY")[:10] if os.getenv("OPENAI_API_KEY") else "❌ None",
)
