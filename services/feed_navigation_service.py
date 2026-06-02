class FeedNode:
    def __init__(self, post_id):
        self.post_id = post_id
        self.prev = None
        self.next = None


class FeedNavigator:
    def __init__(self, post_ids):
        self.nodes = {}

        previous_node = None

        for post_id in post_ids:
            node = FeedNode(post_id)
            self.nodes[post_id] = node

            if previous_node:
                previous_node.next = node
                node.prev = previous_node

            previous_node = node

    def get_neighbors(self, current_post_id):
        current_node = self.nodes.get(current_post_id)

        if not current_node:
            return {
                'prev_post_id': None,
                'next_post_id': None
            }

        return {
            'prev_post_id': current_node.prev.post_id if current_node.prev else None,
            'next_post_id': current_node.next.post_id if current_node.next else None
        }