# creates a constant single user object so BE behaves as if someone is logged in

from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    username: str
    password_hash: str
    created_at: str
