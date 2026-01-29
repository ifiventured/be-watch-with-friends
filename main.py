
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.groups import router as groups_router
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

con = get_connection()

@app.get("/")

def root():

    return {"message": "Hello World"}

@app.get("/user/me")
def get_user_me():
    return {"user_id": "the current user"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    con = get_db_connection()
    cursor = con.cursor()

    cursor.execute("SELECT user_id, username FROM Users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()

    cursor.close()
    con.close()

    if row is None:
        return {"error": "User not found"}

    return {"user_id": row[0], "username": row[1]}

    #return {"user_id": user_id, "username": username}


#, username: str | None = None

