from typing import Optional

from pydantic import BaseModel


class DeckPydantic(BaseModel):
	id: Optional[int] = None
	name: str
	description: Optional[str] = None

	class Config:
		from_attributes = True