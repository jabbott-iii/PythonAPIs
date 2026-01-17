from pydantic import BaseModel

class PostCreate(BaseModel):                                             # schema for creating a post
    title: str                                                           # title of the post
    content: str                                                         # content of the post
    published: bool = True                                               # published status, defaults to True

class PostResponse(BaseModel):                                           # schema for responding with a post
    title: str                                                           # title of the post
    content: str                                                         # content of the post
    published: bool = True                                               # published status, defaults to True