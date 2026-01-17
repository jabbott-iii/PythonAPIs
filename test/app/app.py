import fastapi
import schemas

app = fastapi.FastAPI()

textposts = {}  

@app.get("/posts")
def get_posts():
    return textposts

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id not in textposts:
        raise fastapi.HTTPException(status_code=404, detail="Post not found")
    return textposts.get(post_id)

@app.post("/posts")
def create_post(post: schemas.PostCreate):
    new_post = {"title": post.title, "content": post.content, "published": post.published}
    textposts[max(textposts.keys(), default=0) + 1] = new_post
    return new_post