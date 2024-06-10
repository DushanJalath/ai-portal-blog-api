from fastapi import HTTPException
from database import collection_blog
from models import BlogPost

def initial_service():
    return {"Ping":"Pong"}

def get_blogs_byTags(tags):
    blogs=[]
    if collection_blog.count_documents({"tags": tags}) == 0:
        raise HTTPException(status_code=404, detail="no blogs found with the given tags.")
    cursor=collection_blog.find({"tags":tags})
    for document in cursor:
        blogs.append(BlogPost(**document))
    return blogs
