from typing import Optional

from pydantic import BaseModel, Field


class UserSessionPydantic(BaseModel):
	id: Optional[int] = None
	user_id: int
	deck_id: Optional[int] = None
	active_card_id: Optional[int] = None
	is_finished: bool = False
	studied_cards_ids: Optional[list[int]] = None
	left_cards_ids: Optional[list[int]] = None


	class Config:
		from_attributes = True