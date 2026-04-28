import hmac
import hashlib

SECRET_KEY = b"largest_wins"

def hash_int_to_6_digits(n: int) -> str:
    msg = str(n).encode("utf-8")

    digest = hmac.new(
        SECRET_KEY,
        msg,
        hashlib.sha256
    ).digest()

    value = int.from_bytes(digest, "big") % 1_000_000

    return f"{value:06d}"


# 输入：一行里输入多个整数，用空格分隔
# nums = list(map(int, input("Enter integers: ").split()))
nums = [0,1,2,3,4]

for n in nums:
    print(n, "->", hash_int_to_6_digits(n))
