from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class DeckORM(SQLModel, table=True):
	__tablename__ = "decks"
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	description: Optional[str] = Field(default=None)
	cards: list["CardORM"] = Relationship(back_populates="deck")


	def __str__(self) -> str:
		return f"DeckORM(id={self.id}, name={self.name}, description={self.description}, cards_ids={[card.id for card in self.cards]})"

