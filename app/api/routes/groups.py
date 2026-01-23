# from fastapi import APIRouter, Depends
from app.core.deps import get_current_user

router = APIRouter()
# depends is FastAPI dependency system - gives result before running route - parameter must be provided before running
@router.get("/groups")
def list_groups(user=Depends(get_current_user)):
    return {
        "message": "Groups for user",
        "user": user.username
    }
