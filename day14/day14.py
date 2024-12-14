from collections import defaultdict


class Robot:
    def __init__(self, starting_position, velocity, grid_dimensions):
        self.starting_position = starting_position
        self.position = starting_position
        self.velocity = velocity
        self.grid_dimensions = grid_dimensions

    def tick_warp(self, ticks):
        new_position_x = (self.position[0] + self.velocity[0] * ticks) % self.grid_dimensions[0]
        new_position_y = (self.position[1] + self.velocity[1] * ticks) % self.grid_dimensions[1]
        self.position = (new_position_x, new_position_y)


def parse_input(input_file, grid_dimensions):
    robots = []
    with open(input_file) as file:
        for line in file:
            position_x = int(line.split(',')[0].lstrip("p="))
            position_y = int(line.split(',')[1].split('v=')[0].rstrip(' '))
            velocity_x = int(line.split(',')[1].split('v=')[1])
            velocity_y = int(line.split(',')[2].rstrip('\n'))
            robots.append(Robot((position_x, position_y), (velocity_x, velocity_y), grid_dimensions))
    return robots


def move_robot(robot, ticks):
    pass


def print_robots(robots, position=None):
    grid_width = robots[0].grid_dimensions[0]
    grid_height = robots[0].grid_dimensions[1]

    output_grid = [[0 for _ in range(grid_width)] for __ in range(grid_height)]

    for robot in robots:
        output_grid[robot.position[1]][robot.position[0]] += 1

    if position:
        output_grid[position[1]][position[0]] = "T"


    print('\n'.join([str(row) for row in output_grid]))
    with open("bot_positions", 'w') as output_file:
        output_file.write('\n'.join(["".join(str(n) for n in row) for row in output_grid]))


def get_safety_number(input_file, grid_width=11, grid_height=7):
    robots = parse_input(input_file, (grid_width, grid_height))

    for robot in robots:
        robot.tick_warp(100)

    half_width = grid_width // 2
    half_height = grid_height // 2
    # quadrants = {
    #     ((0, 0), (half_width - 1, half_height - 1)): 0,
    #     ((half_width + 1, 0), (grid_width - 1, half_height - 1)): 0,
    #     ((0, half_height + 1), (half_width - 1, grid_height - 1)): 0,
    #     ((half_width + 1, half_height + 1), (grid_width - 1, grid_height - 1)): 0
    # }
    quadrants = {
        'q1': 0,
        'q2': 0,
        'q3': 0,
        'q4': 0
    }
    for robot in robots:
        if robot.position[0] > half_width and robot.position[1] > half_height:
            quadrants['q4'] += 1
        elif robot.position[0] > half_width and robot.position[1] < half_height:
            quadrants['q2'] += 1
        elif robot.position[0] < half_width and robot.position[1] > half_height:
            quadrants['q3'] += 1
        elif robot.position[0] < half_width and robot.position[1] < half_height:
            quadrants['q1'] += 1

    safety_number = 1
    for quadrant, robot_count in quadrants.items():
        safety_number *= robot_count
    return safety_number


def add_positions(pos_1, pos_2):
    return pos_1[0] + pos_2[0], pos_1[1] + pos_2[1]


def check_for_triangle(position, bot_positions):
    tree_positions = defaultdict(set)
    tree_positions[1].add(position)
    checking_layer = 1
    directions = [
        (0, 1), (-1, 1), (1, 1)
    ]
    while len(tree_positions[checking_layer]) == checking_layer * 2 - 1:
        checking_layer += 1
        for tree_node in tree_positions[checking_layer - 1]:
            for direction in directions:
                if add_positions(tree_node, direction) in bot_positions:
                    tree_positions[checking_layer].add(add_positions(tree_node, direction))

    if len(tree_positions[checking_layer]) == 0 and checking_layer > 3:
        print("Tree found")
        return position, checking_layer


def check_for_tree(robots):
    bot_positions = defaultdict(int)
    for robot in robots:
        bot_positions[robot.position] += 1
    for position, bot_count in bot_positions.items():
        if check_for_triangle(position, bot_positions):
            print(position)
            print_robots(robots, position)
            return True


def get_tree_step(input_file, grid_width=101, grid_height=103):
    robots = parse_input(input_file, (grid_width, grid_height))

    step_count = 0
    while not check_for_tree(robots):
        step_count += 1
        for robot in robots:
            robot.tick_warp(1)
    return step_count


print(get_safety_number("puzzle_input", 101, 103))
print(get_tree_step("puzzle_input"))
