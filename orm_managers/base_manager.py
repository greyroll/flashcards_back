from pathlib import Path

from loguru import logger

from sqlmodel import Session, create_engine, SQLModel

from config import DB_PATH


class BaseORMManager:
	model: SQLModel | None = None

	def __init__(self):
		project_root = Path(__file__).resolve().parent.parent  # Поднимаемся на уровень вверх
		db_path = project_root / DB_PATH  # Формируем полный путь к базе данных
		path = f"sqlite:///{db_path.resolve()}"  # Полный абсолютный путь
		print({"path": path})  # Проверяем правильность пути
		self.engine = create_engine(path)

		# project_root = Path(__file__).resolve().parent.parent  # 1 уровня вверх от текущего файла
		# # db_path = project_root / DB_PATH  # Путь к базе данных в корне проекта
		# path = f"sqlite:///{DB_PATH}"
		# print({"path": path})
		# self.engine = create_engine(path)

	def create_all_tables(self):
		"""Create all tables in the database."""
		SQLModel.metadata.create_all(self.engine)

	def add(self, obj: SQLModel):
		"""Add an object to the database."""
		with Session(self.engine) as session:
			session.add(obj)
			session.commit()
			session.refresh(obj)

	def delete(self, obj_id: int):
		"""Delete an object from the database."""
		if self.model is None:
			raise AttributeError("Define model to use delete")
		with Session(self.engine) as session:
			obj = session.get(self.model, obj_id)
			session.delete(obj)
			session.commit()
