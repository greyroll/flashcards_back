from sqlmodel import Session, select

from orm_models import UserORM
from orm_managers.base_manager import BaseORMManager


class UserManager(BaseORMManager):
	model = UserORM

	def create_user_if_not_exists(self, user_name: str) -> UserORM:
		"""Create a new user if they don't already exist."""
		user = self.fetch_by_user_name(user_name)
		if user is None:
			user = UserORM(name=user_name)
			self.add(user)
		return user

	def fetch_by_id(self, user_id: int) -> UserORM | None:
		"""Fetch a user by their ID."""
		with Session(self.engine) as session:
			return session.exec(select(UserORM).where(UserORM.id == user_id)).one_or_none()

	def fetch_by_user_name(self, user_name: str) -> UserORM | None:
		"""Fetch a user by their username."""
		with Session(self.engine) as session:
			return session.exec(select(UserORM).where(UserORM.name == user_name)).one_or_none()

	def fetch_all_users(self) -> list[UserORM]:
		"""Fetch all users from the database."""
		with Session(self.engine) as session:
			return list(session.exec(select(UserORM)).all())

