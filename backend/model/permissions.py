from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .roles import role_permissions


class Permission(Base):
    __tablename__ = 'permissions'
    permission_id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String, unique=True, index=True)
    description = Column(String)
    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )