import utils
import re
from heapq import heapify, heappop, heappush
from sys import maxsize

example = False

inputfile = utils.INPUT_DIR / "day16.txt"
if example:
    inputfile = utils.INPUT_DIR / "day16_example.txt"

# Part 1
with open(inputfile, 'r') as fh:
    lines = fh.readlines()

blocked = set()

initial_dir = '>'
start_position = None
end_position = None

N_lines = len(lines)
N_col = len(lines[0].strip())

i = 0
for line in lines:
    j = 0
    for x in line.strip():
        if x == '#':
            blocked.add(i + 1j * j)
        elif x == 'S':
            start_position = (i + 1j * j, ">")
        elif x == 'E':
            end_position = (i + 1j * j)
        j += 1
    i += 1

moves = {
    "^": -1 + 0j,
    ">": 0 + 1j,
    "v": 1 + 0j,
    "<": 0 - 1j
    }

cost_rotation = 1000
cost_move = 1

distances_from_S = {start_position: 0}

def get_neighbors(node):
    if node[0] in blocked:
        return {}
    neighbors = {}
    direction = node[1]
    possible_local_dirs = {'^', '>', 'v', '<'}
    possible_local_dirs.remove(direction)
    if direction == "^":
        possible_local_dirs.remove("v")
    if direction == ">":
        possible_local_dirs.remove("<")
    if direction == "v":
        possible_local_dirs.remove("^")
    if direction == "<":
        possible_local_dirs.remove(">")

    # Possible rotations
    for x in possible_local_dirs:
        neighbors[(node[0], x)] = cost_rotation
    
    # Possible neighbor, keeping the same direction
    if node[0] + moves[direction] not in blocked:
        neighbors[(node[0] + moves[direction], direction)] = cost_move
    
    return neighbors

# Building adjacencies table, so it is not computed multiple times
adjacencies = {}
for i in range(N_lines):
    for j in range(N_col):
        for dir in {'^', '>', 'v', '<'}:
            # For each node in the graph, find possible neighbors:
            adjacencies[(i + 1j * j, dir)] = get_neighbors((i + 1j * j, dir))

adjacencies[(end_position, '>')][end_position] =  0
adjacencies[(end_position, 'v')][end_position] =  0
adjacencies[(end_position, '<')][end_position] =  0
adjacencies[(end_position, '^')][end_position] =  0
adjacencies[end_position] = {}
adjacencies[end_position][(end_position, '>')] = 0
adjacencies[end_position][(end_position, 'v')] = 0
adjacencies[end_position][(end_position, '<')] = 0
adjacencies[end_position][(end_position, '^')] = 0

class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph
        self.distances_from = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = weight
        
    def shortest_distances(self, source):
        distances = {node: maxsize for node in self.graph}
        distances[source] = 0
        
        pq = [(0, id(source), source)]
        heapify(pq)
        
        visited = set()
        
        # While the priority queue is not empty
        while pq:
            current_distance, _, current_node = heappop(pq)
            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, weight in self.graph[current_node].items():
                possible_distance = current_distance + weight
                if possible_distance < distances[neighbor]:
                    distances[neighbor] = possible_distance
                    heappush(pq, (possible_distance, id(neighbor), neighbor))
                
        return distances

# Part 1
# Dijkstra
G = Graph(adjacencies)


min_score = G.shortest_distances(start_position)[end_position]

print("Minimum score:", min_score)

# print(get_neighbors((3 + 5j, '<')))
# print(get_neighbors((3 + 5j, 'v')))
# print(get_neighbors((3 + 5j, '>')))
# print(get_neighbors((3 + 5j, '^')))

shortest_distances_from_S = G.shortest_distances(start_position)
shortest_distances_from_E = G.shortest_distances(end_position)

sittable_tiles = set()

opposites = {'>': '<', '<': '>', '^': 'v', 'v': '^'}

for x in shortest_distances_from_S:
    if x != end_position:
        mirror_x = (x[0], opposites[x[1]])
        if shortest_distances_from_S[x] + shortest_distances_from_E[mirror_x] == min_score:
            sittable_tiles.add(x[0])
    

print("Sittable tiles:", len(sittable_tiles))
print(sittable_tiles)

print("-------")
print("End position:", end_position)