#__init__ python constructor - birth of an object

from dataclasses import dataclass
#for readability
from typing import Dict
# creates unique ids
import uuid

@dataclass
class WatchlistItem:
    id: str
    title: str
    tmdb_id: int
    # for film or tv
    media_type: str
    completed: bool = False

#self is how a class refers to its own data
# dict is similar to Map in JavaScript
class WatchlistStore:
    def __init__(self):
        self.items_by_user: Dict[str, Dict[str, WatchlistItem]] = {}

    def add_item(self, user_id: str, title: str, tmdb_id: int, media_type: str):
        item_id = str(uuid.uuid4())
        item = WatchlistItem(
            id=item_id,
            title=title,
            tmdb_id=tmdb_id,
            media_type=media_type,
        )

        if user_id not in self.items_by_user:
            self.items_by_user[user_id] = {}

        self.items_by_user[user_id][item_id] = item
        return item

    def list_items(self, user_id: str):
        return list(self.items_by_user.get(user_id, {}).values())

    def remove_item(self, user_id: str, item_id: str):
        return self.items_by_user.get(user_id, {}).pop(item_id, None)

    def mark_complete(self, user_id: str, item_id: str):
        item = self.items_by_user.get(user_id, {}).get(item_id)
        if item:
            item.completed = True
        return item


watchlist_store = WatchlistStore()
