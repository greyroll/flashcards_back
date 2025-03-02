from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class UserSessionORM(SQLModel, table=True):
	__tablename__ = "user_sessions"
	id: Optional[int] = Field(default=None, primary_key=True)
	user_id: int = Field(foreign_key="users.id")
	deck_id: Optional[int] = Field(default=None, foreign_key="decks.id")
	active_card_id: Optional[int] = Field(default=None, foreign_key="cards.id")
	is_finished: bool = Field(default=False)

	studied_cards_ids: list[int] = Field(default_factory=list, sa_column=Column(JSON))
	left_cards_ids: list[int] =	Field(default_factory=list, sa_column=Column(JSON))

	def __str__(self):
		return f"UserSessionORM(id={self.id}, user_id={self.user_id}, deck_id={self.deck_id}, active_card_id={self.active_card_id})"

