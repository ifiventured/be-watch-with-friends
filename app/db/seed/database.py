from .pw import get_connection
import json
from datetime import datetime

con = get_connection()
con.autocommit = True
cursor = con.cursor()

with open("app/db/test_data/MOCK_USER_DATA.json", "r") as userfile:
    data_user = json.load(userfile)

with open("app/db/test_data/MOCK_GROUP_DATA.json", "r") as groupfile:
    data_group = json.load(groupfile)

with open("app/db/test_data/MOCK_WATCHLIST_DATA.json", "r") as watchlistfile:
    data_watchlist = json.load(watchlistfile)

with open("app/db/test_data/MOCK_GROUP_MEMBER_DATA.json", "r") as grmemberfile:
    data_grmember = json.load(grmemberfile)

with open("app/db/test_data/MOCK_SCHEDULE_DATA.json", "r") as grschedulefile:
    data_grschedule = json.load(grschedulefile)

db_name = "BEUserDatabase"
cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
cursor.execute(f'CREATE DATABASE {db_name}')

cursor.execute("DROP TABLE IF EXISTS Users CASCADE")
cursor.execute("DROP TABLE IF EXISTS Watchlist CASCADE")
cursor.execute("DROP TABLE IF EXISTS Groups CASCADE")
cursor.execute("DROP TABLE IF EXISTS GroupMembers CASCADE")
cursor.execute("DROP TABLE IF EXISTS GroupSchedule CASCADE")

cursor.execute("""
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY, 
        username VARCHAR NOT NULL UNIQUE, 
        created_at DATE DEFAULT CURRENT_DATE
       )
""")

cursor.execute("""
    CREATE TABLE Watchlist (
        watchlist_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        tmdb_id INT NOT NULL,
        tmdb_name VARCHAR NOT NULL,
        poster_url VARCHAR NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
""")
cursor.execute("""
    CREATE TABLE Groups (
        group_id SERIAL PRIMARY KEY,
        group_name VARCHAR NOT NULL,
        description TEXT NULL,
        organiser_user_id INT NOT NULL,
        tmdb_id INT,
        tmdb_name VARCHAR NOT NULL,
        poster_url VARCHAR NOT NULL,
        start_date DATE NULL,       
        episodes_per_week INT,
        created_at DATE DEFAULT CURRENT_DATE      
        )           
""")

cursor.execute("""
    CREATE TABLE GroupMembers (
        group_id INT NOT NULL,
        user_id INT NOT NULL,
        role VARCHAR NOT NULL,
        joined_at DATE DEFAULT CURRENT_DATE
        )           
""")

cursor.execute("""
    CREATE TABLE GroupSchedule (
        schedule_id SERIAL PRIMARY KEY,
        group_id INT NOT NULL,
        episode_number INT NOT NULL,
        due_date DATE DEFAULT CURRENT_DATE
        )           
""")

for user in data_user:
    created_at = datetime.strptime(user["created_at"], "%d/%m/%Y").date()
    cursor.execute("""INSERT INTO Users (user_id, username, created_at)
                   VALUES (%s, %s, %s)
                   """, 
                   (user["user_id"], user["username"], created_at))


for group in data_group:
    start_date = datetime.strptime(group["start_date"], "%d/%m/%Y").date()
    created_at = datetime.strptime(group["created_at"], "%d/%m/%Y").date()
    cursor.execute("""INSERT INTO Groups (group_id, group_name, description, organiser_user_id, tmdb_id, tmdb_name, poster_url, start_date, episodes_per_week, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                   """, 
                   (group["group_id"], group["group_name"], group["description"], group["organiser_user_id"], group["tmdb_id"], group["tmdb_name"], group["poster_url"], start_date, group["episodes_per_week"], created_at))


for watchlist in data_watchlist:
    added_at = datetime.strptime(watchlist["added_at"], "%m/%d/%Y").date()
    cursor.execute("""INSERT INTO Watchlist (watchlist_id, user_id, tmdb_id, tmdb_name, poster_url, added_at)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """, 
                   (watchlist["watchlist_id"], watchlist["user_id"], watchlist["tmdb_id"], watchlist["tmdb_name"], watchlist["poster_url"], added_at))


for grmember in data_grmember:
    joined_at = datetime.strptime(grmember["joined_at"], "%d/%m/%Y").date()
    cursor.execute("""INSERT INTO GroupMembers (group_id, user_id, role, joined_at)
                   VALUES (%s, %s, %s, %s)
                   """, 
                   (grmember["group_id"], grmember["user_id"], grmember["role"], joined_at))
        
for grschedule in data_grschedule:
    due_date = datetime.strptime(grschedule["due_date"], "%m/%d/%Y").date()
    cursor.execute("""INSERT INTO GroupSchedule (schedule_id, group_id, episode_number, due_date)
                   VALUES (%s, %s, %s, %s)
                   """, 
                   (grschedule["schedule_id"], grschedule["group_id"],  grschedule["episode_number"], due_date))
        
tables = ["Groups", "GroupMembers", "Watchlist", "Users", "GroupSchedule"]

cursor.close
con.close