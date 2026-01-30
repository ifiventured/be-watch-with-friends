from fastapi import APIRouter
from app.db.seed.pw import get_connection
from fastapi import HTTPException

router = APIRouter()

@router.get("/user/me")
def get_user_me():
    return {"user_id": "the current user"}

@router.get("/user/{user_id}")
def get_user(user_id: int):
    con = get_connection()
    cursor = con.cursor()

    try:
        cursor.execute("SELECT user_id, username FROM Users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()

        if row is None:
            return {"error": "User not found"}

        return {
            "user_id": row[0],
            "username": row[1]
            }
    
    finally:
        cursor.close()
        con.close()

    

