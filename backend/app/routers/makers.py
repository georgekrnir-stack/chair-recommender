import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.maker_product import MakerProduct, MakerScrapeConfig

router = APIRouter(prefix="/api/makers", tags=["makers"])


class ScrapeConfigCreate(BaseModel):
    maker: str
    url: str
    scrape_method: str | None = None


class ScrapeConfigUpdate(BaseModel):
    maker: str | None = None
    url: str | None = None
    scrape_method: str | None = None


@router.get("")
def list_makers(db: Session = Depends(get_db)):
    configs = db.query(MakerScrapeConfig).order_by(MakerScrapeConfig.maker).all()
    return configs


@router.get("/{maker}/products")
def list_maker_products(maker: str, db: Session = Depends(get_db)):
    products = db.query(MakerProduct).filter(MakerProduct.maker == maker).order_by(MakerProduct.product_name).all()
    return products


@router.post("/scrape")
async def scrape_makers(db: Session = Depends(get_db)):
    # TODO: Implement actual scraping logic
    return {"message": "スクレイピングを開始しました（未実装）"}


@router.post("/configs")
def create_config(body: ScrapeConfigCreate, db: Session = Depends(get_db)):
    config = MakerScrapeConfig(**body.model_dump())
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


@router.put("/configs/{config_id}")
def update_config(config_id: uuid.UUID, body: ScrapeConfigUpdate, db: Session = Depends(get_db)):
    config = db.query(MakerScrapeConfig).filter(MakerScrapeConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="設定が見つかりません")
    for key, value in body.model_dump(exclude_none=True).items():
        setattr(config, key, value)
    db.commit()
    db.refresh(config)
    return config
