import gspread

from oauth2client.service_account import ServiceAccountCredentials

from config import GOOGLE_CREDENTIALS
from orm_managers import CardManager, DeckManager
from pydantic_models import CardPydantic, DeckPydantic


class GoogleSheetsManager:

	def __init__(self):
		self.card_manager = CardManager()
		self.deck_manager = DeckManager()
		self.spreadsheet = self.connect_to_google_sheets("flashcards_data")

	@classmethod
	def connect_to_google_sheets(cls, spreadsheet_name):
		"""
		Establishes a connection to a Google Sheets spreadsheet using service account
		credentials. This method uses the provided credentials to authenticate with
		Google Sheets API and opens the specified spreadsheet.

		:param spreadsheet_name: The name of the Google Sheets spreadsheet to connect to.
		:type spreadsheet_name: str
		:return: A reference to the opened Google Sheets spreadsheet.
		:rtype: gspread.models.Spreadsheet
		"""
		creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS)
		client = gspread.authorize(creds)

		spreadsheet = client.open(spreadsheet_name)
		return spreadsheet

	def export_cards_to_google_sheets(self):
		"""
		Exports cards data to a Google Sheets spreadsheet. Gets all flashcards
		from the card manager, connects to an existing Google Sheets spreadsheet,
		writes the data into a worksheet named "cards".
		"""
		cards = self.card_manager.fetch_all()
		cards_sheet = self.spreadsheet.worksheet("cards")
		cards_sheet.clear()
		cards_sheet.append_row(["id", "front", "back", "deck_id"])
		for card in cards:
			cards_sheet.append_row([str(card.id), str(card.front), str(card.back), str(card.deck_id)])

	def add_card(self, card: CardPydantic):
		"""
		Adds a card to the database using CardManager.
		"""
		return self.card_manager.add_card(card.id, card.front, card.back, card.deck_id)

	def update_card(self, card: CardPydantic):
		"""
		Updates an existing card in the database.
		"""
		return self.card_manager.update_card(card.id, card.front, card.back, card.deck_id)

	def card_exists(self, card_id: int) -> bool:
		"""
		Determines whether a card with the specified ID exists in the database.
		"""
		if card_id is None:
			return False
		return self.card_manager.fetch_by_id(card_id) is not None

	def	update_cards_table(self):
		"""
		Updates the local cards table by retrieving data from the spreadsheet and synchronizing
		it with the database. Update_cards_table method can only
		update existing cards or add new ones. To delete card use delete_card method.
		"""
		cards_sheet = self.spreadsheet.worksheet("cards")
		data: list[tuple] = cards_sheet.get_all_values()
		card_instances = []
		for row in data[1:]:
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

	def delete_card(self, card_id: int):
		"""Deletes a card from the database"""
		self.card_manager.delete(card_id)

	def export_decks_to_google_sheets(self):
		"""
		Exports all decks to a Google Sheets spreadsheet. Gets a list of
		all decks using the deck manager, connects to a Google Sheets document,
		and appends deck data to the "decks" worksheet .
		"""
		decks = self.deck_manager.fetch_all()
		decks_sheet = self.spreadsheet.worksheet("decks")
		decks_sheet.clear()
		decks_sheet.append_row(["id", "name", "description"])
		for deck in decks:
			decks_sheet.append_row([str(deck.id), str(deck.name), str(deck.description)])

	def add_deck(self, deck: DeckPydantic):
		"""Adds a deck to the database"""
		return self.deck_manager.add_deck(deck.id, deck.name, deck.description)

	def deck_exists(self, deck_id: int) -> bool:
		"""Determines whether a deck with the specified ID exists in the database."""
		if deck_id is None:
			return False
		return self.deck_manager.fetch_deck_by_id(deck_id) is not None

	def update_deck(self, deck: DeckPydantic):
		"""Updates an existing deck in the database."""
		return self.deck_manager.update_deck(deck.id, deck.name, deck.description)

	def update_decks_table(self):
		"""
		Updates the decks table, fetches data from a connected Google Sheets document
		and synchronizes it with the local database. Update_decks_table method can only
		update existing decks or add new ones. To delete deck use delete_deck method.
		"""
		decks_sheet = self.spreadsheet.worksheet("decks")
		data: list[tuple] = decks_sheet.get_all_values()
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

	def delete_deck(self, deck_id: int):
		"""Deletes a deck from the database"""
		self.deck_manager.delete(deck_id)