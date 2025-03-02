import pytest

from classes.orm_to_pydantic import ORMToPydantic
from orm_models import CardORM, DeckORM, UserORM, UserSessionORM
from pydantic_models import CardPydantic, DeckPydantic, UserPydantic, UserSessionPydantic


def test_convert_card_orm_to_pydantic(card_orm):
	card_pydantic = ORMToPydantic.convert_orm_to_pydantic(card_orm, CardPydantic)

	assert isinstance(card_pydantic, CardPydantic)
	assert card_pydantic.id == None
	assert card_pydantic.front == "front"
	assert card_pydantic.back == "back"
	assert card_pydantic.deck_id == None


def test_convert_card_pydantic_to_orm(card_pydantic):
	card_orm = ORMToPydantic.convert_pydantic_to_orm(card_pydantic, CardORM)

	assert isinstance(card_orm, CardORM)
	assert card_orm.id == None
	assert card_orm.front == "front"
	assert card_orm.back == "back"
	assert card_orm.deck_id == None


def test_convert_deck_orm_to_pydantic(deck_orm):
	deck_pydantic = ORMToPydantic.convert_orm_to_pydantic(deck_orm, DeckPydantic)

	assert isinstance(deck_pydantic, DeckPydantic)
	assert deck_pydantic.id == None
	assert deck_pydantic.name == "name"


def test_convert_deck_pydantic_to_orm(deck_pydantic):
	deck_orm = ORMToPydantic.convert_pydantic_to_orm(deck_pydantic, DeckORM)

	assert isinstance(deck_orm, DeckORM)
	assert deck_orm.id == None
	assert deck_orm.name == "name"


def test_convert_user_orm_to_pydantic(user_orm):
	user_pydantic = ORMToPydantic.convert_orm_to_pydantic(user_orm, UserPydantic)

	assert isinstance(user_pydantic, UserPydantic)
	assert user_pydantic.id == None
	assert user_pydantic.name == "name"


def test_convert_user_pydantic_to_orm(user_pydantic):
	user_orm = ORMToPydantic.convert_pydantic_to_orm(user_pydantic, UserORM)

	assert isinstance(user_orm, UserORM)
	assert user_orm.id == None
	assert user_orm.name == "name"


def test_convert_user_session_orm_to_pydantic(user_session_orm):
	user_session_pydantic = ORMToPydantic.convert_orm_to_pydantic(user_session_orm, UserSessionPydantic)

	assert isinstance(user_session_pydantic, UserSessionPydantic)
	assert user_session_pydantic.id == None
	assert user_session_pydantic.user_id == 1
	assert user_session_pydantic.deck_id == 1
	assert user_session_pydantic.active_card_id == 1
	assert user_session_pydantic.is_finished == False
	assert user_session_pydantic.studied_cards_ids == []
	assert user_session_pydantic.left_cards_ids == []


def test_convert_user_session_pydantic_to_orm(user_session_pydantic):
	user_session_orm = ORMToPydantic.convert_pydantic_to_orm(user_session_pydantic, UserSessionORM)

	assert isinstance(user_session_orm, UserSessionORM)
	assert user_session_orm.id == None
	assert user_session_orm.user_id == 1
	assert user_session_orm.deck_id == 1
	assert user_session_orm.active_card_id == 1
	assert user_session_orm.is_finished == False
	assert user_session_orm.studied_cards_ids == None
	assert user_session_orm.left_cards_ids == None