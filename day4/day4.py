def parse_input(input_file):
    a_locations = []
    word_search = []
    with open(input_file) as file:
        for line_index, line in enumerate(file):
            word_search.append([])
            for character_index, character in enumerate(line.rstrip('\n')):
                if character == 'A':
                    a_locations.append((character_index, line_index))
                word_search[line_index].append(character)
    return word_search, a_locations


def add_movement(location, movement_vector, magnitude=1):
    return location[0] + movement_vector[0] * magnitude, location[1] + movement_vector[1] * magnitude


def get_letter(coordinates, word_search):
    if coordinates[0] >= 0 and coordinates[1] >= 0:
        try:
            return word_search[coordinates[1]][coordinates[0]]
        except IndexError:
            return 'Z'


def check_for_xmas(location, word_search):
    directions = [
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]
    local_group = []
    for direction in directions:
        local_group.append(get_letter(add_movement(location, direction), word_search))
    if local_group.count('M') == 2 and local_group.count('S') == 2:
        if local_group[0] != local_group[1]:
            return True
    return False


def get_xmas_count():
    word_search, a_locations = parse_input("puzzle_input")
    total_xmas = 0
    for a_location in a_locations:
        if check_for_xmas(a_location, word_search):
            total_xmas += 1
    return total_xmas


print(get_xmas_count())