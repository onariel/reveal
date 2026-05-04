from config import get_db


def add_comment(user_id, post_id, text):
    """
    Insert a new comment and return the full comment row
    (including username) so it can be sent back to the browser immediately.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO comments (user_id, post_id, text)
        VALUES (%s, %s, %s)
        RETURNING id, text, created_at
    """, (user_id, post_id, text))

    db.commit()
    new_comment = cursor.fetchone()

    # Fetch the username to include in the response
    cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    return {
        'id':         new_comment['id'],
        'text':       new_comment['text'],
        'username':   user['name'],
        'created_at': new_comment['created_at'].strftime('%B %d, %Y · %H:%M')
    }


def get_comments_by_post(post_id):
    """
    Return all comments for a post, oldest first, with their author's username.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.text,
            c.created_at,
            u.name AS username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.post_id = %s
        ORDER BY c.created_at ASC
    """, (post_id,))

    rows = cursor.fetchall()

    # Convert datetime to string for JSON serialisation
    return [
        {
            'id':         row['id'],
            'text':       row['text'],
            'username':   row['username'],
            'created_at': row['created_at'].strftime('%B %d, %Y · %H:%M')
        }
        for row in rows
    ]