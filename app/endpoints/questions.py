from fastapi import APIRouter, Depends, HTTPException
from app.models.users import CandidateRegister
from datetime import datetime
from app.database.connection import candidate_collection
from fastapi import Body

# define the routers
router =APIRouter(prefix="/interview_questions", tags=["users"], responses={404:{"description":"Not Found"}})

@router.post("/register_candidate")

async def register_candidate(candidate:CandidateRegister):
    """
    Register a new candidate.
    """
    existing_candidate=candidate_collection.find_one({"email":candidate.email})
    if existing_candidate:
        return{
            "message":"Candidate already registered",
            "candidate_email":existing_candidate["email"],
            "candidate_name":existing_candidate["first_name"]
        }
    # check if the candidate already exists
    candidate_data={
        **candidate.dict(),
        "registered_at":datetime.utcnow(),
        "exam_started_at":None
    }

    candidate_collection.insert_one(candidate_data)
    
    return {
        "message":"Candidate registered successfully",
         "candidate_email":candidate.email,
          "candidate_name":candidate.first_name
          }

@router.post("/start_exam")

async def start_exam(email:str=Body(..., embed=True)):
    """
    Start the exam for a candidate.
    """
    candidate=candidate_collection.find_one({"email":email})
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    if candidate.get("exam_started_at"):
        raise HTTPException(status_code=400, detail="Exam already started")
    
    candidate_collection.update_one({"email":email},{"$set":{"exam_started_at":datetime.utcnow()}})
    return {"message":"Exam started successfully"}