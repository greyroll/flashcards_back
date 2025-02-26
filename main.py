import uvicorn

from fastapi import FastAPI, Request, HTTPException

from classes.flashcards_session import FlashcardsSession
from funcs import get_valid_session_id
from orm_models import UserSession

app = FastAPI()
flashcard_session = FlashcardsSession()


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


uvicorn.run(app, host="127.0.0.1", port=8001)