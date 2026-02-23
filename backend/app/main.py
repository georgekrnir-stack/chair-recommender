from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import aliases, auth, chairs, logs, makers, pipeline, prompts, recommend, videos

app = FastAPI(title="椅子レコメンドAPI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recommend.router)
app.include_router(chairs.router)
app.include_router(aliases.router)
app.include_router(videos.router)
app.include_router(makers.router)
app.include_router(prompts.router)
app.include_router(pipeline.router)
app.include_router(logs.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
