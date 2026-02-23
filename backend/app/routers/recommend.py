from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.recommendation import generate_recommendation

router = APIRouter(prefix="/api/recommend", tags=["recommend"])


class RecommendRequest(BaseModel):
    form_input: str


@router.post("")
async def recommend(body: RecommendRequest, db: Session = Depends(get_db)):
    result = await generate_recommendation(body.form_input, db)
    return result
