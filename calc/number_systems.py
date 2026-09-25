VALID_BASES = (2, 8, 10, 16)


def int_to_base(n: int, base: int) -> str:
    if base == 10:
        return str(n)
    if n == 0:
        return "0"
    sign = ""
    if n < 0:
        sign = "-"
        n = -n
    digits = "0123456789ABCDEF"
    parts = []
    while n:
        n, rem = divmod(n, base)
        parts.append(digits[rem])
    return sign + "".join(reversed(parts))


def parse_in_base(s: str, base: int) -> int | None:
    s = s.strip()
    if not s:
        return None
    try:
        return int(s, base)
    except ValueError:
        return None


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

    print(f"Converting from base {from_base} to base {to_base}. Enter x to exit.")
    while True:
        raw = input(f"Enter a number in base {from_base}: ").strip()
        if raw.lower() == "x":
            return
        value = parse_in_base(raw, from_base)
        if value is None:
            print("Invalid input. Enter a valid number for the selected base.")
            continue
        result = int_to_base(value, to_base)
        print(f"{raw} (base {from_base}) -> {result} (base {to_base})")


if __name__ == "__main__":
    while True:
        print("1. Base conversion")
        print("x. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            call_base_conversion()
        elif choice.lower() == "x":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
