from typing import Optional

from pydantic import BaseModel


class UserPydantic(BaseModel):
	id: Optional[int] = None
	name: str

	class Config:
		from_attributes = True