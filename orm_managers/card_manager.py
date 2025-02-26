from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import Session, create_engine, select

from orm_models.card import Card
from orm_models.deck import Deck
from orm_managers.base_manager import BaseORMManager


class CardManager(BaseORMManager):
	model = Card

	def fetch_by_id(self, card_id: int) -> Card | None:
		"""Fetch a card by its ID."""
		with Session(self.engine) as session:
			result = session.exec(select(Card).options(joinedload(Card.deck).subqueryload(Deck.cards)).where(Card.id == card_id)).one_or_none()
			return result

	def fetch_by_front(self, card_front: str) -> Card | None:
		"""Fetch a card by its front text."""
		with Session(self.engine) as session:
			return session.exec(select(Card).options(joinedload(Card.deck).subqueryload(Deck.cards)).where(
				Card.front == card_front)).one_or_none()

	def fetch_by_back(self, card_back: str) -> Card | None:
		"""Fetch a card by its back text."""
		with Session(self.engine) as session:
			return session.exec(select(Card).options(joinedload(Card.deck).subqueryload(Deck.cards)).where(Card.back == card_back)).one_or_none()

	# def add_card_to_deck(self, deck_id: int, card_id: int):
	# 	"""Add a card to a deck."""
	# 	with Session(self.engine) as session:
	# 		deck = session.exec(select(Deck).where(Deck.id == deck_id)).one_or_none()
	# 		card = session.exec(select(Card).where(Card.id == card_id)).one_or_none()
	# 		if
	# 		deck.cards.append(card)
	# 		card.deck_id = deck.id
	# 		session.add(deck)
	# 		session.commit()
	# 		session.refresh(card)
	# 		session.refresh(deck)

	def update_card(self, card_id: int, front: str, back: str, deck_id: int) -> Card | None:

		with Session(self.engine) as session:
			card = session.exec(select(Card).where(Card.id == card_id)).one_or_none()
			deck = session.exec(select(Deck).where(Deck.id == deck_id)).one_or_none()

			if not card:
				return None

			card.front = front
			card.back = back
			card.deck_id = deck_id

			if card not in deck.cards:
				deck.cards.append(card)
				session.add(deck)

			session.add(card)
			session.commit()
			session.refresh(card)
			session.refresh(deck)

		return card

	def add_card(self, card_id: int | None, front: str, back: str, deck_id: int) -> Card | None:
		with Session(self.engine) as session:
			deck = session.exec(select(Deck).where(Deck.id == deck_id)).one_or_none
			if not deck:
				return None
			card = Card(id=card_id, front=front, back=back, deck_id=deck_id)
			session.add(card)
			deck.cards.append(card)
			session.add(deck)
			session.commit()
			session.refresh(card)
			session.refresh(deck)

		return card


