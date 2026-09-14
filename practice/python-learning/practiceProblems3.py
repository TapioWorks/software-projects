def first_unique_character(text):
    counts = {}

    for character in text:
        if character in counts:
            counts[character] += 1
        else:
            counts[character] = 1

    for character in text:
        if counts[character] == 1:
            return character

    return None

# Test cases
print(first_unique_character("swiss"))       # Expected: "w"
print(first_unique_character("hello"))       # Expected: "h"
print(first_unique_character("aabbcc"))      # Expected: None
print(first_unique_character("abcabcde"))    # Expected: "d"
print(first_unique_character(""))             # Expected: None
print(first_unique_character("a"))            # Expected: "a"
print(first_unique_character("AaBbA"))        # Expected: "a"
