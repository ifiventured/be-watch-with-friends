from fastapi import FastAPI
from app.api.routes import health, auth, groups

app = FastAPI(title="Watch With Friends API")

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(groups.router, prefix="/api")