import json
from fastapi import HTTPException
from bson import ObjectId,json_util
from database import collection_blog

def initial_service():
    return {"Ping": "Pong"}


async def get_blog_by_id(entity_id: int):
    try:
        entity = await collection_blog.find_one({"p_id": entity_id})
        if entity is None:
            return {"message": f"Blog with id {entity_id} not found"}
        else:
            json_data = json.loads(json_util.dumps(entity))
            return json_data
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def create_blog(blog):
    result = await collection_blog.insert_one(blog)
    if result.inserted_id:
        return blog
    raise HTTPException(400, "Blog Insertion failed")


async def update_blog(id, title, content):
    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(400, "Invalid Id format")
    
    result = await collection_blog.update_one(
        {"blogPost_id":objId}, 
        {"$set":{"title":title, "content":content}}
    )

    if result.modified_count == 1:
        blog = await collection_blog.find_one({"blogPost_id":objId})
        return blog
    elif result.modified_count == 0:
        raise HTTPException(404, "Blog not found")
    
    raise HTTPException(400, "Blog update failed")


async def get_all_blogs():
    # function need to be async to use 'async for' loop
    blogs = []
    cursor = collection_blog.find({})
    async for blog in cursor:
        blog["blogPost_id"] = str(blog["_id"])
        del blog["_id"]
        blogs.append(blog)
    if len(blogs) == 0:
        raise HTTPException(404, "No blogs found")
    return blogs
    

async def delete_blog_by_id(id: str):
    result = await collection_blog.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return {"message": "Blog deleted successfully"}
