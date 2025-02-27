from fastapi import Request, HTTPException

from classes.flashcards_session import FlashcardsSession


def get_session_id_or_401(request: Request, flashcard_session: FlashcardsSession) -> int:
    """Извлекает session_id из заголовка Authorization и проверяет его валидность."""
    try:
        session_id = int(request.headers.get("Authorization", "").replace("Bearer ", ""))
    except (ValueError, AttributeError):
        raise HTTPException(status_code=401, detail="Invalid session token format")

    if not flashcard_session.session_exists(session_id):
        raise HTTPException(status_code=401, detail="Invalid session")

    return session_id
