from config import get_db

# This function is uploading all the informations about the post inside the db
def create_post(user_id, caption, media_path, media_type):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO posts (user_id, caption, media_path, media_type)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (user_id, caption, media_path, media_type)
    )
    db.commit()
    return cursor.fetchone()['id']

def get_feed_post_ids(user_id):
    """
    Returns an ordered list of post IDs to show on the home feed.

    THIS IS THE ALGORITHM SLOT — right now it simply returns all posts
    ordered by newest first. Later you will replace this query with your
    scoring algorithm (likes, comments, time decay, follow graph, etc.)
    and this function will still return a plain list of IDs. Nothing else
    in the codebase needs to change.

    Returns: [4, 17, 2, 9, ...]  (list of ints, most relevant first)
    """
    db = get_db()
    cursor = db.cursor()

    # ---------------------------------------------------------------
    # CURRENT BEHAVIOUR: newest posts first, all users
    # Replace this query with your ranking algorithm when ready.
    # ---------------------------------------------------------------
    cursor.execute("""
        SELECT id
        FROM posts
        ORDER BY created_at DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()
    return [row['id'] for row in rows]   # e.g. [4, 17, 2, 9, ...]


def get_posts_by_ids(post_ids):
    """
    Given a list of post IDs, fetch the full post data for each one
    in the SAME ORDER as the input list.

    This keeps the algorithm's ordering intact — SQL does not guarantee
    row order so we re-sort in Python after fetching.

    Returns: list of dicts with keys:
        id, caption, media_path, media_type, created_at,
        user_id, username, profile_picture_path,
        like_count, comment_count
    """
    if not post_ids:
        return []

    db = get_db()
    cursor = db.cursor()

    # %s placeholders for each ID — psycopg2 handles the escaping safely
    placeholders = ','.join(['%s'] * len(post_ids))

    cursor.execute(f"""
        SELECT
            p.id,
            p.caption,
            p.media_path,
            p.media_type,
            p.created_at,
            p.user_id,
            u.name           AS username,
            u.profile_picture_path,
            COUNT(DISTINCT l.id)  AS like_count,
            COUNT(DISTINCT c.id)  AS comment_count
        FROM posts p
        JOIN users u        ON p.user_id = u.id
        LEFT JOIN likes l   ON p.id = l.post_id
        LEFT JOIN comments c ON p.id = c.post_id
        WHERE p.id IN ({placeholders})
        GROUP BY p.id, u.name, u.profile_picture_path
    """, post_ids)

    rows = cursor.fetchall()

    # Re-order rows to match the algorithm's original order
    order = {post_id: index for index, post_id in enumerate(post_ids)}
    return sorted(rows, key=lambda row: order[row['id']])