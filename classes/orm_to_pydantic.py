from typing import Type, TypeVar
from pydantic import BaseModel

T_ORM = TypeVar("T_ORM")  # Любая ORM-модель
T_Pydantic = TypeVar("T_Pydantic", bound=BaseModel)  # Только Pydantic-модели


class ORMToPydantic:

	@staticmethod
	def convert_orm_to_pydantic(orm_obj: T_ORM, pydantic_model: Type[T_Pydantic]) -> T_Pydantic:
		return pydantic_model.model_validate(orm_obj)

	@staticmethod
	def convert_pydantic_to_orm(pydantic_obj: T_Pydantic, orm_model: Type[T_ORM]) -> T_ORM:
		return orm_model(**pydantic_obj.model_dump())
