from pymongo import MongoClient
from bson import json_util
import json
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://AIPortalBlogAdmin:3F45Tohxct3jb2Ih@email.vm8njwj.mongodb.net/')
database = client.AIPortalBlog

collection_user = database["User"]
collection_blog = database["Blogs"]
collection_comment = database["Comments"]
collection_reply = database["Replies"]

async def get_blog_by_id(entity_id: int):
    try:
        entity = await collection_blog.find_one({"p_id": entity_id})
        if entity is None:
            return None
        else:
            json_data = json.loads(json_util.dumps(entity))
            return json_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

