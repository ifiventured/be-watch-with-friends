# defines hard coded fake user
from dataclasses import dataclass
# data container
@dataclass
#minimal user representation: just user id and username - we can add everything else after
class User:
    user_id: str
    username: str
#hard coded dev user
DEV_USER = User(
    user_id="dev-user-1",
    username="devuser"
)
