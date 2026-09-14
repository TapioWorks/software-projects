def second_largest(numbers):
    proper_set = sorted(set(numbers), reverse=True)

    if len(proper_set) <= 1:
        return None

    second_largest_number = proper_set[1]
    return second_largest_number



print(second_largest([4, 1, 7, 3]))       # Expected: 4
print(second_largest([10, 10, 5, 3]))     # Expected: 5
print(second_largest([-2, -8, -1]))       # Expected: -2
print(second_largest([5]))                # Expected: None
print(second_largest([5, 5, 5]))          # Expected: None
print(second_largest([]))                 # Expected: None
