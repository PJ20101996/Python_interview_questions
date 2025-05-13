from fastapi import APIRouter
from app.endpoints import questions

router = APIRouter()

router.include_router(questions.router)


