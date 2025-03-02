import gspread

from oauth2client.service_account import ServiceAccountCredentials

from config import GOOGLE_CREDENTIALS
from orm_managers import CardManager, DeckManager
from pydantic_models import CardPydantic, DeckPydantic


class GoogleSheetsManager:

	def __init__(self):
		self.card_manager = CardManager()
		self.deck_manager = DeckManager()

	def connect_to_google_sheets(self, spreadsheet_name):
		scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
		creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS)
		client = gspread.authorize(creds)

		spreadsheet = client.open(spreadsheet_name)
		return spreadsheet

	def update_card(self, card: CardPydantic):
		return self.card_manager.update_card(card.id, card.front, card.back, card.deck_id)

	def add_card(self, card: CardPydantic):
		return self.card_manager.add_card(card.id, card.front, card.back, card.deck_id)

	def	update_cards_table(self, data: list[tuple]):
		card_instances = []
		for row in data[1:]:  # Пропускаем заголовки
			card_id = int(row[0]) if row[0].strip() else None
			deck_id = int(row[3]) if row[3].strip() else None

			card = CardPydantic(
				id=card_id,
				front=row[1] if row[1].strip() else None,
				back=row[2] if row[2].strip() else None,
				deck_id=deck_id
			)
			card_instances.append(card)

		for card in card_instances:
			if self.card_exists(card.id):
				self.update_card(card)
			else:
				self.add_card(card)

	def card_exists(self, card_id: int) -> bool:
		if card_id is None:
			return False
		return self.card_manager.fetch_by_id(card_id) is not None

	def add_deck(self, deck: DeckPydantic):
		return self.deck_manager.add_deck(deck.id, deck.name, deck.description)

	def update_deck(self, deck: DeckPydantic):
		return self.deck_manager.update_deck(deck.id, deck.name, deck.description)

	def deck_exists(self, deck_id: int) -> bool:
		if deck_id is None:
			return False
		return self.deck_manager.fetch_deck_by_id(deck_id) is not None

	def update_decks_table(self, data: list[tuple]):
		deck_instances = []
		for row in data[1:]:  # Пропускаем заголовки
			deck_id = int(row[0]) if row[0].strip() else None

			deck = DeckPydantic(
				id=deck_id,
				name=row[1],
				description=row[2] if row[2].strip() else None,
			)
			deck_instances.append(deck)

		for deck in deck_instances:
			if self.deck_exists(deck.id):
				self.update_deck(deck)
			else:
				self.add_deck(deck)