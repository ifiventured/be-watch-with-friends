# Watch With Friends – Backend

FastAPI backend for the Watch With Friends project.

## Setup

### 1. Install Python

```bash
sudo apt install python3
```

### 2. Clone the Repo

```bash
git clone https://github.com/ifiventured/be-watch-with-friends.git
cd be-watch-with-friends
```

### 3. Create a Virtual Environment

This project requires a virtual environment for installing fastapi and pg8000, to do that you must setup a virtual environment in the project folder and set it as active

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install fastAPI and PG8000

```
pip install "fastapi[standard]"
pip install pg8000
```

### 5. Setup your pw.py file

pg8000 wants us to have a connection file, inside of app/db/seed, setup a file name pw.py with the contents:

```python
import pg8000

def get_connection():
    return pg8000.connect(
        user="postgres",
        password="",
        host="localhost",
        port=5432,
        database="postgres"
)
```

enter your password into the correct section and add the pw.py file to your .gitignore

### 5.5. Authentication error

If your connection is refused by PSQL due to 'password authentication failed for user postgres', or you can't remember your PSQL password, switch to system user postgres and open PSQL

```bash
sudo -i -u postgres
psql
```

once inside, we can check users:

```sql
-- Check users
\du

-- set a password for the postgres user
ALTER USER postgres WITH PASSWORD 'newpassword';
```

once you've changed your password, you can use:

```sql
\q
exit
```

### requirements.txt

In the virtual environment, run the following:

$ pip freeze > requirements.txt

This will create your requirements file.

Then run:

$ pip install -r requirements.txt

This installs needed dependencies to run the code.
