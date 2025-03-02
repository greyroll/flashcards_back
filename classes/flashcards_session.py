import random

from orm_managers import DeckManager, CardManager, UserManager
from orm_models import DeckORM, UserORM, UserSessionORM
from orm_managers.user_session_manager import UserSessionManager


class FlashcardsSession:
	def __init__(self):
		self.user_session_manager = UserSessionManager()
		self.deck_manager = DeckManager()
		self.card_manager = CardManager()
		self.user_manager = UserManager()

	def get_decks_names(self) -> list[str]:
		"""Fetch all decks names."""
		return self.deck_manager.fetch_decks_names()

	def start_session(self, user_name: str, deck_name: str):
		"""Starts a new session. Adds user id, deck id and cards ids to the session. Sets session.active card to the first card of session.left_card_ids list"""
		user: UserORM = self.user_manager.create_user_if_not_exists(user_name)
		deck: DeckORM = self.deck_manager.fetch_deck_by_name(deck_name)
		session: UserSessionORM = self.user_session_manager.create(user.id, deck.id)

		current_deck_cards_ids: list[int] = [card.id for card in self.deck_manager.fetch_deck_by_id(deck.id).cards]
		session.left_cards_ids = current_deck_cards_ids.copy()
		random.shuffle(session.left_cards_ids)
		session.active_card_id = session.left_cards_ids[0]
		self.update_session(session)
		return session

	def update_session(self, session: UserSessionORM):
		"""Update the session in the database."""
		self.user_session_manager.update_session(session)

	def show_card_front(self, session_id: int):
		"""Show the front of the active card."""
		session: UserSessionORM = self.get_session_by_id(session_id)
		return self.card_manager.fetch_by_id(session.active_card_id).front

	def show_card_back(self, session_id: int):
		"""Show the back of the active card."""
		session: UserSessionORM = self.get_session_by_id(session_id)
		return self.card_manager.fetch_by_id(session.active_card_id).back

	def know_or_repeat_active_card(self, session_id: int, is_known: bool):
		"""Appends the active card to the list of studied cards if card is known. Else appends the active card to the list of left cards."""
		session: UserSessionORM = self.get_session_by_id(session_id)
		session.left_cards_ids.remove(session.active_card_id)
		if is_known is False:
			session.left_cards_ids.append(session.active_card_id)
		else:
			session.studied_cards_ids.append(session.active_card_id)

		if len(session.left_cards_ids) == 0:
			session.is_finished = True
			session.active_card_id = None
		else:
			session.active_card_id = session.left_cards_ids[0]
		self.update_session(session)

	def get_statistics(self, session_id: int):
		"""Returns the statistics of the session."""
		session: UserSessionORM = self.get_session_by_id(session_id)
		return {"studied_cards_number": len(session.studied_cards_ids)}

	def get_session_by_id(self, session_id: int) -> UserSessionORM:
		return self.user_session_manager.fetch_by_session_id(session_id)

	def session_exists(self, session_id: int):
		"""Checks if the session exists."""
		return self.user_session_manager.fetch_by_session_id(session_id) is not None





