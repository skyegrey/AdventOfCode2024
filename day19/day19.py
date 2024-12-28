import functools


methods_count = 0


def parse_input(input_file):
    with open(input_file) as file:
        lines = "".join([line for line in file])
        available_towels, patterns = lines.split('\n\n')
        available_towels = set(available_towels.split(', '))
        print(f'Available towels: {available_towels}')

        patterns = patterns.split('\n')
        print(f'Patterns: {patterns}')

    return available_towels, patterns


def can_be_made(pattern, towels, total=0):
    # print(f'Checking pattern: {pattern}')
    for split_index in range(1, len(pattern) + 1):
        if pattern[:split_index] in towels:
            if split_index == len(pattern):
                # print(f'Rest of towel found!')
                return True
            # print(f'{pattern[:split_index]} found! Checking {pattern[split_index:]}')
            if can_be_made(pattern[split_index:], towels):
                return True
    return False


@functools.lru_cache(maxsize=128)
def count_all_possible_methods(pattern, towels):
    return count_ways_to_make_fragment(pattern, towels)

@functools.lru_cache(maxsize=128)
def count_ways_to_make_fragment(fragment, towels):
    total_ways = 0
    for index in range(1, len(fragment) + 1):
        starting_fragment = fragment[:index]
        ending_fragment = fragment[index:]
        print(f'Testing if {starting_fragment} can be made')
        if starting_fragment in towels:
            if index == len(fragment):
                print('Starting fragment can be made and no string remains')
                total_ways += 1
            print(f'{starting_fragment} can be made, checking combinations of {ending_fragment}')
            total_ways += count_all_possible_methods(ending_fragment, towels)
    return total_ways






def find_makeable_patterns(input_file):
    available_towels, patterns = parse_input(input_file)
    makeable_patterns = 0
    total_ways = 0
    global methods_count
    for pattern_index, pattern in enumerate(patterns):
        if can_be_made(pattern, available_towels):
            makeable_patterns += 1
            total_ways += count_all_possible_methods(pattern, tuple(available_towels))
            print(f'Finding pattern {pattern_index}')
    return makeable_patterns, total_ways


print(find_makeable_patterns("puzzle_input"))