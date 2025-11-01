import argparse

DIGITS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", " "}
OPERANDS = {"+", "-", "*", "/"}


def validate_str(text):
    for ch in text:
        if ch not in DIGITS and ch not in OPERANDS:
            raise ValueError(f"Invalid character: {ch}")


def to_number(text: str):
    try:
        num = int(text)
        return num
    except:
        pass
    try:
        num = float(text)
        return num
    except:
        return False


def separate(q: str):
    expr = q.replace(" ", "")
    separated = []
    before = 0
    for i, ch in enumerate(expr):
        if ch in OPERANDS:
            separated.append(expr[before:i])
            separated.append(ch)
            before = i + 1
    separated.append(expr[before:])
    return separated


def multdiv(tokens: list):
    i = 0
    while i < len(tokens):
        if tokens[i] in "*/":
            n1 = to_number(tokens[i-1])
            n2 = to_number(tokens[i+1])
            if tokens[i] == "*":
                newvalue = n1 * n2
            elif tokens[i] == "/":
                newvalue = n1 / n2
            tokens[i-1:i+2] = [str(newvalue)]
        else:
            i += 1
    return tokens


def addsub(tokens: list):
    i = 0
    while i < len(tokens):
        if tokens[i] in "+-":
            n1 = to_number(tokens[i-1])
            n2 = to_number(tokens[i+1])
            if tokens[i] == "+":
                newvalue = n1 + n2
            elif tokens[i] == "-":
                newvalue = n1 - n2
            tokens[i-1:i+2] = [str(newvalue)]
        else:
            i += 1
    return tokens


def calculate(q: str):
    """The actual calculation logic"""
    try:
        validate_str(q)
    except ValueError as e:
        print(e)
        return
    separated = separate(q)
    multdiv_result = multdiv(separated)
    addsub_result = addsub(multdiv_result)
    print(addsub_result[0])


def main():
    """Entry point for the console script"""
    parser = argparse.ArgumentParser()
    parser.add_argument('q', type=str, help='query')
    args = parser.parse_args()
    calculate(args.q)


if __name__ == "__main__":
    main()
