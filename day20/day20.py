import copy
import sys


def add_locations(loc_1, loc_2):
    return loc_1[0] + loc_2[0], loc_1[1] + loc_2[1]


location_to_rest_of_solve = {}
start_location = None
good_cheats = 0
sys.setrecursionlimit(50000)


class MazeNode:
    def __init__(self, location, seen_nodes=None, cost_to_reach=0):
        self.location = location
        self.child_nodes = []
        self.cost_to_reach = cost_to_reach

        if not seen_nodes:
            self.seen_nodes = set()
        else:
            self.seen_nodes = seen_nodes

        self.directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        self.cheat_directions = set()
        max_cheat_length = 20
        for cheat_length in range(1, max_cheat_length + 1):
            for x in range(cheat_length + 1):
                self.cheat_directions.add((x, cheat_length - x))
                self.cheat_directions.add((-x, cheat_length - x))
                self.cheat_directions.add((-x, -(cheat_length - x)))
                self.cheat_directions.add((x, -(cheat_length - x)))
        # print(sorted(list(self.cheat_directions)))

    def populate_standard_route(self, maze):
        for direction in self.directions:
            check_location = add_locations(self.location, direction)
            if maze.get_object(check_location) in ('.', 'S'):
                self.add_standard_route(check_location)
        for child in self.child_nodes:
            child.populate_standard_route(maze)

    def add_standard_route(self, location):
        if location not in self.seen_nodes:
            route_seen_nodes = self.seen_nodes.copy()
            route_seen_nodes.add(self.location)
            self.child_nodes.append(MazeNode(location, route_seen_nodes, self.cost_to_reach + 1))
            location_to_rest_of_solve[self.child_nodes[-1].location] = self.child_nodes[-1]

    def find_good_cheats(self, maze, found_good_cheats=0):
        print("Checking depth", self.cost_to_reach)
        found_good_cheats += sum(child.find_good_cheats(maze, found_good_cheats) for child in self.child_nodes)
        for cheat_direction in self.cheat_directions:
            check_location = add_locations(self.location, cheat_direction)
            wall_checks = []
            # if abs(cheat_direction[0]) + abs(cheat_direction[1]) >= 17:
            if check_location[0] > 0:
                wall_checks.append((1, 0))
            elif check_location[0] < 0:
                wall_checks.append((-1, 0))
            if check_location[1] > 0:
                wall_checks.append((0, 1))
            elif check_location[1] < 0:
                wall_checks.append((0, -1))
            if maze.get_object(check_location) in ('.', 'S'): # and any(maze.get_object(add_locations(self.location, wall_check)) == '#' for wall_check in wall_checks):
                try:
                    time_save = location_to_rest_of_solve[check_location].cost_to_reach - self.cost_to_reach - abs(cheat_direction[0]) - abs(cheat_direction[1])
                    if time_save >= 100:
                        # maze.print_maze_skip(self.location, cheat_direction)
                        found_good_cheats += 1
                except KeyError:
                    continue
        return found_good_cheats

    def print_node_root(self):
        self_print = f'Root Node {self.location}, children nodes: {"".join([child_node.print_node() for child_node in self.child_nodes])}'
        print(self_print)

    def print_node(self, tabs=1):
        if tabs < 5:
            self_print = '\n' + '\t'*tabs + f'Child Node {self.location}, children nodes:' + "".join([child_node.print_node(tabs + 1) for child_node in self.child_nodes])
        else:
            return ''
        return self_print


class Maze:
    def __init__(self):
        self.starting_location = None
        self.ending_location = None
        self.map = []
        self.dag_root = None

    def add_to_map(self, character):
        self.map[-1].append(character)

    def print_map(self):
        print('\n'.join(''.join(row) for row in self.map))

    def get_object(self, location):
        try:
            return self.map[location[1]][location[0]]
        except IndexError:
            return None

    def build_dag(self):
        self.dag_root = MazeNode(self.ending_location)
        self.dag_root.populate_standard_route(self)
        self.dag_root.print_node_root()
        print(self.dag_root.find_good_cheats(self))

    def print_maze_skip(self, ending_location, vector):
        starting_location = add_locations(ending_location, vector)
        print_map = copy.deepcopy(self.map)
        print_map[ending_location[1]][ending_location[0]] = 'C'
        print_map[starting_location[1]][starting_location[0]] = 'H'
        print('\n'.join(''.join(row) for row in print_map))



def parse_input(input_file):
    _maze = Maze()
    with open(input_file) as file:
        for line_index, line in enumerate(file):
            _maze.map.append([])
            for character_index, character in enumerate(line.rstrip('\n')):
                maze_location = (character_index, line_index)
                if character == 'S':
                    _maze.starting_location = maze_location
                elif character == 'E':
                    # Very E
                    _maze.ending_location = maze_location
                _maze.add_to_map(character)
    return _maze


maze = parse_input("puzzle_input")
maze.print_map()
maze.build_dag()