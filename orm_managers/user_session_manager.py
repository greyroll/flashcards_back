from sqlmodel import Session, select, and_

from orm_models.user_session import UserSession
from orm_managers.base_manager import BaseORMManager


class UserSessionManager(BaseORMManager):
	model = UserSession

	def fetch_by_session_id(self, session_id: int) -> UserSession:
		"""Fetch a session by its ID."""
		with Session(self.engine) as session:
			return session.exec(select(UserSession).where(UserSession.id == session_id)).one_or_none()

	def fetch_all_by_user_id(self, user_id: int) -> list[UserSession]:
		"""Fetch all sessions for a user."""
		with Session(self.engine) as session:
			return session.exec(select(UserSession).where(UserSession.user_id == user_id)).fetchall()

	def fetch_by_user_id_deck_id(self, user_id: int, deck_id: int) -> UserSession | None:
		"""Fetch a session for a user and deck."""
		with Session(self.engine) as session:
			return session.exec(select(UserSession).where(and_(UserSession.user_id == user_id, UserSession.deck_id == deck_id))).unique().one_or_none()

	def create(self, user_id: int, deck_id: int) -> UserSession:
		"""Create a new session for a user and deck."""
		with Session(self.engine) as session:
			session_obj = UserSession(user_id=user_id, deck_id=deck_id)
			session.add(session_obj)
			session.commit()
			session.refresh(session_obj)
			return session_obj

	def update_session(self, user_session: UserSession):
		"""Update an existing session."""
		with Session(self.engine) as session:
			session_obj = session.exec(select(UserSession).where(UserSession.id == user_session.id)).first()
			if session_obj is None:
				raise ValueError("Session for the user not found.")
			session_obj.studied_cards_ids = user_session.studied_cards_ids
			session_obj.left_cards_ids = user_session.left_cards_ids
			session_obj.active_card_id = user_session.active_card_id
			session_obj.is_finished = user_session.is_finished
			session.add(session_obj)
			session.commit()
			session.refresh(session_obj)

	def finish(self, user_session: UserSession):
		"""Mark a session as finished."""
		with Session(self.engine) as session:
			session_obj = session.exec(select(UserSession).where(UserSession.id == user_session.id)).first()
			if session_obj is None:
				raise ValueError("Session for the user not found.")
			session_obj.active_card_id = None
			session_obj.is_finished = True
			session.commit()
			session.add(session_obj)
			session.commit()
			session.refresh(session_obj)


	def delete(self, *args):
		raise NotImplementedError

