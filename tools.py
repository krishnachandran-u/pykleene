def get_all_strings(alphabets: list, length: int) -> list[str]:
    if length < 0:
        raise Exception(f"Inside get_all_strings: variable length cannot be negative")
    if length == 0:
        return [""]
    strings = []
    for string in get_all_strings(alphabets, length - 1):
        for alphabet in alphabets:
            strings.append(string + alphabet)
    return strings

def get_next_letter(letter: str) -> str:
    if letter == 'z':
        return 'a'
    if letter == 'Z':
        return 'A'
    return chr(ord(letter) + 1)