def detect_instruction(index, instructions):
    valid_instructions = [
        'mul', 'don\'t()', 'do()'
    ]
    for instruction in valid_instructions:
        try:
            if instructions[index:index + len(instruction)] == instruction:
                return instruction
        except IndexError:
            pass


def parse_and_mul(instruction):
    args = instruction.split(")")[0]
    try:
        first_arg = int(args.split(",")[0])
        second_arg = int(args.split(",")[1])
        return first_arg * second_arg
    except IndexError:
        return 0
    except ValueError:
        return 0


with open("puzzle_input") as input:
    all_lines = [line for line in input]
    string_input = "".join(all_lines)

    mul_sum = 0
    can_mul = True
    for index in range(len(string_input)):
        instruction = detect_instruction(index, string_input)
        if instruction == 'mul':
            if can_mul:
                mul_sum += parse_and_mul(string_input[index + 4:])
        if instruction == 'do()':
            can_mul = True
        if instruction == 'don\'t()':
            can_mul = False
    print(mul_sum)