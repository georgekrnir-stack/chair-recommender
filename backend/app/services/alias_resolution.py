import json

from sqlalchemy.orm import Session

from app.models.alias import ChairAlias
from app.models.chair import Chair
from app.models.extraction_log import ExtractionLog
from app.models.maker_product import MakerProduct
from app.models.prompt import Prompt
from app.services.llm import call_llm_json


async def cluster_and_resolve(db: Session) -> dict:
    """Cluster extraction logs and resolve aliases."""
    # Get all unresolved mentions
    unresolved = db.query(ExtractionLog).filter(ExtractionLog.status == "unresolved").all()
    if not unresolved:
        return {"message": "未解決の言及はありません"}

    # Get existing chairs and maker products for reference
    chairs = db.query(Chair).all()
    products = db.query(MakerProduct).all()

    prompt = db.query(Prompt).filter(Prompt.key == "cluster_aliases", Prompt.is_active.is_(True)).first()
    if not prompt:
        return {"error": "クラスタリングプロンプトが設定されていません"}

    # Build input data
    mentions_data = [{"id": str(log.id), "mention": log.raw_mention, "context": log.context} for log in unresolved]
    chairs_data = [{"id": str(c.id), "name": c.canonical_name, "maker": c.maker} for c in chairs]
    products_data = [{"maker": p.maker, "name": p.product_name, "model": p.model_number} for p in products]

    input_text = json.dumps(
        {"mentions": mentions_data, "existing_chairs": chairs_data, "maker_products": products_data},
        ensure_ascii=False,
    )

    result = await call_llm_json(prompt.content, input_text)

    try:
        clusters = json.loads(result)
    except json.JSONDecodeError:
        return {"error": "LLMの出力をパースできませんでした", "raw": result}

    return {"clusters": clusters}
