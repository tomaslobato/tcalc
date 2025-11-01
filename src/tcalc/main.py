import argparse

DIGITS = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", " "}
OPERANDS = {"+", "-", "*", "/", "^", "√"}


def validate_str(text):
    for idx, ch in enumerate(text):
        if ch not in DIGITS and ch not in OPERANDS:
            raise ValueError(f"Invalid character: {ch}")
        if ch in "*/^" and idx == 0:
            raise ValueError(f"Expression cannot start with {ch}")
        if ch in "*/^√" and idx == len(text) - 1:
            raise ValueError(f"Expression cannot end with {ch}")


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


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:  # % = modulo
        return n == 2  # only return if it's 2, if not, it's not prime
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False  # understand later
        i += 2
    return True


def separate(q: str):
    expr = q.replace(" ", "")
    separated = []
    before = 0
    for i, ch in enumerate(expr):
        if ch in OPERANDS:
            if before < i:  # Only add if there's content
                separated.append(expr[before:i])
            separated.append(ch)
            before = i + 1
    if before < len(expr):  # Only add if there's content at the end
        separated.append(expr[before:])
    return separated


def multdiv(tokens: list):
    i = 0

    while i < len(tokens):
        if tokens[i] in "*/^":
            # safety check: Binary operators - need tokens before and after it
            if i == 0 or i + 1 >= len(tokens):
                i += 1
                continue

            n1 = to_number(tokens[i-1])
            n2 = to_number(tokens[i+1])

            if tokens[i] == "*":
                newvalue = n1 * n2
            elif tokens[i] == "/":
                newvalue = n1 / n2
            elif tokens[i] == "^":
                u = 1
                newvalue = n1
                while u < n2:  # multiply by itself n2 times
                    newvalue = newvalue * n1
                    u += 1

            # replace where n1 and n2 were for the result of it's calculation
            tokens[i-1:i+2] = [str(newvalue)]

        elif tokens[i] == "√":
            # safety check: Unary operator - only the token after it
            if i + 1 >= len(tokens):
                i += 1
                continue

            n2 = to_number(tokens[i+1])  # only get n2
            num = n2
            subtracted_times = 0
            if n2 % 2 == 0:  # even
                while num > 0:
                    num -= 4  # repeat -4
                    subtracted_times += 1  # the result is as many times as it takes to get 0
            elif n2 % 2 != 0:  # odd
                increasing_odd = 1
                while num > 0:
                    increasing_odd += 2
                    num -= increasing_odd  # subtract all increasing odd numbers until got to 0
                    subtracted_times += 1

                # result is subtracted times, replace only operator and n2 token, not n1.
                tokens[i:i+2] = [str(subtracted_times)]

        else:
            i += 1
    return tokens


def addsub(tokens: list):
    i = 0
    while i < len(tokens):
        if tokens[i] == "":
            continue
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
    parser = argparse.ArgumentParser()
    parser.add_argument('q', type=str, help='query')
    args = parser.parse_args()
    calculate(args.q)


if __name__ == "__main__":
    main()
