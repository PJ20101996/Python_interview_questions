from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url=os.getenv("MONGO_URL")
client=MongoClient(mongo_url)
db=client["Python-Interview-Questions"]
candidate_collection=db["candidates"]

