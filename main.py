import uvicorn

from fastapi import FastAPI, Request, HTTPException

from loguru import logger

from classes.flashcards_session import FlashcardsSession
from classes.google_sheets_manager import GoogleSheetsManager
from funcs import get_session_id_or_401
from orm_models import UserSessionORM

app = FastAPI()
flashcard_session = FlashcardsSession()
sheets_manager = GoogleSheetsManager()

logger.add("logfile.log", level="DEBUG")


@app.post("/session/start")
async def start_session(request: Request):
	data = await request.json()
	session: UserSessionORM = flashcard_session.start_session(data["user_name"], data["deck_name"])
	session_id = session.id
	return {"session_id": session_id}


@app.get("/session/front")
async def show_front(request: Request):
	session_id = get_session_id_or_401(request, flashcard_session)
	card_front = flashcard_session.show_card_front(session_id)
	return {"card_front": card_front}


@app.get("/session/back")
async def show_back(request: Request):
	session_id = get_session_id_or_401(request, flashcard_session)
	card_back = flashcard_session.show_card_back(session_id)
	return {"card_back": card_back}


@app.post("/session/check_answer")
async def check_answer(request: Request):
	session_id = get_session_id_or_401(request, flashcard_session)
	data = await request.json()
	is_studied: bool = data["is_card_studied"]
	flashcard_session.know_or_repeat_active_card(session_id, is_studied)
	is_finished: bool = flashcard_session.get_session_by_id(session_id).is_finished
	return {"is_finished": is_finished}


@app.get("/session/finish")
async def finish_session_show_stats(request: Request):
	session_id = get_session_id_or_401(request, flashcard_session)
	stats = flashcard_session.get_statistics(session_id)
	return {**stats}


@app.get("/decks")
async def export_decks():
	decks = sheets_manager.deck_manager.fetch_all()
	spreadsheet = sheets_manager.connect_to_google_sheets("flashcards_data")
	decks_sheet = spreadsheet.worksheet("decks")
	decks_sheet.clear()
	decks_sheet.append_row(["id", "name", "description"])

	for deck in decks:
		decks_sheet.append_row([str(deck.id), str(deck.name), str(deck.description)])

	return {"status": "success", "message": "Data exported successfully"}


@app.get("/decks/names")
async def export_decks_names():
	decks_names: list[str] = flashcard_session.get_decks_names()
	return {"decks_names": decks_names}


@app.get("/decks/update")
async def import_decks():
	spreadsheet = sheets_manager.connect_to_google_sheets("flashcards_data")
	decks_sheet = spreadsheet.worksheet("decks")
	decks_data = decks_sheet.get_all_values()
	sheets_manager.update_decks_table(decks_data)
	return {"status": "success"}


@app.get("/cards")
async def export_cards():
	cards = sheets_manager.card_manager.fetch_all()

	spreadsheet = sheets_manager.connect_to_google_sheets("flashcards_data")
	cards_sheet = spreadsheet.worksheet("cards")
	cards_sheet.clear()
	cards_sheet.append_row(["id", "front", "back", "deck_id"])  # Заголовки

	for card in cards:
		cards_sheet.append_row([str(card.id), str(card.front), str(card.back), str(card.deck_id)])

	return {"status": "success", "message": "Data exported successfully"}


@app.get("/cards/update")
async def import_cards():
	spreadsheet = sheets_manager.connect_to_google_sheets("flashcards_data")
	cards_sheet = spreadsheet.worksheet("cards")
	cards_data = cards_sheet.get_all_values()
	sheets_manager.update_cards_table(cards_data)
	return {"status": "success"}


if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8001)