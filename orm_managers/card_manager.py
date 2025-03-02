from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from orm_models.card_orm import CardORM
from orm_models.deck_orm import DeckORM
from orm_managers.base_manager import BaseORMManager


class CardManager(BaseORMManager):
	model = CardORM

	def fetch_all(self) -> list[CardORM]:
		"""Fetch all cards."""
		with Session(self.engine) as session:
			return list(session.exec(select(CardORM)).fetchall())

	def fetch_by_id(self, card_id: int) -> CardORM | None:
		"""Fetch a card by its ID."""
		with Session(self.engine) as session:
			result = session.exec(select(CardORM).options(joinedload(CardORM.deck).subqueryload(DeckORM.cards)).where(CardORM.id == card_id)).one_or_none()
			return result

	def fetch_by_front(self, card_front: str) -> CardORM | None:
		"""Fetch a card by its front text."""
		with Session(self.engine) as session:
			return session.exec(select(CardORM).options(joinedload(CardORM.deck).subqueryload(DeckORM.cards)).where(
				CardORM.front == card_front)).one_or_none()

	def fetch_by_back(self, card_back: str) -> CardORM | None:
		"""Fetch a card by its back text."""
		with Session(self.engine) as session:
			return session.exec(select(CardORM).options(joinedload(CardORM.deck).subqueryload(DeckORM.cards)).where(CardORM.back == card_back)).one_or_none()


	def update_card(self, card_id: int, front: str, back: str, deck_id: int | None) -> CardORM | None:
		"""Update a card."""
		with Session(self.engine) as session:
			card = session.exec(select(CardORM).where(CardORM.id == card_id)).one_or_none()

			if card is None:
				return None

			deck = session.exec(select(DeckORM).where(DeckORM.id == deck_id)).one_or_none() if deck_id else None

			if deck_id and deck is None:
				return None

			card.front = front
			card.back = back
			card.deck_id = deck_id

			if deck and card not in deck.cards:
				deck.cards.append(card)
				session.add(deck)

			session.add(card)
			session.commit()
			session.refresh(card)
			if deck:
				session.refresh(deck)

		return card

	def add_card(self, card_id: int | None, front: str, back: str, deck_id: int | None) -> CardORM | None:
		"""Add a new card."""
		with Session(self.engine) as session:
			deck = session.exec(select(DeckORM).where(DeckORM.id == deck_id)).one_or_none() if deck_id else None
			if deck_id and deck is None:
				return None
			card = CardORM(id=card_id, front=front, back=back, deck_id=deck_id)
			session.add(card)
			if deck:
				deck.cards.append(card)
				session.add(deck)
			session.commit()
			session.refresh(card)
			if deck:
				session.refresh(deck)

		return card


