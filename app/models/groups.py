from pydantic import BaseModel


class Group(BaseModel):
    group_id: int
    group_name: str
    organiser_user_id: int
    tmdb_id: int
    episodes_per_week: int
                 

class GroupCreate(BaseModel):
    group_name: str
    organiser_user_id: int
    tmdb_id: int
    episodes_per_week: int
