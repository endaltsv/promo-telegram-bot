from sqlalchemy import Column, Integer, String

from bot.database.database_config import Base


class Setting(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    welcome_message = Column(String, nullable=False)
    support_id = Column(String, nullable=True)
