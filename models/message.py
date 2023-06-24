#!/user/bin/env python
"""Message model."""
import datetime

from sqlalchemy import Column, String, DateTime, Text, ForeignKey

from models.base_model import Base, BaseModel


class Message(BaseModel, Base):
    """Class to manipulate messages table."""

    __tablename__ = "messages"
    id = Column(String(50), primary_key=True)
    sender_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    message = Column(Text)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.now())

    def to_dict(self):
        """convert object to_dictionary for json serialization"""
        info = super().to_dict()
        info['timestamp'] = self.timestamp.isoformat()
        return info
