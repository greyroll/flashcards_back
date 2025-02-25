import random

from orm_managers import DeckManager, CardManager, UserManager
from orm_models import Card, Deck, User, UserSession
from orm_managers.user_session_manager import UserSessionManager


class FlashcardsSession:
	def __init__(self):
		self.session: UserSession | None = None
		self.user_session_manager = UserSessionManager()
		self.deck_manager = DeckManager()
		self.card_manager = CardManager()
		self.user_manager = UserManager()

	def get_decks_names(self) -> list[str]:
		"""Fetch all decks names."""
		return self.deck_manager.fetch_decks_names()

	def start_session(self, user_name: str, deck_name: str):
		"""Starts a new session. Adds user id, deck id and cards ids to the session. Sets session.active card to the first card of session.left_card_ids list"""
		user: User = self.user_manager.create_user_if_not_exists(user_name)
		deck: Deck = self.deck_manager.fetch_deck_by_name(deck_name)
		self.session = self.user_session_manager.create(user.id, deck.id)

		current_deck_cards_ids: list[int] = [card.id for card in self.deck_manager.fetch_deck_by_id(deck.id).cards]
		self.session.left_cards_ids = current_deck_cards_ids.copy()
		random.shuffle(self.session.left_cards_ids)
		self.session.active_card_id = self.session.left_cards_ids[0]
		self.update_session()

	def continue_session(self, session_id: int):
		"""Continue a session."""
		self.session = self.user_session_manager.fetch_by_session_id(session_id)
		self.update_session()

	def update_session(self):
		"""Update the session in the database."""
		self.user_session_manager.update_session(self.session)

	def show_card_front(self):
		"""Show the front of the active card."""
		return self.card_manager.fetch_by_id(self.session.active_card_id).front

	def show_card_back(self):
		"""Show the back of the active card."""
		return self.card_manager.fetch_by_id(self.session.active_card_id).back

	def know_or_repeat_active_card(self, is_known: bool):
		"""Appends the active card to the list of studied cards if card is known. Else appends the active card to the list of left cards."""
		self.session.left_cards_ids.remove(self.session.active_card_id)
		if is_known is False:
			self.session.left_cards_ids.append(self.session.active_card_id)
		else:
			self.session.studied_cards_ids.append(self.session.active_card_id)

		if len(self.session.left_cards_ids) == 0:
			self.session.is_finished = True
			self.session.active_card_id = None
		else:
			self.session.active_card_id = self.session.left_cards_ids[0]
		self.update_session()

	def get_statistics(self):
		"""Returns the statistics of the session."""
		return {"studied_cards_number": len(self.session.studied_cards_ids)}

	def session_exists(self, session_id: int):
		"""Checks if the session exists."""
		return self.user_session_manager.fetch_by_session_id(session_id) is not None





