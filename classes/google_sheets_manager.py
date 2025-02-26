from orm_managers import CardManager


class GoogleSheetsManager:

	def __init__(self):
		self.card_manager = CardManager()

	def update_card(self, card_id: int, front: str, back: str, deck_id: int):
		return self.card_manager.update_card(card_id, front, back, deck_id)

	def add_card(self, card_id: int | None, front: str, back: str, deck_id: int):
		return self.card_manager.add_card(card_id, front, back, deck_id)

	def card_exists(self, card_id: int) -> bool:
		if card_id is None:
			return False
		return self.card_manager.fetch_by_id(card_id) is not None