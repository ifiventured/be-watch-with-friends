from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.core.mock_watchlist import WATCHLIST_BY_USER_ID

router = APIRouter(tags=["watchlist"])

@router.get("/watchlist")
#ask fastApi for the current userthen returns that user’s watchlist from the lookup dictionary
def list_watchlist(user=Depends(get_current_user)):
    return WATCHLIST_BY_USER_ID.get(user.user_id, [])
 