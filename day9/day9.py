import time


def parse_input(input_file):
    disk_map = []
    with open(input_file) as file:
        for line in file:
            disk_map = [int(character) for character in line]

    return disk_map


def generate_disk(disk_map):
    disk = []
    for index, size in enumerate(disk_map):
        # File block
        if index % 2 == 0:
            file_id = index // 2
            disk.extend([file_id] * size)
        # Free space block
        else:
            disk.extend([-2] * size)
    return disk


def get_checksum(disk):
    checksum = 0
    for index, file_id in enumerate(disk):
        if disk[index] != -2:
            checksum += index * file_id
    return checksum


def swap_disk(disk):
    front_head = 0
    back_head = len(disk) - 1
    while front_head < back_head:
        if disk[front_head] != -2:
            front_head += 1
        elif disk[back_head] == -2:
            back_head -= 1
        else:
            disk[front_head] = disk[back_head]
            disk[back_head] = -2
            front_head += 1
            back_head -= 1
    return disk


def generate_disk_properties(disk_map):
    class File:
        def __init__(self, id, start, size):
            self.id = id
            self.start = start
            self.size = size

    class FreeSpace:
        def __init__(self, start, size):
            self.start = start
            self.size = size
    files = []
    free_spaces = []

    size_total = 0
    for index, size in enumerate(disk_map):
        # File block
        if index % 2 == 0:
            file_id = index // 2
            files.append(File(file_id, size_total, size))

        # Free Space
        else:
            free_spaces.append(FreeSpace(size_total, size))
        size_total += size
    return files, free_spaces


def swap_files(files, free_spaces, disk):
    for file_index, file in enumerate(reversed(files)):
        for free_space_index, free_space in enumerate(free_spaces):
            if free_space.size >= file.size and free_space.start < file.start:
                # Swap file to front of free space
                disk[free_space.start:free_space.start + file.size] = [file.id] * file.size
                disk[file.start:file.start + file.size] = [-2] * file.size

                # Update the remaining free space
                free_space.size -= file.size
                free_space.start += file.size
                # If it is less than 0, remove from the list
                if free_space.size == 0:
                    free_spaces.pop(free_space_index)
                break
    return disk


def defrag():
    input_file = "puzzle_input"
    disk_map = parse_input(input_file)
    disk = generate_disk(disk_map)
    # disk = swap_disk(disk)s
    files, free_spaces = generate_disk_properties(disk_map)
    disk = swap_files(files, free_spaces, disk)
    return get_checksum(disk)


start_time = time.time()
print(defrag())
end_time = time.time()
print(f'Computation time: {end_time - start_time} seconds')