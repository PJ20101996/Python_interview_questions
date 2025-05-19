from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class CandidateRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[int] = None

class CandidateInDB(CandidateRegister):
    _id: str
    registered_at: str
    exam_started_at: Optional[str] = None

class Question(BaseModel):
    question_id: int
    category: str
    type: int  # 1: MCQ, 2: Descriptive, 3: Coding
    text: str
    options: Optional[Dict[str, str]] = None
    level: str

class StartExamResponse(BaseModel):
    candidate_id: str
    mcq_questions: List[Question]
    descriptive_questions: List[Question]
    coding_questions: List[Question]