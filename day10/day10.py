class TrailNode:
    def __init__(self, elevation, location):
        self.elevation = elevation
        self.higher_elevation_nodes = []
        self.location = location
        self.rank = 0

    def add_higher_elevation_node(self, trail_node):
        self.higher_elevation_nodes.append(trail_node)

    def add_if_connected(self, trail_node):
        if self.elevation == trail_node.elevation - 1:
            self.higher_elevation_nodes.append(trail_node)
        elif self.elevation - 1 == trail_node.elevation:
            trail_node.add_higher_elevation_node(self)

    def get_rank(self):
        # if seen_nodes is None:
        #     seen_nodes = set()
        if self.elevation == 0:
            self.rank = sum(trail_node.get_rank() for trail_node in self.higher_elevation_nodes)
        if self.elevation == 9:
             return 1
        else:
            return sum(trail_node.get_rank() for trail_node in self.higher_elevation_nodes)


def parse_input(input_file):
    trail_heads = list()
    trail_elevation_grid = []
    with open(input_file) as file:
        for line_index, line in enumerate(file):
            trail_elevation_grid.append([])
            for elevation_index, elevation in enumerate(line.rstrip('\n')):
                trail_node = TrailNode(int(elevation), (elevation_index, line_index))
                trail_elevation_grid[line_index].append(trail_node)
                if trail_node.elevation == 0:
                    trail_heads.append(trail_node)
                if line_index >= 1:
                    local_node = trail_elevation_grid[line_index - 1][elevation_index]
                    trail_node.add_if_connected(local_node)
                if elevation_index >= 1:
                    local_node = trail_elevation_grid[line_index][elevation_index - 1]
                    trail_node.add_if_connected(local_node)
    for trail_head in trail_heads:
        trail_head.get_rank()
    return trail_heads


def map_trailhead_score(input_file):
    trail_heads = parse_input(input_file)
    return sum(trail_head.rank for trail_head in trail_heads)


print(map_trailhead_score("puzzle_input"))