from app.db.base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, DateTime, Text


class RoleEntity(BaseEntity):

    __tablename__ = 'role'

    id = Column(String(3), primary_key=True)  # 角色 ID
    name = Column(String(32), primary_key=True)  # 角色名稱
