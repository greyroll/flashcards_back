from typing import Optional

from sqlmodel import Field, SQLModel


class UserORM(SQLModel, table=True):
	__tablename__ = "users"
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str

	def __repr__(self) -> str:
		return f"UserORM(id={self.id}, name={self.name}"
