#!/user/bin/env python
"""Friends model."""
import datetime
import enum

from sqlalchemy import Column, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models.base_model import Base
from models.base_model import BaseModel


class FriendshipStatus(enum.Enum):
    """Friend request status"""
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class Friend(BaseModel, Base):
    """Class to manipulate messages table."""

    __tablename__ = "friends"
    requester_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    requested_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    status = Column(Enum(FriendshipStatus, length=20), nullable=False)
    date = Column(Date, nullable=False, default=datetime.date.today())

    friend1 = relationship("User", backref="friend1", foreign_keys="Friend.requester_id", cascade="all, delete-orphan", single_parent=True)
    friend2 = relationship("User", backref="friend2", foreign_keys="Friend.requested_id", cascade="all, delete-orphan", single_parent=True)

    def to_dict(self):
        """"""

        info = super().to_dict()
        info.pop("id", None)
        info["status"] = self.status.value
        info["date"] = self.date.isoformat()

        return info
