from config import get_db


def is_following(follower_id, following_id):
    """Return True if follower_id already follows following_id."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT 1 FROM follows WHERE user1_id = %s AND user2_id = %s",
        (follower_id, following_id)
    )
    return cursor.fetchone() is not None


def toggle_follow(follower_id, following_id):
    """
    Follow if not yet following, unfollow if already following.
    Returns { 'following': bool }
    """
    if follower_id == following_id:
        raise ValueError("A user cannot follow themselves.")

    db = get_db()
    cursor = db.cursor()

    if is_following(follower_id, following_id):
        cursor.execute(
            "DELETE FROM follows WHERE user1_id = %s AND user2_id = %s",
            (follower_id, following_id)
        )
        following = False
    else:
        cursor.execute(
            "INSERT INTO follows (user1_id, user2_id) VALUES (%s, %s)",
            (follower_id, following_id)
        )
        following = True

    db.commit()
    return {'following': following}


def get_users_by_ids(user_ids):
    """
    Given a list of user IDs (from your suggestion algorithm),
    return their basic info in the same order.

    This is the ONLY function the suggestion sidebar needs.
    Your algorithm produces the IDs, this function fetches the data.

    Returns: [{ id, username, profile_picture_path }, ...]
    """
    if not user_ids:
        return []

    db = get_db()
    cursor = db.cursor()

    placeholders = ','.join(['%s'] * len(user_ids))
    cursor.execute(f"""
        SELECT id, name AS username, profile_picture_path
        FROM users
        WHERE id IN ({placeholders})
    """, user_ids)

    rows = cursor.fetchall()

    # Preserve the order the algorithm decided
    order = {uid: i for i, uid in enumerate(user_ids)}
    return sorted(rows, key=lambda r: order[r['id']])


def get_followed_ids(user_id):
    """
    Return the set of user IDs that user_id is currently following.
    Used by the home route to mark which suggestion buttons are already followed.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT user2_id FROM follows WHERE user1_id = %s", (user_id,))
    return {row['user2_id'] for row in cursor.fetchall()}