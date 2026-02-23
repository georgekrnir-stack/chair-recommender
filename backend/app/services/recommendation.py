import json

from sqlalchemy.orm import Session

from app.models.chair import Chair
from app.models.prompt import Prompt
from app.models.recommendation_log import RecommendationLog
from app.services.llm import call_llm, call_llm_json


async def generate_recommendation(form_input: str, db: Session) -> dict:
    """Generate chair recommendation from form input."""

    # Step 1: Parse form input
    parse_prompt = db.query(Prompt).filter(Prompt.key == "parse_form", Prompt.is_active.is_(True)).first()
    if not parse_prompt:
        return {"error": "フォームパースプロンプトが設定されていません"}

    parsed_result = await call_llm_json(parse_prompt.content, form_input)
    try:
        parsed_conditions = json.loads(parsed_result)
    except json.JSONDecodeError:
        parsed_conditions = {"raw": parsed_result}

    # Step 2: Get recommendable chairs
    chairs = db.query(Chair).filter(Chair.is_recommendable.is_(True)).all()
    chairs_data = [
        {
            "id": str(c.id),
            "name": c.canonical_name,
            "maker": c.maker,
            "price_range": c.price_range,
            "features": c.features,
            "target_users": c.target_users,
            "pros": c.pros,
            "cons": c.cons,
            "comparison_notes": c.comparison_notes,
        }
        for c in chairs
    ]

    # Step 3: Filter candidates
    filter_prompt = db.query(Prompt).filter(Prompt.key == "filter_candidates", Prompt.is_active.is_(True)).first()
    if not filter_prompt:
        return {"error": "フィルタリングプロンプトが設定されていません"}

    filter_input = json.dumps(
        {"conditions": parsed_conditions, "chairs": chairs_data}, ensure_ascii=False
    )
    filter_result = await call_llm_json(filter_prompt.content, filter_input)

    try:
        candidates = json.loads(filter_result)
    except json.JSONDecodeError:
        candidates = chairs_data[:3]

    # Step 4: Generate recommendation text
    gen_prompt = db.query(Prompt).filter(
        Prompt.key == "generate_recommendation", Prompt.is_active.is_(True)
    ).first()
    if not gen_prompt:
        return {"error": "推薦文生成プロンプトが設定されていません"}

    gen_input = json.dumps(
        {"conditions": parsed_conditions, "candidates": candidates}, ensure_ascii=False
    )
    response_text = await call_llm(gen_prompt.content, gen_input)

    # Step 5: Save recommendation log
    recommended_ids = [c.get("id") for c in (candidates if isinstance(candidates, list) else candidates.get("candidates", []))]
    log = RecommendationLog(
        form_input=form_input,
        parsed_conditions=parsed_conditions,
        recommended_chair_ids=recommended_ids,
        response_text=response_text,
    )
    db.add(log)
    db.commit()

    return {
        "response_text": response_text,
        "parsed_conditions": parsed_conditions,
        "recommended_chair_ids": recommended_ids,
    }
