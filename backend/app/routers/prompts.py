from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.prompt import Prompt, PromptVersion
from app.routers.auth import require_admin

router = APIRouter(prefix="/api/prompts", tags=["prompts"])


class PromptUpdate(BaseModel):
    content: str


class PromptTestRequest(BaseModel):
    sample_input: str


@router.get("")
def list_prompts(db: Session = Depends(get_db)):
    prompts = db.query(Prompt).order_by(Prompt.key).all()
    return prompts


@router.get("/{key}")
def get_prompt(key: str, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.key == key).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="プロンプトが見つかりません")
    return prompt


@router.put("/{key}")
def update_prompt(key: str, body: PromptUpdate, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    prompt = db.query(Prompt).filter(Prompt.key == key).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="プロンプトが見つかりません")

    # Save version history
    version = PromptVersion(
        prompt_id=prompt.id,
        version=prompt.version,
        content=prompt.content,
    )
    db.add(version)

    prompt.content = body.content
    prompt.version += 1
    db.commit()
    db.refresh(prompt)
    return prompt


@router.get("/{key}/versions")
def list_versions(key: str, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.key == key).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="プロンプトが見つかりません")
    versions = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt.id)
        .order_by(PromptVersion.version.desc())
        .all()
    )
    return versions


@router.post("/{key}/rollback/{version}")
def rollback_prompt(key: str, version: int, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    prompt = db.query(Prompt).filter(Prompt.key == key).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="プロンプトが見つかりません")

    target_version = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_id == prompt.id, PromptVersion.version == version)
        .first()
    )
    if not target_version:
        raise HTTPException(status_code=404, detail="指定バージョンが見つかりません")

    # Save current as version history
    current_version = PromptVersion(
        prompt_id=prompt.id,
        version=prompt.version,
        content=prompt.content,
    )
    db.add(current_version)

    prompt.content = target_version.content
    prompt.version += 1
    db.commit()
    db.refresh(prompt)
    return prompt


@router.post("/{key}/test")
async def test_prompt(key: str, body: PromptTestRequest, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    prompt = db.query(Prompt).filter(Prompt.key == key).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="プロンプトが見つかりません")

    from app.services.llm import call_llm
    result = await call_llm(prompt.content, body.sample_input)
    return {"result": result}
