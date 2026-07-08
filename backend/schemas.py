from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class VaultItemBase(BaseModel):
    title: str
    username_encrypted: str
    password_encrypted: str
    url_encrypted: Optional[str] = None
    notes_encrypted: Optional[str] = None
    favorite: bool = False
    folder_id: Optional[int] = None

class VaultItemCreate(VaultItemBase):
    pass

class VaultItem(VaultItemBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class FolderBase(BaseModel):
    name: str

class FolderCreate(FolderBase):
    pass

class Folder(FolderBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True
