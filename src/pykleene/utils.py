def getAllStrings(alphabets: list, length: int) -> list[str]:
    if length < 0:
        raise Exception(f"Inside get_all_strings: variable length cannot be negative")
    result = [""]  
    all_results = [""] 
    for current_length in range(1, length + 1):
        new_strings = []
        for string in result:
            for alphabet in alphabets:
                new_strings.append(string + alphabet)
        result = new_strings 
        all_results.extend(result) 
    return all_results

def _getNextLetter(char: str) -> str:
    if char == 'Z':
        return 'A'
    if char == 'z':
        return 'a'
    if char == '9':
        return '0'
    return chr(ord(char) + 1)

def randomDarkColor() -> str:
    from random import randint
    r = randint(50, 150)
    g = randint(50, 150)
    b = randint(50, 150)
    return f'#{r:02x}{g:02x}{b:02x}'  