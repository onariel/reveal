from config import get_db


def get_user_by_email(email):
    """Fetch a single user by email. Returns a dict or None."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()


def get_user_by_username(username):
    """Fetch a single user by username. Returns a dict or None."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
    return cursor.fetchone()


def create_user(name, email, password_hash):
    """
    Insert a new user into the database.
    Returns the newly created user's id.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (name, email, password_hash)
    )
    db.commit()
    return cursor.fetchone()['id']


def email_exists(email):
    """Check if an email is already registered."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
    return cursor.fetchone() is not None


def username_exists(name):
    """Check if a username is already taken."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM users WHERE name = %s", (name,))
    return cursor.fetchone() is not None