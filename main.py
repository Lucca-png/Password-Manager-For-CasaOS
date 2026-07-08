import os
import string
import random
import json
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import models, schemas, auth, database, security

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Minimalist Password Manager API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication Endpoints
@app.post("/api/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = auth.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return auth.create_user(db=db, user=user)

@app.post("/api/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = auth.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if not auth.verify_password(old_password, current_user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    current_user.password_hash = auth.get_password_hash(new_password)
    db.commit()
    return {"message": "Password changed successfully"}

# Vault Endpoints
@app.get("/api/vault", response_model=list[schemas.VaultItem])
def get_vault(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.VaultItem).filter(models.VaultItem.user_id == current_user.id).all()

@app.post("/api/vault", response_model=schemas.VaultItem)
def create_vault_item(item: schemas.VaultItemCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_item = models.VaultItem(**item.dict(), user_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/api/vault/{item_id}", response_model=schemas.VaultItem)
def update_vault_item(item_id: int, item: schemas.VaultItemCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_item = db.query(models.VaultItem).filter(models.VaultItem.id == item_id, models.VaultItem.user_id == current_user.id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/vault/{item_id}")
def delete_vault_item(item_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_item = db.query(models.VaultItem).filter(models.VaultItem.id == item_id, models.VaultItem.user_id == current_user.id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted"}

# Folder Endpoints
@app.get("/api/folders", response_model=list[schemas.Folder])
def get_folders(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Folder).filter(models.Folder.user_id == current_user.id).all()

@app.post("/api/folders", response_model=schemas.Folder)
def create_folder(folder: schemas.FolderCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_folder = models.Folder(**folder.dict(), user_id=current_user.id)
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    return db_folder

@app.delete("/api/folders/{folder_id}")
def delete_folder(folder_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_folder = db.query(models.Folder).filter(models.Folder.id == folder_id, models.Folder.user_id == current_user.id).first()
    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    db.delete(db_folder)
    db.commit()
    return {"message": "Folder deleted"}

# Password Generator Endpoint
@app.post("/api/generate-password")
def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_numbers: bool = True,
    use_symbols: bool = True
):
    if length < 4 or length > 128:
        raise HTTPException(status_code=400, detail="Password length must be between 4 and 128")
    
    chars = ""
    if use_uppercase:
        chars += string.ascii_uppercase
    if use_lowercase:
        chars += string.ascii_lowercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    
    if not chars:
        raise HTTPException(status_code=400, detail="At least one character type must be selected")
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return {"password": password}

# Backup Endpoints
@app.get("/api/backup")
def backup_vault(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    vault_items = db.query(models.VaultItem).filter(models.VaultItem.user_id == current_user.id).all()
    folders = db.query(models.Folder).filter(models.Folder.user_id == current_user.id).all()
    
    backup_data = {
        "version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "vault_items": [
            {
                "title": item.title,
                "username_encrypted": item.username_encrypted,
                "password_encrypted": item.password_encrypted,
                "url_encrypted": item.url_encrypted,
                "notes_encrypted": item.notes_encrypted,
                "favorite": item.favorite,
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
            }
            for item in vault_items
        ],
        "folders": [
            {
                "name": folder.name,
            }
            for folder in folders
        ]
    }
    
    return backup_data

@app.post("/api/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
