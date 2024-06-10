import json
from fastapi import HTTPException
from bson import json_util
from database import collection_blog

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