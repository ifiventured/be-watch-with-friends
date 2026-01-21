from pw import get_connection

con = get_connection()
con.autocommit = True
cursor = con.cursor()

db_name = "BEUserDatabase"
cursor.execute(f'DROP DATABASE IF EXISTS {db_name}')
cursor.execute(f'CREATE DATABASE {db_name}')
print(f"Database {db_name} created succesfully!")

cursor.execute("DROP TABLE IF EXISTS Users CASCADE")
cursor.execute("DROP TABLE IF EXISTS Watchlist CASCADE")
cursor.execute("DROP TABLE IF EXISTS Groups CASCADE")
cursor.execute("DROP TABLE IF EXISTS GroupMembers CASCADE")

cursor.execute("""
    CREATE TABLE Users (
        user_id SERIAL PRIMARY KEY, 
        username VARCHAR NOT NULL UNIQUE, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       )
""")
print("Table 'Users' created")

cursor.execute("""
    CREATE TABLE Watchlist (
        watchlist_id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        tmdb_id INT NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
""")
print("Table 'Watchlist' created")

cursor.execute("""
    CREATE TABLE Groups (
        group_id SERIAL PRIMARY KEY,
        group_name VARCHAR NOT NULL UNIQUE,
        organiser_user_id INT NOT NULL,
        tmdb_id INT,
        episodes_per_week INT
        )           
""")
print("Table 'Groups' created")

cursor.execute("""
    CREATE TABLE GroupMembers (
        group_id INT NOT NULL,
        user_id INT NOT NULL
        )           
""")
print("Table 'GroupMembers' created")

# for title in ("Ender's Game", "The Magus", "Starlight"):
#     con.run("INSERT INTO book (title) VALUES (:title)", title=title)

# for row in con.run("SELECT * FROM book"):
#     print(row)

cursor.close
con.close