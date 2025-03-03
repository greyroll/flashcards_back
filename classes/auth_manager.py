from fastapi import Request, HTTPException, Header
from classes.flashcards_session import FlashcardsSession
from config import API_KEY


class AuthManager:
	"""Класс для управления аутентификацией API-ключей и проверкой сессий"""

	X_API_KEY = API_KEY

	@staticmethod
	def validate_api_key_or_403(x_api_key: str = Header(None)):
		"""Проверяет, что переданный X-API-Key совпадает с ключом"""
		if x_api_key != AuthManager.X_API_KEY:
			raise HTTPException(status_code=403, detail="Invalid API Key")

	@staticmethod
	def get_session_id_or_401(request: Request, flashcard_session: FlashcardsSession) -> int:
		"""Извлекает session_id из заголовка Authorization и проверяет его валидность."""
		try:
			session_id = int(request.headers.get("Authorization", "").replace("Bearer ", ""))
		except (ValueError, AttributeError):
			raise HTTPException(status_code=401, detail="Invalid session token format")

		if not flashcard_session.session_exists(session_id):
			raise HTTPException(status_code=401, detail="Invalid session")

		return session_id
