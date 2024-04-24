from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

role_permissions = Table('role_permissions', Base.metadata,
                         Column('role_id', ForeignKey('roles.role_id'), primary_key=True),
                         Column('permission_id', ForeignKey('permissions.permission_id'), primary_key=True)
                         )

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