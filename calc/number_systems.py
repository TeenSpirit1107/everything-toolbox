from fractions import Fraction

VALID_BASES = (2, 8, 10, 16)
DIGITS = "0123456789ABCDEF"
MAX_FRAC_DIGITS = 48


def int_to_base(n: int, base: int) -> str:
    if base == 10:
        return str(n)
    if n == 0:
        return "0"
    sign = ""
    if n < 0:
        sign = "-"
        n = -n
    parts = []
    while n:
        n, rem = divmod(n, base)
        parts.append(DIGITS[rem])
    return sign + "".join(reversed(parts))


def parse_in_base(s: str, base: int) -> int | None:
    s = s.strip()
    if not s:
        return None
    try:
        return int(s, base)
    except ValueError:
        return None


def parse_rational_in_base(s: str, base: int) -> Fraction | None:
    s = s.strip()
    if not s or "." not in s:
        return None

    sign = 1
    if s[0] in "+-":
        if s[0] == "-":
            sign = -1
        s = s[1:].strip()
        if not s:
            return None

    parts = s.split(".")
    if len(parts) != 2:
        return None

    int_s, frac_s = parts
    if not int_s and not frac_s:
        return None

    try:
        int_val = int(int_s or "0", base)
    except ValueError:
        return None

    frac_val = Fraction(0)
    for i, ch in enumerate(frac_s, start=1):
        try:
            d = int(ch, base)
        except ValueError:
            return None
        if d >= base:
            return None
        frac_val += Fraction(d, base**i)

    return sign * (int_val + frac_val)


def fractional_to_base(frac: Fraction, base: int, max_digits: int) -> tuple[str, bool]:
    """Expand fractional part in (0, 1). Returns (digit string, exact)."""
    if frac == 0:
        return "", True

    digits: list[str] = []
    f = frac
    for _ in range(max_digits):
        f *= base
        d = f.numerator // f.denominator
        digits.append(DIGITS[d])
        f -= d
        if f == 0:
            return "".join(digits), True
    return "".join(digits), False


def rational_to_base(value: Fraction, base: int, max_frac_digits: int = MAX_FRAC_DIGITS) -> str:
    if value == 0:
        return "0"

    sign = ""
    if value < 0:
        sign = "-"
        value = -value

    int_part = value.numerator // value.denominator
    frac = value - int_part

    if frac == 0:
        return sign + int_to_base(int_part, base)

    int_str = int_to_base(int_part, base) if int_part != 0 else "0"
    frac_str, exact = fractional_to_base(frac, base, max_frac_digits)
    suffix = "" if exact else "..."
    return sign + int_str + "." + frac_str + suffix


def prompt_base(prompt: str, exclude: int | None = None) -> int | None:
    while True:
        print("2. Binary")
        print("8. Octal")
        print("10. Decimal")
        print("16. Hexadecimal")
        print("x. Back / exit this step")
        choice = input(prompt).strip()
        if choice.lower() == "x":
            return None
        try:
            base = int(choice)
        except ValueError:
            print("Invalid choice. Enter 2, 8, 10, or 16.")
            continue
        if base not in VALID_BASES:
            print("Invalid choice. Enter 2, 8, 10, or 16.")
            continue
        if exclude is not None and base == exclude:
            print("Target base must differ from source base. Choose again.")
            continue
        return base


def call_base_conversion():
    from_base = prompt_base("Select source base (from): ")
    if from_base is None:
        return

    to_base = prompt_base("Select target base (to): ", exclude=from_base)
    if to_base is None:
        return

    print(
        f"Converting from base {from_base} to base {to_base}. "
        f"Enter integers or decimals (non-terminating fractions end with ...). "
        f"Enter x to exit."
    )
    while True:
        raw = input(f"Enter a number in base {from_base}: ").strip()
        if raw.lower() == "x":
            return

        if "." in raw:
            value = parse_rational_in_base(raw, from_base)
            if value is None:
                print("Invalid input. Enter a valid integer or decimal for the selected base.")
                continue
            result = rational_to_base(value, to_base)
        else:
            value = parse_in_base(raw, from_base)
            if value is None:
                print("Invalid input. Enter a valid integer or decimal for the selected base.")
                continue
            result = int_to_base(value, to_base)

        print(f"{raw} (base {from_base}) -> {result} (base {to_base})")


if __name__ == "__main__":
    while True:
        print("1. Base conversion (integers or decimals)")
        print("x. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            call_base_conversion()
        elif choice.lower() == "x":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
