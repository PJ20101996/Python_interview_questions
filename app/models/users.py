from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CandidateRegister(BaseModel):
    first_name:str
    last_name:str
    email:str
    phone_number:int

class CandidateInDB(CandidateRegister):
    registered_at:str
    exam_started_at:Optional[datetime]=None