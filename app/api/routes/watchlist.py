from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.deps import get_current_user
from app.core.watchlist_store import watchlist_store

router = APIRouter(tags=["watchlist"])


class WatchlistCreateBody(BaseModel):
    title: str
    tmdb_id: int
    media_type: str = Field(pattern="^(movie|tv)$")


@router.post("/watchlist", status_code=201)
def add_to_watchlist(body: WatchlistCreateBody, user=Depends(get_current_user)):
    item = watchlist_store.add_item(
        user_id=user.user_id,
        title=body.title,
        tmdb_id=body.tmdb_id,
        media_type=body.media_type,
    )
    return item

@router.get("/watchlist")
def list_watchlist(user=Depends(get_current_user)):
    return watchlist_store.list_items(user.user_id)


@router.delete("/watchlist/{item_id}")
def remove_from_watchlist(item_id: str, user=Depends(get_current_user)):
    removed = watchlist_store.remove_item(user.user_id, item_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}


@router.patch("/watchlist/{item_id}/complete")
def mark_complete(item_id: str, user=Depends(get_current_user)):
    item = watchlist_store.mark_complete(user.user_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item