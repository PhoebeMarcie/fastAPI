from typing import Optional
from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time




app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True



my_posts = [{"title":"post 1", "content":"post 1 content","id":1},{"title":"post 2", "content":"post 2 content","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def find_index_post(id):
    for i ,p in enumerate(my_posts):
        if p ['id']==id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    # print(posts)
    return{"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) 
                   VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id:int, response:Response):
    print(id)
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
   
    # post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return {"data":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    # index = find_index_post(id)
    if  deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts  SET title = %s, content=%s, published=%s WHERE id = %s RETURNING * """, (post.title, post.content,post.published,str(id)),)
    updated_post = cursor.fetchone()
    conn.commit()
    index = find_index_post(id)
    # if index == None:
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # post_dict= post.dict()
    # post_dict['id']=id
    # my_posts[index] = post_dict
    # print(post)
    # return {"message":post_dict}
    return{"data": updated_post}



