from fastapi import APIRouter
from app.db.seed.pw import get_connection
from fastapi import HTTPException

router = APIRouter()

# @router.post("/groups", response_model=Group)
# def create_group(group: GroupCreate):
#     con = get_connection()
#     cursor = con.cursor()

#     cursor.execute(
#         """
#         INSERT INTO groups (
#             group_name,
#             organiser_user_id,
#             tmdb_id,
#             episodes_per_week
#         )
#         VALUES (%s, %s, %s, %s)
#         RETURNING group_id
#         """,
#         (
#             group.group_name,
#             group.organiser_user_id,
#             group.tmdb_id,
#             group.episodes_per_week,
#         ),
#     )

#     group_id = cursor.fetchone()[0]

#     con.commit()
#     cursor.close()
#     con.close()

#     # Return a full Group object including the generated ID
#     return Group(
#         group_id=group_id,
#         group_name=group.group_name,
#         organiser_user_id=group.organiser_user_id,
#         tmdb_id=group.tmdb_id,
#         episodes_per_week=group.episodes_per_week,
#     )



# @router.delete("/groups/{group_id}")
# def delete_group(group_id: int):
    # con = get_connection()
    # con.autocommit = True
    # cursor = con.cursor()

    # # Check if group exists
    # cursor.execute(
    #     "SELECT 1 FROM groups WHERE group_id = %s",
    #     (group_id,)
    # )
    # if cursor.fetchone() is None:
    #     cursor.close()
    #     con.close()
    #     raise HTTPException(status_code=404, detail="Group not found")

    # # Delete the group
    # cursor.execute(
    #     "DELETE FROM groups WHERE group_id = %s",
    #     (group_id,)
    # )

    # cursor.close()
    # con.close()

    # return {"message": "Group deleted successfully"}



# get all groups

@router.get("/groups/")
def list_groups():
    con = get_connection()
    cursor = con.cursor()

    try:
        cursor.execute(
        """
        SELECT * From groups
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
            "group_id": row[0],
            "group_name": row[1],
            "description": row[2],
            "organiser_user_id": row[3],
            "tmdb_id": row[4],
            "tmdb_name": row[5],
            "poster_url": row[6],
            "start_date": row[7],
            "episodes_per_week": row[8],
            "created_at": row[9],
            })
        return result

    finally:
        cursor.close()
        con.close()

# GET group by group_id using only PG8000

@router.get("/groups/{group_id}")
def get_group(group_id: int):
    con = get_connection()
    cursor = con.cursor()

    try:
        cursor.execute(
        """
        SELECT * FROM groups WHERE group_id = %s
        """,
        (group_id,)
        )
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Group not Found")
    
        return {
            "group_id": row[0],
            "group_name": row[1],
            "description": row[2],
            "organiser_user_id": row[3],
            "tmdb_id": row[4],
            "tmdb_name": row[5],
            "poster_url": row[6],
            "start_date": row[7],
            "episodes_per_week": row[8],
            "created_at": row[9],
        }
    
    finally:
        cursor.close()
        con.close()

# POST groups
# DELETE group
# Group by user_id