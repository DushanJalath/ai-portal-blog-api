from pymongo import MongoClient

client=MongoClient('mongodb+srv://AIPortalBlogAdmin:3F45Tohxct3jb2Ih@email.vm8njwj.mongodb.net/')

database=client.AIPortalBlog

collection_user=database["User"]
collection_blog=database["Blogs"]
collection_comment=database["Comments"]
collection_reply=database["Replies"]