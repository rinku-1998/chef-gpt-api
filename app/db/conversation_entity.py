from app.db.base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, DateTime


class ConversationEntity(BaseEntity):

    __tablename__ = 'conversation'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 使用者 ID
    title = Column(String(128), nullable=False)  # 對話標題
    create_time = Column(DateTime, nullable=False)  # 建立時間
