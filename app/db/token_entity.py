from app.db.base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, DateTime


class TokenEntity(BaseEntity):

    __tablename__ = 'token'

    token = Column(String(32), primary_key=True)  # Token
    user_id = Column(Integer, nullable=False)  # 使用者 ID
    issue_time = Column(DateTime, nullable=False)  # 發行時間
