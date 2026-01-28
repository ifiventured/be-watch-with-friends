#from fastapi import FastAPI
#from app.api.routes import health, auth, groups
from fastapi import FastAPI
from app.api.routes import health, groups
#from app.api.routes import watchlist


#app = FastAPI(title="Watch With Friends API")

#app.include_router(health.router, prefix="/api")
#app.include_router(auth.router, prefix="/api")

#app.include_router(watchlist.router, prefix="/api")

from fastapi import FastAPI
from app.db.seed.connection import get_db_connection
from app.db.seed.pw import get_connection



app = FastAPI()
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

