#!/user/bin/env python
"""Message model."""

from base_model import Base, BaseModel
from sqlalchemy import Column, String, DateTime, Text, ForeignKey


class Message(Base, BaseModel):
    """Class to manipulate messages table."""

    __tablename__ = "messages"
    id = Column(String(50), primary_key=True)
    sender_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    receiver_id = Column(String(50), ForeignKey('users.id'), nullable=False, primary_key=True)
    message = Column(Text)
    timestamp = Column(DateTime, nullable=False)
