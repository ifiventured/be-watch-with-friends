from fastapi import APIRouter, Request, HTTPException
from app.db.seed.pw import get_connection
from app.dependencies import get_current_user


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
@router.post("/groups/")
def create_group(data: dict):
    group_name = data["group_name"]
    description = data.get("description")
    organiser_user_id = get_current_user()

    con = get_connection()
    cursor = con.cursor()

    if not group_name:
        raise HTTPException(status_code = 422, detail="group_name is essential")

    try:
        cursor.execute(
            """
            INSERT INTO groups (
                group_name,
                description,
                organiser_user_id
            )
            VALUES (
                %s,
                %s,
                %s
            )
            RETURNING
                group_id,
                group_name,
                description,
                organiser_user_id,
                tmdb_id,
                tmdb_name,
                poster_url,
                start_date,
                episodes_per_week,
                created_at
            """, 
            (
                group_name,
                description,
                organiser_user_id,
            ),
        )

        row = cursor.fetchone()
        con.commit()

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

# PATCH group
@router.patch("/groups/{group_id}")
def add_show_and_schedule(group_id: int, data: dict):
    tmdb_id = data["tmdb_id"]
    start_date = data["start_date"]
    episodes_per_week = data["episodes_per_week"]

    con = get_connection()
    cursor = con.cursor()

    try:
        cursor.execute(
            """
            UPDATE groups
            SET 
                tmdb_id = %s,
                start_date = %s,
                episodes_per_week = %s
            WHERE
                group_id = %s
            RETURNING
                group_id,
                group_name,
                description,
                organiser_user_id,
                tmdb_id,
                tmdb_name,
                poster_url,
                start_date,
                episodes_per_week,
                created_at
            """,
            (
                tmdb_id,
                start_date,
                episodes_per_week,
                group_id
            ),
        )

        row = cursor.fetchone()
        con.commit()

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

# DELETE group
# Group by user_id
