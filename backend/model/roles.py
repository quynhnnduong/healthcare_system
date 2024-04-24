from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import Base
from .permissions import role_permissions


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)
    description = Column(String)
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )

