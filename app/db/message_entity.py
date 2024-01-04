from app.db.base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, DateTime, Text


class MessageEntity(BaseEntity):

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 訊息 ID
    conversation_id = Column(Integer, nullable=False)  # 對話 ID
    role_id = Column(String(3), nullable=False)  # 角色 ID
    content = Column(Text, nullable=False)  # 內容
    create_time = Column(DateTime, nullable=False)  # 建立時間
