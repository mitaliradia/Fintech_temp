# from datetime import datetime
import datetime
from enum import Enum
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, ARRAY, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models import db

class RoleEnum(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    STATION_MASTER = "STATION_MASTER"
    SUPPORT_STAFF = "SUPPORT_STAFF"
    FINANCE_ADMIN = "FINANCE_ADMIN"

class Admin(db.Model):
    __tablename__ = "admins"
    __table_args__ = {'extend_existing': True} 
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLAEnum(RoleEnum), nullable=False)
    station_id = Column(UUID(as_uuid=True), ForeignKey("stations.id", deferrable=True), nullable=True)
    permissions = Column(ARRAY(String), default=[])
    last_login_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("admins.id"), nullable=True)
    profile_image = Column(String(255), nullable=True)
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    creator = relationship("Admin", remote_side=[id], backref="created_admins")
    station = relationship("Station", backref="station_masters")
    
    def __repr__(self):
        return f"<Admin {self.email} ({self.role})>"
