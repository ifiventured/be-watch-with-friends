import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path(__file__).parent.parent / "data"
WATCHLIST_FILE = DATA_DIR / "mock_watchlist.json"


@dataclass
class MockWatchlistRow:
    watchlist_id: int
    user_id: int
    tmdb_id: int
    added_at: str 


def load_mock_watchlist() -> List[MockWatchlistRow]:
    with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [MockWatchlistRow(**row) for row in raw]


MOCK_WATCHLIST: List[MockWatchlistRow] = load_mock_watchlist()

WATCHLIST_BY_USER_ID: Dict[int, List[MockWatchlistRow]] = {}
for row in MOCK_WATCHLIST:
    WATCHLIST_BY_USER_ID.setdefault(row.user_id, []).append(row)
