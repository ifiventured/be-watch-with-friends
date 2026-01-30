from fastapi import APIRouter
from app.db.seed.pw import get_connection
from fastapi import HTTPException

router = APIRouter()

con = get_connection()

@router.get("/watchlist")
def get_all_watchlists():
    con = get_connection()
    cursor = con.cursor()
    try:
        cursor.execute("SELECT * FROM watchlist")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
            "watchlist_id": row[0], 
            "user_id": row[1],
            "tmdb_id": row[2],
            "tmdb_name": row[3],
            "poster_url": row[4],
            "added_at": row[5]
            })

        return result
    
    finally:
        cursor.close()
        con.close()

@router.get("/watchlist/{user_id}/{watchlist_id}")
def get_user_watchlist(user_id: int, watchlist_id: int):
    con = get_connection()
    cursor = con.cursor()

    try:
        cursor.execute("SELECT watchlist_id, user_id, tmdb_id, tmdb_name, poster_url, added_at FROM watchlist WHERE watchlist_id = %s", (watchlist_id,))
        row = cursor.fetchone()

        if row is None:
            return {"error": "Watchlist not found"}
    
        return {"watchlist_id": row[0], 
            "user_id": row[1],
            "tmdb_id": row[2],
            "tmdb_name": row[3],
            "poster_url": row[4],
            "added_at": row[5]}

    finally:
        cursor.close()
        con.close()