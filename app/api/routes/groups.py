from fastapi import APIRouter
from app.models.groups import Group, GroupCreate
from app.db.seed.pw import get_connection
from fastapi import HTTPException

router = APIRouter()

@router.get("/groups",response_model=list[Group])
def list_groups():
    con = get_connection()
    con.autocommit = True
    cursor = con.cursor()  
    cursor.execute("SELECT * FROM groups")
    result = cursor.fetchall()
    all_groups = []
    for record in result:
        all_groups.append(
            Group(
                group_id=record[0],
                group_name=record[1],
                organiser_user_id=record[2],
                tmdb_id=record[3],
                episodes_per_week=record[4],
            )
        )

    cursor.close()
    con.close()
    return all_groups


@router.get("/groups/{user_id}", response_model=list[Group])
def list_groups_by_user_id(user_id: int):
    con = get_connection()
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM groups WHERE organiser_user_id = %s",
        (user_id,),
    )

    result = cursor.fetchall()

    all_groups = [
        Group(
            group_id=record[0],
            group_name=record[1],
            organiser_user_id=record[2],
            tmdb_id=record[3],
            episodes_per_week=record[4],
        )
        for record in result
    ]

    cursor.close()
    con.close()
    return all_groups


@router.post("/groups", response_model=Group)
def create_group(group: GroupCreate):
    con = get_connection()
    cursor = con.cursor()

    cursor.execute(
        """
        INSERT INTO groups (
            group_name,
            organiser_user_id,
            tmdb_id,
            episodes_per_week
        )
        VALUES (%s, %s, %s, %s)
        RETURNING group_id
        """,
        (
            group.group_name,
            group.organiser_user_id,
            group.tmdb_id,
            group.episodes_per_week,
        ),
    )

    group_id = cursor.fetchone()[0]

    con.commit()
    cursor.close()
    con.close()

    # Return a full Group object including the generated ID
    return Group(
        group_id=group_id,
        group_name=group.group_name,
        organiser_user_id=group.organiser_user_id,
        tmdb_id=group.tmdb_id,
        episodes_per_week=group.episodes_per_week,
    )



@router.delete("/groups/{group_id}")
def delete_group(group_id: int):
    con = get_connection()
    con.autocommit = True
    cursor = con.cursor()

    # Check if group exists
    cursor.execute(
        "SELECT 1 FROM groups WHERE group_id = %s",
        (group_id,)
    )
    if cursor.fetchone() is None:
        cursor.close()
        con.close()
        raise HTTPException(status_code=404, detail="Group not found")

    # Delete the group
    cursor.execute(
        "DELETE FROM groups WHERE group_id = %s",
        (group_id,)
    )

    cursor.close()
    con.close()

    return {"message": "Group deleted successfully"}
