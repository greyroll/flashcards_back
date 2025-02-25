from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

from orm_models.deck import Deck


class Card(SQLModel, table=True):
	__tablename__ = "cards"
	id: Optional[int] = Field(default=None, primary_key=True)
	front: str
	back: str
	deck_id: Optional[int] = Field(default=None, foreign_key="decks.id")
	deck: Deck | None = Relationship(back_populates="cards")


	def __str__(self):
		return f"Card(id={self.id}, front={self.front}, back={self.back}, deck_id={self.deck_id})"

