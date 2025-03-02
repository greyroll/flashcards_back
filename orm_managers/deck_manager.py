from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import Session, create_engine, select

from orm_models.card_orm import CardORM
from orm_models.deck_orm import DeckORM
from orm_managers.base_manager import BaseORMManager


class DeckManager(BaseORMManager):
	model = DeckORM

	def fetch_all(self) -> list[DeckORM]:
		"""Fetch all decks."""
		with Session(self.engine) as session:
			return list(session.exec(select(DeckORM)).fetchall())

	def fetch_deck_by_id(self, deck_id: int) -> DeckORM | None:
		"""Fetch a deck by its ID."""
		with Session(self.engine) as session:
			return session.exec(select(DeckORM).options(selectinload(DeckORM.cards).subqueryload(CardORM.deck)).where(DeckORM.id == deck_id)).unique().one_or_none()

	def fetch_deck_by_name(self, deck_name: str) -> DeckORM | None:
		"""Fetch a deck by its name."""
		with Session(self.engine) as session:
			return session.exec(select(DeckORM).options(selectinload(DeckORM.cards).subqueryload(CardORM.deck)).where(DeckORM.name == deck_name)).unique().one_or_none()

	def fetch_decks_names(self) -> list[str] | None:
		"""Fetch all decks names."""
		with Session(self.engine) as session:
			return list(session.exec(select(DeckORM.name)))
		
	def add_deck(self, deck_id: int | None, name: str, description: str | None) -> DeckORM | None:
		"""Add a new deck."""
		with Session(self.engine) as session:
			deck = DeckORM(id=deck_id, name=name, description=description)
			session.add(deck)
			session.commit()
			session.refresh(deck)
		return deck

	def update_deck(self, deck_id: int, name: str, description: str | None):
		"""Update a deck."""
		with Session(self.engine) as session:
			deck = session.exec(select(DeckORM).where(DeckORM.id == deck_id)).one_or_none()
			if not deck:
				return None
			deck.name = name
			deck.description = description
			session.add(deck)
			session.commit()
			session.refresh(deck)
		return deck



