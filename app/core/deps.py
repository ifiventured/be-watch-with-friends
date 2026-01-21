# temp holder for a logged in user -wil be replaced when we have auth sorted
# gives fastapi the function that will always returns the temporary user written in the dev_user file
from app.core.dev_user import DEV_USER

def get_current_user():
    # again, temp for now, we'll add the token auth logic later
    return DEV_USER
