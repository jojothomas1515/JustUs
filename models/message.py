#!/user/bin/env python
"""Message model."""

from base_model import Base
from sqlalchemy import Column, String, DateTime, Text, ForeignKey


class Message(Base):
    """Class to manipulate messages table."""

    __tablename__ = "messages"

    sender_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    receiver_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    message = Column(Text)
    timestamp = Column(DateTime, nullable=False)
