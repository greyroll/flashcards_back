import uvicorn

from fastapi import FastAPI, Request, HTTPException, Header

from loguru import logger

from classes.auth_manager import AuthManager
from classes.flashcards_session import FlashcardsSession
from classes.google_sheets_manager import GoogleSheetsManager
from orm_models import UserSessionORM

app = FastAPI()
flashcard_session = FlashcardsSession()
sheets_manager = GoogleSheetsManager()

logger.add("logfile.log", level="DEBUG")


@app.post("/session/start")
async def start_session(request: Request, x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	data = await request.json()
	session: UserSessionORM = flashcard_session.start_session(data["user_name"], data["deck_name"])
	session_id = session.id
	return {"session_id": session_id}


@app.get("/session/front")
async def show_front(request: Request, x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	session_id = AuthManager.get_session_id_or_401(request, flashcard_session)
	card_front = flashcard_session.show_card_front(session_id)
	return {"card_front": card_front}


@app.get("/session/back")
async def show_back(request: Request, x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	session_id = AuthManager.get_session_id_or_401(request, flashcard_session)
	card_back = flashcard_session.show_card_back(session_id)
	return {"card_back": card_back}


@app.post("/session/check_answer")
async def check_answer(request: Request, x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	session_id = AuthManager.get_session_id_or_401(request, flashcard_session)
	data = await request.json()
	is_studied: bool = data["is_card_studied"]
	flashcard_session.know_or_repeat_active_card(session_id, is_studied)
	is_finished: bool = flashcard_session.get_session_by_id(session_id).is_finished
	return {"is_finished": is_finished}


@app.get("/session/finish")
async def finish_session_show_stats(request: Request, x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	session_id = AuthManager.get_session_id_or_401(request, flashcard_session)
	stats = flashcard_session.get_statistics(session_id)
	return {**stats}


@app.get("/decks/names")
async def export_decks_names(x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	decks_names: list[str] = flashcard_session.get_decks_names()
	return {"decks_names": decks_names}


@app.get("/decks")
async def export_decks(x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	sheets_manager.export_decks_to_google_sheets()
	return {"status": "success", "message": "Data exported successfully"}


@app.get("/decks/update")
async def import_decks(x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	sheets_manager.update_decks_table()
	return {"status": "success"}


@app.get("/cards")
async def export_cards(x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	sheets_manager.export_cards_to_google_sheets()
	return {"status": "success", "message": "Data exported successfully"}


@app.get("/cards/update")
async def import_cards(x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	sheets_manager.update_cards_table()
	return {"status": "success"}


@app.delete("/cards/delete/{card_id}")
async def delete_card(card_id: int, x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	if not sheets_manager.card_exists(card_id):
		raise HTTPException(status_code=404, detail="Card not found")
	sheets_manager.delete_card(card_id)
	return {"status": "success", "message": f"Card {card_id} deleted"}


@app.delete("/decks/delete/{deck_id}")
async def delete_deck(deck_id: int, x_api_key: str = Header()):
	AuthManager.validate_api_key_or_403(x_api_key)
	if not sheets_manager.deck_exists(deck_id):
		raise HTTPException(status_code=404, detail="Deck not found")
	sheets_manager.delete_deck(deck_id)
	return {"status": "success", "message": f"Deck {deck_id} deleted"}


if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8001)