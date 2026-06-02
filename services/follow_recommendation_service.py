from collections import defaultdict
from math import log1p

from config import get_db


def jaccard_similarity(set1, set2):
    union = set1 | set2
    if not union:
        return 0.0

    intersection = set1 & set2
    return len(intersection) / len(union)


def get_follow_recommendations(current_user_id, limit=5):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id FROM users")
    all_users = {row['id'] for row in cursor.fetchall()}

    cursor.execute("SELECT user1_id, user2_id FROM follows")
    follow_rows = cursor.fetchall()

    following_map = defaultdict(set)
    followers_count = defaultdict(int)

    for row in follow_rows:
        follower_id = row['user1_id']
        following_id = row['user2_id']

        following_map[follower_id].add(following_id)
        followers_count[following_id] += 1

    current_following = following_map[current_user_id]

    excluded_users = set(current_following)
    excluded_users.add(current_user_id)

    scores = defaultdict(float)
    reason_map = {}
    for followed_user_id in current_following:
        for candidate_id in following_map[followed_user_id]:
            if candidate_id in excluded_users:
                continue

            scores[candidate_id] += 3

            if candidate_id not in reason_map:
                reason_map[candidate_id] = followed_user_id

    for candidate_id in all_users:
        if candidate_id in excluded_users:
            continue

        candidate_following = following_map[candidate_id]
        similarity = jaccard_similarity(current_following, candidate_following)

        if similarity > 0:
            scores[candidate_id] += similarity * 2

    for candidate_id in all_users:
        if candidate_id in excluded_users:
            continue

        scores[candidate_id] += log1p(followers_count[candidate_id]) * 0.3

    ranked_candidates = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        {
            'user_id': user_id,
            'reason_user_id': reason_map.get(user_id)
        }
        for user_id, score in ranked_candidates[:limit]
    ]