import pydantic

class PostCreateSchema(pydantic.BaseModel):
    title: str
    content: str
    published: bool = True