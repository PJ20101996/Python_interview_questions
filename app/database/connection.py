from pymongo import MongoClient
from app.config.config import settings
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url=settings.mongo_uri
client=MongoClient(mongo_url)
db=client["Python-Interview-Questions"]
candidate_collection=db["candidates"]
question_collection=db["questions"]
response_collection=db["responses"]


