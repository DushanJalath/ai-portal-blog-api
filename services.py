import json
from fastapi import HTTPException
from bson import json_util
from database import collection_blog

def initial_service():
    return {"Ping":"Pong"}


async def get_blog_by_id(entity_id: int):
    entity = await collection_blog.find_one({"p_id": entity_id})
    if entity is None:
        return None
    else:
        json_data = json.loads(json_util.dumps(entity))
        return json_data
