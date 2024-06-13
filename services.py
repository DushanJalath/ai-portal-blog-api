import json
from uuid import UUID
from fastapi import HTTPException
from bson import ObjectId,json_util
from database import collection_blog, collection_comment, collection_reply
from models import BlogPost, Comment, Reply
from typing import List


def initial_service():
    return {"Ping":"Pong"}


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


async def update_blog(id, title, content, tags):
    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(400, "Invalid Id format")
    
    result = await collection_blog.update_one(
        {"blogPost_id":objId}, 
        {"$set":{"title":title, "content":content, "tags":tags}}
    )

    if result.modified_count == 1:
        blog = await collection_blog.find_one({"blogPost_id":objId})
        return blog
    elif result.modified_count == 0:
        raise HTTPException(404, "Blog not found")
    
    raise HTTPException(400, "Blog update failed")


async def write_comment(comment):
    result = await collection_blog.insert_one(comment)
    if result.inserted_id:
        return comment
    raise HTTPException(400, "Comment Insertion failed")

async def reply_comment(reply):
    result = await collection_blog.insert_one(reply)
    if result.inserted_id:
        return reply
    raise HTTPException(400, "Reply Insertion failed")



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

async def get_blogs_byTags(tags : List[int]):
    blogs=[]
    if collection_blog.count_documents({"tags": {"$in": tags}}) == 0:
        raise HTTPException(status_code=404, detail="no blogs found with the given tags.")
    cursor=collection_blog.find({"tags": {"$in": tags}})
    for document in cursor:
        blogs.append(BlogPost(**document))
    return blogs


async def fetch_replies(parent_content_id: UUID):
    replies_cursor = await collection_reply.find({"parentContent_id": parent_content_id})
    replies = [Reply(**reply) async for reply in replies_cursor]
    
    # Recursively fetch replies for each reply
    for reply in replies:
        reply.replies = await fetch_replies(reply.reply_id)
    
    return replies


async def fetch_comments_and_replies(id: str):
    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(400, "Invalid Id format")
    
    comments_cursor = await collection_comment.find({"blogPost_id": objId})
    comments = [Comment(**comment) async for comment in comments_cursor]
    
    if len(comments)==0 :
        raise HTTPException(404, "Comments not found")
        
    # Fetch replies for each comment
    for comment in comments:
        comment.replies = await fetch_replies(comment.comment_id)
    
    return comments

async def update_Comment_Reply(id:str, text:str):
    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(400, "Invalid Id Format")
    
    #First search in comments collection
    comment = await collection_comment.find_one({"comment_id": objId})
    if comment:
        result = await collection_comment.update_one(
            {"comment_id": objId},
            {"$set": {"text": text}}
        )
        if result.modified_count == 1:
            updated_comment = await collection_comment.find_one({"comment_id": objId})
            return updated_comment
        raise HTTPException(400, "Comment update failed")
    
    #If it is not in comment collection, then search in reply collection
    reply = await collection_reply.find_one({"reply_id":objId})
    if reply:
        result = await collection_reply.update_one(
            {"reply_id":objId},
            {"$set": {"text":text}}
        )
        if result.modified_count == 1:
            updated_reply = await collection_reply.find_one({"reply_id": objId})
            return updated_reply
        raise HTTPException(400, "Reply update failed")
    
    raise HTTPException(404, "Comment or Reply not found")

async def delete_comment_reply(id):
    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(400, "Invalid Id Format")
    
    #First search in comments collection
    comment = await collection_comment.find_one({"comment_id": objId})
    if comment:
        result = await collection_comment.delete_one({'comment_id': objId})

        # Delete all replies associated with the comment
        result_ = await collection_reply.delete_many({'parentContent_id': objId})
        if result.deleted_count == 0:
            raise HTTPException(400, "Comment deletion failed")
        return {"message": "Comment deleted successfully"}
    
    #If it is not in comment collection, then search in reply collection
    reply = await collection_reply.find_one({"reply_id":objId})
    if reply:
        result = await collection_reply.delete_one({'reply_id': objId})

        # Delete all replies associated with the reply
        result_ = await collection_reply.delete_many({'parentContent_id': objId})
        if result.deleted_count == 0:
            raise HTTPException(400, "Reply deletion failed")
        return {"message": "Reply deleted successfully"}
    
    raise HTTPException(404, "Comment or Reply not found")