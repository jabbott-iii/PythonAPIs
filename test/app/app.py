from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from httpx import post
from . import schemas
from . import db
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

@asynccontextmanager                                                                                # define lifespan event
async def lifespan(app: FastAPI):                                                                   # lifespan event to create database tables on startup
    await db.create_db_and_tables()                                                                 # create database tables
    yield

app = FastAPI(lifespan=lifespan)                                                                    # pass lifespan to FastAPI instance

@app.post("/upload")                                                                               # endpoint to upload a file
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(db.get_async_session)                                           # database session dependency
):
    post = db.Post(                                                                                 # implementation of file upload endpoint goes here
        caption=caption,
        url=f"/files/{file.filename}",
        file_type=file.content_type,
        file_name=file.filename
    )                                                                                            
    session.add(post)                                                                               # add post to session
    await session.commit()                                                                          # commit session to save post
    await session.refresh(post)                                                                     # refresh session to get updated post
    return post                                                                                     # return the created post

@app.get("/feed")                                                                                   # endpoint to get all posts
async def get_feed(
    session: AsyncSession = Depends(db.get_async_session)
):
    result = await session.execute(select(db.Post).order_by(db.Post.created_at.desc()))             # select all posts from database and orders by descending timestamp
    posts = [row[0] for row in result.all()]                                                        # fetch all posts and convert to list

    posts_data = []                                                                                 # convert posts to list of dictionaries
    for post in posts:                                                                              # Defines the dictionary format that will be in the list
        posts_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
        })
        return {"posts": posts_data}