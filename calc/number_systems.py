import struct
from collections.abc import Callable
from fractions import Fraction
from typing import TypeVar

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


T = TypeVar("T")


def prompt_validated_input(
    prompt: str,
    parse_fn: Callable[[str], T | None],
    invalid_message: str,
) -> tuple[str, T] | None:
    while True:
        raw = input(prompt).strip()
        if raw.lower() == "x":
            return None
        parsed = parse_fn(raw)
        if parsed is None:
            print(invalid_message)
            continue
        return raw, parsed


def parse_decimal_number(s: str) -> float | None:
    s = s.strip()
    if not s:
        return None
    if "." in s:
        value = parse_rational_in_base(s, 10)
        if value is None:
            return None
        return float(value)
    int_val = parse_in_base(s, 10)
    if int_val is None:
        return None
    return float(int_val)


def parse_ieee754_single_bits(s: str) -> int | None:
    compact = s.strip().replace(" ", "").replace("_", "")
    if not compact:
        return None
    lower = compact.lower()
    if lower.startswith("0b"):
        compact = compact[2:]
    elif lower.startswith("0x"):
        compact = compact[2:]
        if len(compact) != 8:
            return None
        try:
            bits = int(compact, 16)
        except ValueError:
            return None
        if bits < 0 or bits > 0xFFFFFFFF:
            return None
        return bits

    if len(compact) == 8 and all(ch in "0123456789ABCDEFabcdef" for ch in compact):
        try:
            bits = int(compact, 16)
        except ValueError:
            return None
        return bits

    if len(compact) != 32 or any(ch not in "01" for ch in compact):
        return None
    return int(compact, 2)


def float_to_ieee754_single_bits(value: float) -> int:
    return struct.unpack(">I", struct.pack(">f", value))[0]


def ieee754_single_bits_to_float(bits: int) -> float:
    return struct.unpack(">f", struct.pack(">I", bits & 0xFFFFFFFF))[0]


def format_ieee754_single(bits: int) -> str:
    binary = f"{bits:032b}"
    sign, exponent, fraction = binary[0], binary[1:9], binary[9:]
    hex_repr = f"0x{bits:08X}"
    return (
        f"{sign} {exponent} {fraction} (32-bit, sign / exponent / fraction); hex {hex_repr}"
    )


def call_fixed_point_conversion():
    print("Fixed point conversion is not implemented yet.")


def call_ieee754_single_conversion():
    print(
        "IEEE 754 single precision (32-bit: 1 sign bit, 8 exponent bits, 23 fraction bits)."
    )
    while True:
        print("1. Decimal -> IEEE 754 single precision")
        print("2. IEEE 754 single precision -> decimal")
        print("x. Back / exit this step")
        direction = input("Select conversion direction: ").strip()
        if direction.lower() == "x":
            return
        if direction not in ("1", "2"):
            print("Invalid choice. Enter 1, 2, or x.")
            continue

        if direction == "1":
            print(
                "Enter a decimal number (integer or decimal). "
                "Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "Decimal: ",
                    parse_decimal_number,
                    "Invalid input. Enter a valid decimal integer or decimal fraction.",
                )
                if entry is None:
                    break
                raw, value = entry
                bits = float_to_ieee754_single_bits(value)
                print(f"{raw} -> {format_ieee754_single(bits)}")
        else:
            print(
                "Enter IEEE 754 single precision as 32 binary digits, "
                "8 hex digits, or 0x-prefixed hex. Enter x to go back."
            )
            while True:
                entry = prompt_validated_input(
                    "IEEE 754 single: ",
                    parse_ieee754_single_bits,
                    "Invalid input. Use 32 bits (0/1), 8 hex digits, or 0x........",
                )
                if entry is None:
                    break
                raw, bits = entry
                value = ieee754_single_bits_to_float(bits)
                print(f"{raw} -> {value} ({format_ieee754_single(bits)})")


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
    invalid_msg = "Invalid input. Enter a valid integer or decimal for the selected base."

    def parse_number_in_from_base(raw: str) -> str | None:
        if "." in raw:
            value = parse_rational_in_base(raw, from_base)
            if value is None:
                return None
            return rational_to_base(value, to_base)
        value = parse_in_base(raw, from_base)
        if value is None:
            return None
        return int_to_base(value, to_base)

    while True:
        entry = prompt_validated_input(
            f"Enter a number in base {from_base}: ",
            parse_number_in_from_base,
            invalid_msg,
        )
        if entry is None:
            return
        raw, result = entry
        print(f"{raw} (base {from_base}) -> {result} (base {to_base})")


if __name__ == "__main__":
    while True:
        print("1. Base conversion (integers or decimals)")
        print("2. Fixed point conversion")
        print("3. Floating point conversion (IEEE 754 single precision)")
        print("x. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            call_base_conversion()
        elif choice == "2":
            call_fixed_point_conversion()
        elif choice == "3":
            call_ieee754_single_conversion()
        elif choice.lower() == "x":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
