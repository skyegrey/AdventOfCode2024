from collections import namedtuple
import time

def parse_input(input_file):
    calibrations = []
    Calibration = namedtuple("Calibration", "result, inputs")
    with open(input_file) as file:
        for line in file:
            result = int(line.split(":")[0])
            input_string = line.split(":")[1]
            input_string = input_string.rstrip('\n')
            input_string = input_string.lstrip()
            inputs = [int(number) for number in input_string.split(" ")]
            calibrations.append(Calibration(result, inputs))
    return calibrations


def generate_all_instruction_sets(inputs):
    possible_instructions = ['*', '+', '|']
    total_equations = len(possible_instructions)**(len(inputs) - 1)
    instruction_sets = list(possible_instructions)
    while len(instruction_sets) < total_equations:
        new_instruction_set = []
        for instruction_set in instruction_sets:
            for instruction in possible_instructions:
                new_instruction_set.append(instruction_set + instruction)
        instruction_sets = list(new_instruction_set)
    return instruction_sets


def evaluate_equation(instruction_set, inputs):
    operations = {
        '*': lambda x, y: x * y,
        '+': lambda x, y: x + y,
        '|': lambda x, y: int(str(x) + str(y))
    }

    total = operations[instruction_set[0]](inputs[0], inputs[1])
    for index, instruction in enumerate(instruction_set[1:], 1):
        total = operations[instruction](total, (inputs[index + 1]))
    return total


def brute_force_check_calibration(calibration):
    # create all the possible equations given the input
    instruction_sets = generate_all_instruction_sets(calibration.inputs)

    # Loop through generation equations, to see if their result is equal to the result
    for instruction_set in instruction_sets:
        evaluation_result = evaluate_equation(instruction_set, calibration.inputs)
        if evaluation_result == calibration.result:
            return True


def get_correct_calibration_totals():
    calibrations = parse_input("puzzle_input")
    correct_calibration_results = 0
    for calibration in calibrations:
        if brute_force_check_calibration(calibration):
            correct_calibration_results += calibration.result
    return correct_calibration_results


start_time = time.time()
result = get_correct_calibration_totals()
end_time = time.time()
print(f'Correct calibration sum: {result} in {end_time - start_time} seconds')