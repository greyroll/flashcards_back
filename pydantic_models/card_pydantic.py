from typing import Optional

from pydantic import BaseModel


class CardPydantic(BaseModel):
	id: Optional[int] = None
	front: str
	back: str
	deck_id: Optional[int] = None

	class Config:
		from_attributes = True