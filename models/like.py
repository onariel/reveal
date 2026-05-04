from config import get_db


def toggle_like(user_id, post_id):
    """
    If the user has not liked the post yet, add a like.
    If they already liked it, remove it.
    Returns a dict: { 'liked': True/False, 'like_count': N }
    """
    db = get_db()
    cursor = db.cursor()

    # Check if a like already exists
    cursor.execute("""
        SELECT id FROM likes
        WHERE user_id = %s AND post_id = %s
    """, (user_id, post_id))

    existing = cursor.fetchone()

    if existing:
        # Already liked → remove it
        cursor.execute("""
            DELETE FROM likes WHERE user_id = %s AND post_id = %s
        """, (user_id, post_id))
        liked = False
    else:
        # Not liked yet → add it
        cursor.execute("""
            INSERT INTO likes (user_id, post_id) VALUES (%s, %s)
        """, (user_id, post_id))
        liked = True

    db.commit()

    # Return the fresh count
    cursor.execute("SELECT COUNT(*) AS count FROM likes WHERE post_id = %s", (post_id,))
    count = cursor.fetchone()['count']

    return {'liked': liked, 'like_count': count}


def get_liked_post_ids(user_id, post_ids):
    """
    Given a list of post IDs, return the subset that the user has already liked.
    Used on page load to render hearts as filled or empty.
    Returns a set: {4, 17, ...}
    """
    if not post_ids:
        return set()

    db = get_db()
    cursor = db.cursor()

    placeholders = ','.join(['%s'] * len(post_ids))
    cursor.execute(f"""
        SELECT post_id FROM likes
        WHERE user_id = %s AND post_id IN ({placeholders})
    """, [user_id] + list(post_ids))

    rows = cursor.fetchall()
    return {row['post_id'] for row in rows}