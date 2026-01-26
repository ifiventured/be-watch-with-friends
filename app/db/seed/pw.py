import pg8000

def get_connection():
    return pg8000.connect(
        user="postgres",
        password="password234",
        host="localhost",
        port=5432,
        database="postgres"
)