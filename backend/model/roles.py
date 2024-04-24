from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from .base import Base

role_permissions = Table('role_permissions', Base.metadata,
                         Column('role_id', ForeignKey('roles.role_id'), primary_key=True),
                         Column('permission_id', ForeignKey('permissions.permission_id'), primary_key=True)
                         )


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
