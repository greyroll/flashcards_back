from orm_managers import CardManager, DeckManager


class GoogleSheetsManager:

	def __init__(self):
		self.card_manager = CardManager()
		self.deck_manager = DeckManager()

	def update_card(self, card_id: int, front: str, back: str, deck_id: int):
		return self.card_manager.update_card(card_id, front, back, deck_id)

	def add_card(self, card_id: int | None, front: str, back: str, deck_id: int):
		return self.card_manager.add_card(card_id, front, back, deck_id)

	def card_exists(self, card_id: int) -> bool:
		if card_id is None:
			return False
		return self.card_manager.fetch_by_id(card_id) is not None

	def add_deck(self, deck_id: int | None, name: str, description: str):
		return self.deck_manager.add_deck(deck_id, name, description)

	def update_deck(self, deck_id: int, name: str, description: str):
		return self.deck_manager.update_deck(deck_id, name, description)