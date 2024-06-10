from fastapi import HTTPException
from database import collection_blog
from models import BlogPost

def initial_service():
    return {"Ping":"Pong"}

def get_blogs_byTags(tags):
    blogs=[]
    cursor=collection_blog.find({"tags":tags})
    for document in cursor:
        blogs.append(BlogPost(**document))
    
    if not blogs:  # if the blogs list is empty
        return [{"message": "No blogs found for these tags"}]
    else:
        return blogs
