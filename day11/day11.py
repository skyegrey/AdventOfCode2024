from collections import defaultdict

seen_instructions = {
    0: [1],
    1: [2024],
    2024: [20, 24]
}


def parse_input(input_file):
    stones = defaultdict(int)
    with open(input_file) as file:
        for line in file:
            for stone in line.rstrip('\n').split(' '):
                stones[int(stone)] += 1
    return stones


def blink(stones):
    post_blink_stones = defaultdict(int)
    for stone, count in stones.items():
        if stone not in seen_instructions.keys():
            stone_as_string = str(stone)

            # If even, split into two stones
            if len(stone_as_string) % 2 == 0:
                new_rhs = int(stone_as_string[len(stone_as_string) // 2:])
                new_lhs = int(stone_as_string[:len(stone_as_string) // 2])
                new_stones = [new_lhs, new_rhs]
                seen_instructions[stone] = new_stones
            # If odd, multiply by 2024
            else:
                new_stone = stone * 2024
                seen_instructions[stone] = [new_stone]

        for resulting_stone in seen_instructions[stone]:
            post_blink_stones[resulting_stone] += count
    return post_blink_stones


def count_stones(input_file, blinks):
    stones = parse_input(input_file)
    for _ in range(blinks):
        print(f'Blinking step {_} of {blinks}')
        stones = blink(stones)
    return sum(stones.values())


print(count_stones("puzzle_input", 60000))