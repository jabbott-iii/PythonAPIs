import pydantic

class PostCreate(pydantic.BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(pydantic.BaseModel):
    title: str
    content: str
    published: bool = True