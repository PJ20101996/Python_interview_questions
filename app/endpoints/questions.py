from fastapi import APIRouter, HTTPException
from app.models.users import CandidateRegister, StartExamResponse, Question
from datetime import datetime
from app.database.connection import candidate_collection, question_collection
from fastapi import Body
from bson import ObjectId
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interview_questions", tags=["users"], responses={404: {"description": "Not Found"}})

@router.post("/register_candidate")
async def register_candidate(candidate: CandidateRegister):
    """Register a candidate, checking for existing email."""
    # Check for existing candidate by email
    existing_candidate = candidate_collection.find_one({"email": candidate.email})
    if existing_candidate:
        logger.info(f"Existing candidate found: {existing_candidate}")
        return {
            "message": "Candidate already registered",
            "candidate_id": str(existing_candidate["_id"]),
            "candidate_name": existing_candidate["first_name"]
        }

    # Register new candidate
    candidate_data = {
        "first_name": candidate.first_name,
        "last_name": candidate.last_name,
        "email": candidate.email,
        "phone_number": candidate.phone_number,
        "registered_at": datetime.utcnow().isoformat(),
        "exam_started_at": None
    }
    result = candidate_collection.insert_one(candidate_data)
    candidate_id = str(result.inserted_id)
    logger.info(f"New candidate registered: {candidate_data}, _id: {candidate_id}")
    return {
        "message": "Candidate registered successfully",
        "candidate_id": candidate_id,
        "candidate_name": candidate.first_name
    }

@router.get("/start_exam", response_model=StartExamResponse)
async def start_exam(candidate_id: str = Body(..., embed=True)):
    """Start the exam and return all 45 MCQs, 12 Descriptive, and 3 Coding questions."""
    try:
        candidate = candidate_collection.find_one({"_id": ObjectId(candidate_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid candidate_id format")
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    if candidate.get("exam_started_at"):
        raise HTTPException(status_code=400, detail="Exam already started")
    
    # Mark exam as started
    candidate_collection.update_one(
        {"_id": ObjectId(candidate_id)},
        {"$set": {"exam_started_at": datetime.utcnow().isoformat()}}
    )
    
    # Fetch all questions
    mcq_questions = question_collection.find({"type": 1})  # 45 MCQs
    descriptive_questions = question_collection.find({"type": 2})  # 12 Descriptive
    coding_questions = question_collection.find({"type": 3})  # 3 Coding
    
    return StartExamResponse(
        candidate_id=candidate_id,
        mcq_questions=[
            {
                "question_id": q["question_id"],
                "category": q["category"],
                "type": q["type"],
                "text": q["text"],
                "options": q.get("options"),
                "level": q["level"]
            } for q in mcq_questions
        ],
        descriptive_questions=[
            {
                "question_id": q["question_id"],
                "category": q["category"],
                "type": q["type"],
                "text": q["text"],
                "options": None,
                "level": q["level"]
            } for q in descriptive_questions
        ],
        coding_questions=[
            {
                "question_id": q["question_id"],
                "category": q["category"],
                "type": q["type"],
                "text": q["text"],
                "options": None,
                "level": q["level"]
            } for q in coding_questions
        ]
    )