import random
from collections import deque
class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        
        # Add users
        for i in range(num_users):
            self.add_user(f'Person {i + 1}')

        

        # Create friendships
        possible_friendships = []

        for i in range(1, num_users + 1):
            for j in range(1, num_users + 1):
                if i < j:
                    possible_friendships.append((i, j))

        random.shuffle(possible_friendships)
        
        for f in range((avg_friendships * num_users) // 2):
            self.add_friendship(possible_friendships[f][0], possible_friendships[f][1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        stack = deque()

        for f in self.friendships[user_id]: #add friends to stack
            stack.append(f)

        while len(stack) > 0:
            #print(stack)
            friend_id = stack.pop()
            visited[friend_id] = self.bfs_helper(user_id, friend_id, stack, visited)

        
        
        return visited

    def bfs_helper(self, user_id, friend_id, stack, visited_d):
        queue = deque()
        queue.append([user_id])
        visited = set()
        while len(queue) > 0:
            currPath = queue.popleft()
            currNode = currPath[-1]
            if currNode == friend_id:
                for f in self.friendships[currNode]: #add friends to stack
                    if f not in visited_d:
                        stack.append(f)
                return currPath
            if currNode not in visited:
                visited.add(currNode)
                for neighbor in self.get_neighbors(currNode):
                    newPath = list(currPath)
                    newPath.append(neighbor)
                    queue.append(newPath)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.friendships[vertex_id] if vertex_id in self.friendships else set()


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(100, 10)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
