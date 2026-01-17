from fastapi import FastAPI, HTTPException
from . import schemas
from . import db
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager                                                                                # define lifespan event
async def lifespan(app: FastAPI):                                                                   # lifespan event to create database tables on startup
    await db.create_db_and_tables()                                                                 # create database tables
    yield

app = FastAPI(lifespan=lifespan)                                                                    # pass lifespan to FastAPI instance

textposts = {}                                                                                      # in-memory storage for text posts

@app.get("/posts")                                                                                  # get all posts
def get_posts():
    return textposts

@app.get("/posts/{post_id}")                                                                        # get specific post by id
def get_post(post_id: int) -> schemas.PostResponse:                                                 # specify response model to avoid returning extra data
    if post_id not in textposts:                                                                    # check if post exists
        raise HTTPException(status_code=404, detail="Post not found")                               # raise 404 if not found
    return textposts.get(post_id)                                                                   # return the requested post

@app.post("/posts")                                                                                 # create a new post
def create_post(post: schemas.PostCreate) -> schemas.PostResponse:                                  # specify response model to avoid returning extra data
    new_post = {"title": post.title, "content": post.content, "published": post.published}          # create new post dictionary
    textposts[max(textposts.keys(), default=0) + 1] = new_post                                      # add new post to in-memory storage with incremented id
    return new_post                                                                                 # return the newly created post