from fastapi import HTTPException
from database import collection_blog

def initial_service():
    return {"Ping":"Pong"}

async def create_blog(blog):
    result = await collection_blog.insert_one(blog)
    return blog

async def update_blog(id, title, content):
    await collection_blog.update_one(
        {"blogPost_id":id}, 
        {"$set":{"title":title, "content":content}}
    )
    blog = await collection_blog.find_one({"blogPost_id":id})
    return blog