from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Messages(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id', ondelete='CASCADE'), index=True)
    role = Column(String)
    content = Column(String)
    timestamp = Column(String, nullable=True)

    def get_dict_format(self):
        return {"role": self.role, "content": self.content, "timestamp": self.timestamp}


class Sessions(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True, index=True)
    date_created = Column(String, nullable=True)
    name = Column(String)

    def get_dict_format(self):
        return {"session_id": self.session_id, "date_created": self.date_created, "name": self.name}
