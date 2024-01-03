from app.db.base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, DateTime, Text


class LoginEntity(BaseEntity):

    __tablename__ = 'login'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 登入 ID
    user_id = Column(Integer, nullable=False)  # 使用者 ID
    login_time = Column(DateTime, nullable=False)  # 登入時間
