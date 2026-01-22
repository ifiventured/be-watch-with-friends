import json
from pathlib import Path
from app.core.dev_user import User

MOCK_USERS_FILE = Path(__file__).parent / "MOCK_USER_DATA.json"

with open(MOCK_USERS_FILE, "r") as f:
    raw_users = json.load(f)

USERS = [User(**u) for u in raw_users]

USERS_BY_ID = {u.user_id: u for u in USERS}
USERS_BY_USERNAME = {u.username: u for u in USERS}
