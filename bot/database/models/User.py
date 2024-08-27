from sqlalchemy import Column, Integer, String, Boolean

from bot.database.database_config import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    username = Column(String(50), nullable=True, unique=True)
    language = Column(String(2), nullable=False, default='ru')
    is_admin = Column(Boolean, nullable=False, default=False)
    last_message = Column(String)