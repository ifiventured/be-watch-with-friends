import pg8000

con = pg8000.connect(
    user="postgres",
    password="password123",
    host="localhost",
    port=5432,
    database="postgres"
)

con.autocommit = True
cursor = con.cursor()

# db_name = "NewDatabase"
# cursor.execute(f'CREATE DATABASE {db_name}')
# print(f"Database {db_name} created succesfully!")

con.run("CREATE TEMPORARY TABLE book (id SERIAL, title TEXT)")

for title in ("Ender's Game", "The Magus", "Starlight"):
    con.run("INSERT INTO book (title) VALUES (:title)", title=title)

for row in con.run("SELECT * FROM book"):
    print(row)

cursor.close
con.close