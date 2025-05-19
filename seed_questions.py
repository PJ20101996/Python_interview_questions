from pymongo import MongoClient
from app.config.config import settings
from app.database.connection import question_collection
import json

# Load JSON file
with open(r"C:\Users\jagadishpagolu\python_interview_web_application\app\data\python_questions.json", 'r') as f:
    questions = json.load(f)

def seed_questions():
    try:
        for question in questions:
            question_collection.update_one(
                {"question_id": question["question_id"]},
                {"$set": question},
                upsert=True
            )
        print(f"Successfully processed {len(questions)} questions.")
    except Exception as e:
        print(f"Error processing questions: {str(e)}")

if __name__ == "__main__":
    seed_questions()