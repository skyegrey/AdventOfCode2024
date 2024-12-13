def parse_input(input_file):
    a_buttons = []
    b_buttons = []
    prizes = []
    with open(input_file) as file:
        for line in file:
            if line.startswith('Button A'):
                a_button = (
                    int(line.split(',')[0].split('X+')[1]),
                    int(line.split(',')[1].split('Y+')[1])
                )
                a_buttons.append(a_button)

            elif line.startswith('Button B'):
                b_button = (
                    int(line.split(',')[0].split('X+')[1]),
                    int(line.split(',')[1].split('Y+')[1])
                )
                b_buttons.append(b_button)
            elif line.startswith("Prize: "):
                prizes.append(
                    (
                        int(line.split(',')[0].split('X=')[1]) + 10000000000000,
                        int(line.split(',')[1].split('Y=')[1]) + 10000000000000
                    )
                )

    return a_buttons, b_buttons, prizes


def get_minimum_tokens(a_button, b_button, prize):
    X = prize[0]
    Y = prize[1]
    x_a = a_button[0]
    y_a = a_button[1]
    x_b = b_button[0]
    y_b = b_button[1]
    A = (X - (Y*x_b)/y_b) / (x_a - y_a * x_b / y_b)
    B = (Y - A * y_a) / y_b
    if A > 0 and B > 0:
        if round(A)*x_a + round(B)*x_b == X and round(A)*y_a + round(B)*y_b == Y:
            return int(3*(round(A)) + round(B))

    return 0


def get_token_count(input_file):
    a_buttons, b_buttons, prizes = parse_input(input_file)
    token_count = 0
    for a_button, b_button, prize in zip(a_buttons, b_buttons, prizes):
        print(prize)
        token_count += get_minimum_tokens(a_button, b_button, prize)
    return token_count


print(get_token_count("puzzle_input"))
