import base64
import os
import json
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
API_KEY = os.getenv("API_KEY")


def get_google_credentials() -> dict:
	""" Декодирует ключ Google API из переменной окружения """
	credentials_base64 = os.getenv("GOOGLE_CREDENTIALS")
	if not credentials_base64:
		raise ValueError("GOOGLE_CREDENTIALS не найден в .env")

	decoded_credentials = base64.b64decode(credentials_base64).decode("utf-8")
	return json.loads(decoded_credentials)


GOOGLE_CREDENTIALS = get_google_credentials()
