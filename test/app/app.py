from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from . import schemas
from . import db
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from . import images
import imagekitio
import os
import uuid
import shutil
import tempfile

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
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:      # create temporary file
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)                                               # copy uploaded file to temporary file

        upload_response = images.imagekit.files.upload(                                              # upload file to ImageKit
            file = open(temp_file_path, "rb"),
            file_name = file.filename
            )

        if upload_response.http_status == 200:                                                              # ensure upload succeeded
            post = db.Post(                                                                                 # implementation of file upload endpoint goes here
                caption = caption,
                url = upload_response.url,
                file_type = "video" if file.content_type.startswith("video/") else "image",
                file_name = upload_response.name
    )
        else:
            raise HTTPException(status_code=500, detail="Failed to upload file to ImageKit")
        
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            file.file.close()                                                             # close uploaded file
            os.remove(temp_file_path)                                                                       # remove temporary file                                                                  
    
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