import uvicorn

from fastapi import FastAPI, Request, HTTPException

from classes.flashcards_session import FlashcardsSession

app = FastAPI()
flashcard_session = FlashcardsSession()


@app.get("/decks")
async def index():
	decks_names: list[str] = flashcard_session.get_decks_names()
	return {"decks_names": decks_names}


@app.post("/session/start")
async def start_session(request: Request):
	data = await request.json()
	flashcard_session.start_session(data["user_name"], data["deck_name"])
	session_id = flashcard_session.session.id
	return {"session_id": session_id}


@app.get("/session/front")
async def show_front(request: Request):
	session_id = int(request.headers.get("Authorization").replace("Bearer ", ""))
	if flashcard_session.session_exists(session_id) is False:
		return HTTPException(status_code=401, detail="Invalid session")
	flashcard_session.continue_session(session_id)
	card_front = flashcard_session.show_card_front()
	return {"card_front": card_front}


@app.get("/session/back")
async def show_back(request: Request):
	session_id = int(request.headers.get("Authorization").replace("Bearer ", ""))
	if flashcard_session.session_exists(session_id) is False:
		return HTTPException(status_code=401, detail="Invalid session")
	flashcard_session.continue_session(session_id)
	card_back = flashcard_session.show_card_back()
	return {"card_back": card_back}


@app.post("/session/check_answer")
async def check_answer(request: Request):
	session_id = int(request.headers.get("Authorization").replace("Bearer ", ""))
	if flashcard_session.session_exists(session_id) is False:
		return HTTPException(status_code=401, detail="Invalid session")
	data = await request.json()
	is_studied: bool = data["is_card_studied"]
	flashcard_session.continue_session(session_id)
	flashcard_session.know_or_repeat_active_card(is_studied)
	return {"is_finished": flashcard_session.session.is_finished}


@app.get("/session/finish")
async def finish_session_show_stats(request: Request):
	session_id = int(request.headers.get("Authorization").replace("Bearer ", ""))
	if flashcard_session.session_exists(session_id) is False:
		return HTTPException(status_code=401, detail="Invalid session")
	flashcard_session.continue_session(session_id)
	stats = flashcard_session.get_statistics()
	return {**stats}


# uvicorn.run(app, host="127.0.0.1", port=8001)