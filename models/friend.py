#!/user/bin/env python
"""Friends model."""

import enum

from sqlalchemy import Column, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models.base_model import Base
from models.base_model import BaseModel
from models.user import User


class FriendshipStatus(enum.Enum):
    """Friend request status"""
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class Friend(Base, BaseModel):
    """Class to manipulate messages table."""

    __tablename__ = "friends"
    requester_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    requested_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    status = Column(Enum(FriendshipStatus, length=20), nullable=False)
    date = Column(Date, nullable=False)

    friend1 = relationship("User", backref="friend1", foreign_keys="Friend.requester_id")
    friend2 = relationship("User", backref="friend2", foreign_keys="Friend.requested_id")

