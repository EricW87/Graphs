from room import Room
from player import Player
from world import World

import random
from collections import deque
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

##HELPER FUNCTION - returns opposite of given direction
def opp_dir(d):
    if d == 'n':
        return 's'

    if d == 's':
        return 'n'

    if d == 'e':
        return 'w'

    return 'e'

##BFS - When you reach a dead end, this function looks for the shortest path back
def bfs_goback(room_id, edges):
        queue = deque()
        queue.append([(room_id, '')])
        visited = set()
        
        while len(queue) > 0:
            #print(queue)
            adjacent = []
            currPath = queue.popleft()
            currNode = currPath[-1]
            #base case - find room with a '?'
            for e in list(edges[currNode[0]].keys()):
                #print(e)
                adjacent.append((edges[currNode[0]][e], e))
                if edges[currNode[0]][e] == '?':
                    return currPath
            if currNode[0] not in visited:
                visited.add(currNode[0])
                #print(f'visited {visited}')
                #print(f'adjacent {adjacent}')
                for neighbor in adjacent:
                    #print(f'neighbor {neighbor}')
                    newPath = list(currPath)
                    newPath.append(neighbor)
                    queue.append(newPath)

edges = {} #adjacency dictionary
prev_id = -1
prev_d = ''

while len(edges) < len(room_graph):
    print(edges)
    if player.current_room.id not in edges:
        edges[player.current_room.id] = {}
        for e in player.current_room.get_exits():
            edges[player.current_room.id][e] = '?'

    if prev_id >= 0: #Just to make sure you haven't just started
        edges[prev_id][prev_d] = player.current_room.id
        edges[player.current_room.id][opp_dir(prev_d)] = prev_id

    found = False
    for e in list(edges[player.current_room.id].keys()):
        if edges[player.current_room.id][e] == '?' and found == False:
            traversal_path.append(e)
            prev_id = player.current_room.id
            prev_d = e
            player.travel(e)
            found = True
            break

    if found == False:
        path = bfs_goback(player.current_room.id, edges)
        #print(path, player.current_room.id)
        for m in path:
            if m[1] >= 'a' and m[1] <= 'z':
                #print(m[1])
                player.travel(m[1])
        #print(player.current_room.id)
        prev_id = -1 #We shouldn't need to add anything to the dictionary
"""
#RANDOM CHOICE
    if found == False:
        c = random.choice(list(edges[player.current_room.id].keys()))
        print(c)
        traversal_path.append(c)
        prev_id = player.current_room.id
        prev_d = c
        player.travel(c)
"""





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
"""
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""
