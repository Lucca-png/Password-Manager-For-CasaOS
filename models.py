from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    encryption_salt = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    vault_items = relationship("VaultItem", back_populates="owner")
    folders = relationship("Folder", back_populates="owner")

class VaultItem(Base):
    __tablename__ = "vault_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    title = Column(String)
    username_encrypted = Column(String)
    password_encrypted = Column(String)
    url_encrypted = Column(String, nullable=True)
    notes_encrypted = Column(String, nullable=True)
    favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="vault_items")
    folder = relationship("Folder", back_populates="items")

class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)

    owner = relationship("User", back_populates="folders")
    items = relationship("VaultItem", back_populates="folder")
