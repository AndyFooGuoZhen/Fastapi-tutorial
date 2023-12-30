from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

#Used for data validation when fetching data from db
class PostBase(BaseModel):
    title: str
    content: str
    userid: int

class UserBase(BaseModel):
    username: str


#Dont want to keep connection to db open for too long
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

#Dependency injection
dp_dependency = Annotated[Session, Depends(get_db)]

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: dp_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: dp_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: dp_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: dp_dependency):
    db_user = models.User(**user.dict()) #Deserialize user object into models.User
    db.add(db_user)
    db.commit()
   
@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: dp_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user