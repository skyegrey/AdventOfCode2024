from collections import defaultdict, namedtuple
Node = namedtuple("Node", "x, y")


def parse_input(input_file):
    antenna_grid = []
    frequency_to_locations = defaultdict(list)
    with open(input_file) as file:
        for line_index, line in enumerate(file):
            antenna_grid.append([])
            for character_index, character in enumerate(line.rstrip('\n')):
                if character != '.':
                    frequency_to_locations[character].append(Node(character_index, line_index))
                antenna_grid[line_index].append(character)

    return antenna_grid, len(antenna_grid), len(antenna_grid[0]), frequency_to_locations


def get_distance(node_1, node_2):
    return node_2.x - node_1.x, node_2.y - node_1.y


def add_nodes(node_1, node_2):
    return Node(node_1.x + node_2.x, node_1.y + node_2.y)


def calculate_antinodes_locations(antenna_locations, height, width):
    antinode_locations = set()
    for antenna_index, antenna_location in enumerate(antenna_locations[:-1], 1):
        antinode_locations.add(antenna_location)
        for same_frequency_antenna in antenna_locations[antenna_index:]:
            x_distance, y_distance = get_distance(antenna_location, same_frequency_antenna)
            positive_line = Node(x_distance, y_distance)
            negative_line = Node(-x_distance, -y_distance)
            next_location = add_nodes(same_frequency_antenna, positive_line)
            while is_valid(next_location, height, width):
                antinode_locations.add(next_location)
                next_location = add_nodes(next_location, positive_line)
            next_location = add_nodes(antenna_location, negative_line)
            while is_valid(next_location, height, width):
                antinode_locations.add(next_location)
                next_location = add_nodes(next_location, negative_line)
            antinode_locations.add(same_frequency_antenna)
    return antinode_locations


def is_valid(node, height, width):
    if 0 <= node.x < height and 0 <= node.y < width:
        return True


def print_antenna_grid(antenna_grid):
    print("\n".join(["".join(line) for line in antenna_grid]))


def count_antinodes(input_file):
    antenna_grid, height, width, frequency_to_locations = parse_input(input_file)

    # print_antenna_grid(antenna_grid)
    antinode_locations = set()
    for frequency in frequency_to_locations.keys():
        antinode_locations.update(calculate_antinodes_locations(frequency_to_locations[frequency],
                                                                         height, width))
    print(antinode_locations)
    for location in antinode_locations:
        antenna_grid[location.y][location.x] = '#'
    # print_antenna_grid(antenna_grid)
    return len(antinode_locations)


print(count_antinodes("puzzle_input"))
