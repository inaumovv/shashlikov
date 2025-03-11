from src.bot.utils.keyboards import Keyboards
from src.config import settings
from src.services.openai_worker import OpenAIWorker
from src.services.recognizer import Recognizer

openai_worker: OpenAIWorker = OpenAIWorker(
    'gpt-3.5-turbo',
    'user_history.json',
    settings.OPENAI_API_KEY,
    settings.OPENAI_ORGANIZATION,
    settings.OPENAI_PROJECT
)

recognizer: Recognizer = Recognizer()

keyboards: Keyboards = Keyboards()
