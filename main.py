
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.groups import router as groups_router
from app.api.routes.users import router as users_router
from app.api.routes.watchlist1 import router as watchlist_router
#from app.api.routes import watchlist
#app = FastAPI(title="Watch With Friends API")
#app.include_router(watchlist.router, prefix="/api")

from fastapi import FastAPI
from app.db.seed.connection import get_db_connection
from app.db.seed.pw import get_connection


app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(groups_router)
app.include_router(users_router)
app.include_router(watchlist_router)

con = get_connection()

@app.get("/")

def root():

    return {"message": "Hello World"}

