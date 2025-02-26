import uvicorn

from fastapi import FastAPI, Request, HTTPException

from classes.flashcards_session import FlashcardsSession
from classes.google_sheets_manager import GoogleSheetsManager
from funcs import get_valid_session_id
from orm_models import UserSession

app = FastAPI()
flashcard_session = FlashcardsSession()
flashcard_session.user_session_manager.create_all_tables()
sheets_manager = GoogleSheetsManager()


@app.get("/decks")
async def index():
	decks_names: list[str] = flashcard_session.get_decks_names()
	return {"decks_names": decks_names}


@app.post("/session/start")
async def start_session(request: Request):
	data = await request.json()
	session: UserSession = flashcard_session.start_session(data["user_name"], data["deck_name"])
	session_id = session.id
	return {"session_id": session_id}


@app.get("/session/front")
async def show_front(request: Request):
	session_id = get_valid_session_id(request, flashcard_session)
	card_front = flashcard_session.show_card_front(session_id)
	return {"card_front": card_front}


@app.get("/session/back")
async def show_back(request: Request):
	session_id = get_valid_session_id(request, flashcard_session)
	card_back = flashcard_session.show_card_back(session_id)
	return {"card_back": card_back}


@app.post("/session/check_answer")
async def check_answer(request: Request):
	session_id = get_valid_session_id(request, flashcard_session)
	data = await request.json()
	is_studied: bool = data["is_card_studied"]
	flashcard_session.know_or_repeat_active_card(session_id, is_studied)
	is_finished: bool = flashcard_session.get_session_by_id(session_id).is_finished
	return {"is_finished": is_finished}


@app.get("/session/finish")
async def finish_session_show_stats(request: Request):
	session_id = get_valid_session_id(request, flashcard_session)
	stats = flashcard_session.get_statistics(session_id)
	return {**stats}


@app.post("/cards/update")
async def update_card(request: Request):
	data = await request.json()
	card_id = data.get("id")
	front = data.get("front")
	back = data.get("back")
	deck_id = data.get("deck_id")

	if not front or not back or not deck_id:
		return {"status": "error", "message": "Missing required fields"}

	if sheets_manager.card_manager.fetch_by_id(card_id) is None:
		sheets_manager.add_card(card_id, front, back, deck_id)
	else:
		sheets_manager.update_card(card_id, front, back, deck_id)

	return {"status": "success"}

@app.get("/cards")
async def export_cards():
	cards = sheets_manager.card_manager.fetch_all()
	return {"cards": cards}

# uvicorn.run(app, host="127.0.0.1", port=8001)