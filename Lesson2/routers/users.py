from fastapi import APIRouter
from schemas.user import UserResponse, UserCreate, FeedbackResponse, FeedbackMessage

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
async def RegisterUser(user: UserCreate):
    return user

@router.post("/feedback", response_model=FeedbackResponse)
async def RegisterFeedback(feedback: FeedbackMessage):
    return feedback