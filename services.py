from fastapi import HTTPException
from database import collection_blog
from models import BlogPost
from typing import List

def initial_service():
    return {"Ping":"Pong"}

def get_blogs_byTags(tags : List[int]):
    blogs=[]
    if collection_blog.count_documents({"tags": {"$in": tags}}) == 0:
        raise HTTPException(status_code=404, detail="no blogs found with the given tags.")
    cursor=collection_blog.find({"tags": {"$in": tags}})
    for document in cursor:
        blogs.append(BlogPost(**document))
    return blogs
