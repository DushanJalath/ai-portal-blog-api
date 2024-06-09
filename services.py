from bson import ObjectId
from fastapi import HTTPException
from database import collection_blog


def initial_service():
    return {"Ping": "Pong"}


def get_all_blogs():
    # TODO: correct project fields should be added - rtw
    blogs = collection_blog.aggregate([
        {
            '$project': {
                'id': {
                    '$toString': '$_id'  # Convert ObjectId to string at DB level
                },
                '_id': 0,  # 0 means 'exclude this field from the result'
                'title': 1,
                'body': 1
            }
        }
    ])
    if blogs is None:
        return []
    return list(blogs)


def delete_blog_by_id(id: str):
    result = collection_blog.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
