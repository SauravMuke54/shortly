CHARACTERS = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)


def encode_base62(number: int) -> str:
    if number == 0:
        return CHARACTERS[0]

    result = []

    while number > 0:
        number, remainder = divmod(number, 62)
        result.append(CHARACTERS[remainder])

    return "".join(reversed(result))


def decode_base62(value: str) -> int:
    number = 0

    for char in value:
        number = number * 62 + CHARACTERS.index(char)

    return number