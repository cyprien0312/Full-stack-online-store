from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.routers.users import router as users_router

app = FastAPI(title="Backend API", version="0.1.0")
logger = logging.getLogger(__name__)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


# Access-Control-Allow-Origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    try:
        db = SessionLocal()
        init_db(db)  # add admin if there is no user
    except Exception as exc:
        logger.exception("Database init failed: %s", exc)
    finally:
        try:
            db.close()
        except Exception as exc:
            logger.exception("Database close failed: %s", exc)


app.include_router(users_router)
