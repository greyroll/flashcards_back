from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import Session, create_engine, select

from orm_models.card import Card
from orm_models.deck import Deck
from orm_managers.base_manager import BaseORMManager


class DeckManager(BaseORMManager):
	model = Deck

	def fetch_deck_by_id(self, deck_id: int) -> Deck | None:
		"""Fetch a deck by its ID."""
		with Session(self.engine) as session:
			return session.exec(select(Deck).options(selectinload(Deck.cards).subqueryload(Card.deck)).where(Deck.id == deck_id)).unique().one_or_none()

	def fetch_deck_by_name(self, deck_name: str) -> Deck | None:
		"""Fetch a deck by its name."""
		with Session(self.engine) as session:
			return session.exec(select(Deck).options(selectinload(Deck.cards).subqueryload(Card.deck)).where(Deck.name == deck_name)).unique().one_or_none()

	def fetch_decks_names(self) -> list[str] | None:
		"""Fetch a deck by its name."""
		with Session(self.engine) as session:
			return list(session.exec(select(Deck.name)))
		
	def add_deck(self, deck_id: int | None, name: str, description: str):
		with Session(self.engine) as session:
			deck = Deck(id=deck_id, name=name, description=description)
			session.add(deck)
			session.commit()
			session.refresh(deck)
		return deck

	def update_deck(self, deck_id: int, name: str, description: str):
		with Session(self.engine) as session:
			deck = session.exec(select(Deck).where(Deck.id == deck_id)).one_or_none()
			if not deck:
				return None
			deck.name = name
			deck.description = description
			session.add(deck)
			session.commit()
			session.refresh(deck)
		return deck



