from sqlmodel import Session, select

from orm_models import User
from orm_managers.base_manager import BaseORMManager


class UserManager(BaseORMManager):
	model = User

	def create_user_if_not_exists(self, user_name: str) -> User:
		"""Create a new user if they don't already exist."""
		user = self.fetch_by_user_name(user_name)
		if user is None:
			user = User(name=user_name)
			self.add(user)
		return user

	def fetch_by_id(self, user_id: int) -> User:
		"""Fetch a user by their ID."""
		with Session(self.engine) as session:
			return session.exec(select(User).where(User.id == user_id)).one_or_none()

	def fetch_by_user_name(self, user_name: str) -> User:
		"""Fetch a user by their username."""
		with Session(self.engine) as session:
			return session.exec(select(User).where(User.name == user_name)).one_or_none()

	def fetch_all_users(self) -> list[User]:
		"""Fetch all users from the database."""
		with Session(self.engine) as session:
			return session.exec(select(User)).all()

