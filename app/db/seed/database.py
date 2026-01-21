from pw import get_connection
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

db_name = "BEUserDatabase"
cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
cursor.execute(f'CREATE DATABASE {db_name}')

cursor.execute("DROP TABLE IF EXISTS Users CASCADE")
cursor.execute("DROP TABLE IF EXISTS Watchlist CASCADE")
cursor.execute("DROP TABLE IF EXISTS Groups CASCADE")
cursor.execute("DROP TABLE IF EXISTS GroupMembers CASCADE")

cursor.execute("""
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY, 
        username VARCHAR NOT NULL UNIQUE, 
        password_hash VARCHAR,
        created_at DATE DEFAULT CURRENT_DATE
       )
""")

cursor.execute("""
    CREATE TABLE Watchlist (
        watchlist_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        tmdb_id INT NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
""")
cursor.execute("""
    CREATE TABLE Groups (
        group_id SERIAL PRIMARY KEY,
        group_name VARCHAR NOT NULL UNIQUE,
        organiser_user_id INT NOT NULL,
        tmdb_id INT,
        episodes_per_week INT
        )           
""")

cursor.execute("""
    CREATE TABLE GroupMembers (
        group_id INT NOT NULL,
        user_id INT NOT NULL
        )           
""")

for user in data_user:
    created_at = datetime.strptime(user["created_at"], "%m/%d/%Y").date()
    cursor.execute("""INSERT INTO Users (user_id, username, password_hash, created_at)
                   VALUES (%s, %s, %s, %s)
                   """, 
                   (user["user_id"], user["username"], user["password_hash"], user["created_at"]))


for group in data_group:
        cursor.execute("""INSERT INTO Groups (group_id, group_name, organiser_user_id, tmdb_id, episodes_per_week)
                   VALUES (%s, %s, %s, %s, %s)
                   """, 
                   (group["group_id"], group["group_name"], group["organiser_user_id"], group["tmdb_id"], group["episodes_per_week"]))


for watchlist in data_watchlist:
        created_at = datetime.strptime(user["created_at"], "%m/%d/%Y").date()
        cursor.execute("""INSERT INTO Watchlist (watchlist_id, user_id, tmdb_id, added_at)
                   VALUES (%s, %s, %s, %s)
                   """, 
                   (watchlist["watchlist_id"], watchlist["user_id"], watchlist["tmdb_id"], watchlist["added_at"]))


for grmember in data_grmember:
        cursor.execute("""INSERT INTO GroupMembers (group_id, user_id)
                   VALUES (%s, %s)
                   """, 
                   (grmember["group_id"], grmember["user_id"]))

tables = ["Groups", "GroupMembers", "Watchlist", "Users"]

cursor.close
con.close