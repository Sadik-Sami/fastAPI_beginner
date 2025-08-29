from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "Title 1",
        "content": "Content 1",
        "published": True,
        "rating": 4,
        "id": 1,
    },
    {
        "title": "Title 2",
        "content": "Content 2",
        "published": True,
        "rating": 4.5,
        "id": 2,
    },
    {
        "title": "Title 3",
        "content": "Content 3",
        "published": True,
        "rating": 3.5,
        "id": 3,
    },
]


def findPost(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def findPostIndex(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"success": True, "data": my_posts}


# @app.post("/posts")
# async def create_post(payload: dict = Body(...)):
# print(payload)


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    # response = {
    #     "Title": new_post.title,
    #     "Content": new_post.content,
    #     "is_Published": new_post.published,
    #     "rating": new_post.rating,
    # }
    return {"data": my_posts}


# @app.get("/posts/{id}")
# async def get_post(id: int, response: Response):
#     post = findPost(id)
#     if not post:
#         # response.status_code = 404
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"post {id} was not found"}
#     return {"post": post}


# Recomended approach
@app.get("/posts/{id}")
async def get_post(id: int):
    post = findPost(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} was not found"
        )
    return {"post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post = findPostIndex(id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} was not found"
        )
    my_posts.pop(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = findPostIndex(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} was not found"
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
