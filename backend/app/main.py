from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Backend API", version="0.1.0")


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