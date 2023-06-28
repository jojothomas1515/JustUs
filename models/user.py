#!/user/bin/env python
"""User model."""

from sqlalchemy import Column, String, Date, Boolean

from models.base_model import Base, BaseModel
from models.message import Message


class User(BaseModel, Base):
    """Class to manipulate users table.

    Returns:
        User
    """

    __tablename__ = "users"
    id = Column(String(50), primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    date_of_birth = Column(Date)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean)

    @property
    def friends(self):
        """get all user friends"""
        res = []
        res.extend(list(
            map(lambda f: {"status": f.status.value, "requester_id": f.requester_id, "data": f.friend2.to_dict()},
                self.friend1)))
        res.extend(list(
            map(lambda f: {"status": f.status.value, "requester_id": f.requester_id, "data": f.friend1.to_dict()},
                self.friend2)))
        return res

    @property
    def exc_friends(self):
        """get all user friends"""
        res = []
        res.extend(list(map(lambda f: f.friend2, self.friend1)))
        res.extend(list(map(lambda f: f.friend1, self.friend2)))
        return res

    def messages_with(self, user_id: str):
        data = Message.filter(((Message.sender_id == self.id) & (Message.receiver_id == user_id)) | (
                (Message.sender_id == user_id) & (Message.receiver_id == self.id)))
        messages = list(map(lambda message: message.to_dict(), data))
        return messages

    def get_id(self):
        """For Flask Login to get the user id

        Returns:
            User id.
        """

        return self.id

    def to_dict(self):
        res = super().to_dict()
        try:
            res.pop('friend1')
            res.pop('friend2')
        except KeyError:
            pass
        return res

    @property
    def is_authenticated(self):
        """Check is user is authenticated

        Returns:
            True if user is_active
        """
        return True
