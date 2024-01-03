from app.db.base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, DateTime


class UserEntity(BaseEntity):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 使用者 ID
    name = Column(String(128), nullable=False)  # 名字
    email = Column(String(256), nullable=False)  # Email
    password_hash = Column(String(256), nullable=False)  # 雜湊密碼
    create_time = Column(DateTime,
                         nullable=False)  # 建立時間
