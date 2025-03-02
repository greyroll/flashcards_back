import pytest

from orm_models import CardORM, DeckORM, UserORM, UserSessionORM
from pydantic_models import CardPydantic, DeckPydantic, UserPydantic, UserSessionPydantic


@pytest.fixture()
def card_orm():
	return CardORM(front="front", back="back")

@pytest.fixture()
def card_pydantic():
	return CardPydantic(front="front", back="back")

@pytest.fixture()
def deck_orm():
	return DeckORM(name="name")

@pytest.fixture()
def deck_pydantic():
	return DeckPydantic(name="name")

@pytest.fixture()
def user_orm():
	return UserORM(name="name")

@pytest.fixture()
def user_pydantic():
	return UserPydantic(name="name")

@pytest.fixture()
def user_session_orm():
	return UserSessionORM(user_id=1, deck_id=1, active_card_id=1)

@pytest.fixture()
def user_session_pydantic():
	return UserSessionPydantic(user_id=1, deck_id=1, active_card_id=1)