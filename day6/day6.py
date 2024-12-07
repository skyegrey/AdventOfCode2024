def parse_input(input_file):
    starting_position = []
    starting_direction = None
    obstacles = set()
    with open(input_file) as file:
        for line_index, line in enumerate(file):
            for character_index, character in enumerate(line.rstrip('\n')):
                if character == "#":
                    obstacles.add((character_index, line_index))
                if not starting_direction:
                    if character == "<":
                        starting_direction = (-1, 0)
                    elif character == "^":
                        starting_direction = (0, -1)
                    elif character == "v":
                        starting_direction = (0, 1)
                    elif character == ">":
                        starting_direction = (1, 0)
                    if starting_direction:
                        starting_position = (character_index, line_index)
            else:
                width = character_index
        else:
            height = line_index

    return starting_position, starting_direction, obstacles, height, width


def add_position(position, direction):
    return position[0] + direction[0], position[1] + direction[1]


def rotate_90(direction):
    return -direction[1], direction[0]


def on_map(position, width, height):
    return 0 <= position[0] < width and 0 <= position[1] < height


def been_at_location_with_direction(current_position, current_direction, seen_locations):
    if current_position in seen_locations.keys():
        if current_direction in seen_locations[current_position]:
            return True


def walk_path(_current_position, _current_direction, _obstacles, height, width):
    current_position = _current_position
    current_direction = _current_direction
    obstacles = _obstacles
    seen_locations = set()
    while on_map(current_position, width, height):

        # Look ahead one step
        next_tile = add_position(current_position, current_direction)
        # Check if you need to turn
        if next_tile in obstacles:
            current_direction = rotate_90(current_direction)

        # If not, move forward one
        else:
            current_position = add_position(current_position, current_direction)

            # Update seen locations
            seen_locations.add(current_position)

    print(current_position)
    return seen_locations


def is_route_looping(_current_position, _current_direction, _obstacles, height, width):
    current_position = _current_position
    current_direction = _current_direction
    obstacles = set(_obstacles)
    seen_locations = {}
    while on_map(current_position, width, height):

        # Look ahead one step
        next_tile = add_position(current_position, current_direction)

        # Check if you need to turn
        if next_tile in obstacles:
            current_direction = rotate_90(current_direction)

        else:
            # If not, move forward one
            current_position = add_position(current_position, current_direction)

            # Check if loop has been found
            if been_at_location_with_direction(current_position, current_direction, seen_locations):
                return True
            else:
                if current_position in seen_locations:
                    seen_locations[current_position].add(current_direction)
                else:
                    seen_locations[current_position] = {current_direction}


# Get the map properties
def count_loops():
    current_position, current_direction, obstacles, height, width = parse_input("puzzle_input")
    path = walk_path(current_position, current_direction, obstacles, height, width)
    looping_paths = 0

    print("Path length: ", len(path))
    for tile in path:
        new_obstacle_set = set(obstacles)
        new_obstacle_set.add(tile)
        if is_route_looping(current_position, current_direction, new_obstacle_set, height, width):
            looping_paths += 1

    return looping_paths
    # return is_route_looping(current_position, current_direction, obstacles, height, width)


print(count_loops())