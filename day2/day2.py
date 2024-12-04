def is_safe(reactor_output, top_level=True):
    print(reactor_output)
    # has to be decreasing or increasing
    is_increasing = None
    # has to change by less than 3
    max_number_change = 3
    level_differences = [number - reactor_output[index + 1] for index, number in enumerate(reactor_output[:-1])]
    sign_sum = 0
    difference_errors = 0
    for level_difference in level_differences:
        if abs(level_difference) > max_number_change:
            difference_errors += 1
        if level_difference != 0:
            sign_sum += level_difference // abs(level_difference)
    if abs(sign_sum) == len(level_differences) and difference_errors == 0:
        return True
    elif top_level:
        # Not safe, try removing :)
        # VERY NAIVE APPROACH YOU CAN PROBABLY BE CLEVER BUT I WANT TO MOVE ON TO THE NEXT PROBLEM
        if any([is_safe(reactor_output[:index] + reactor_output[index + 1:], False) for index in range(len(reactor_output))]):
            return True


with open("puzzle_input") as input_file:
    safe_outputs = 0
    for line in input_file:
        reactor_numbers = list(map(int, line.split()))
        if is_safe(reactor_numbers):
            safe_outputs += 1
    print(safe_outputs)
