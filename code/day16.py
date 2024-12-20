import utils
import re

example = True

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

class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph
        self.distances_from = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = weight

# Part 1
# Dijkstra
G = Graph(adjacencies)

print(G.graph)

# print(get_neighbors((3 + 5j, '<')))
# print(get_neighbors((3 + 5j, 'v')))
# print(get_neighbors((3 + 5j, '>')))
# print(get_neighbors((3 + 5j, '^')))
