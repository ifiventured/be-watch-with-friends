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

    # needs a get, delete and patch 