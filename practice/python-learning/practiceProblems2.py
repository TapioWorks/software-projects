def find_missing(numbers):
    proper_set = sorted(set(numbers))
    sum_of_all_numbers = len(proper_set) * (len(proper_set) + 1 ) / 2
    sum_of_original_list = sum(proper_set)
    return int(sum_of_all_numbers - sum_of_original_list)


# Test cases
print(find_missing([3, 0, 1]))                    # Expected: 2
print(find_missing([0, 1]))                       # Expected: 2
print(find_missing([9, 6, 4, 2, 3, 5, 7, 0, 1])) # Expected: 8
print(find_missing([0]))                          # Expected: 1
print(find_missing([1]))                          # Expected: 0
print(find_missing([]))                            # Expected: 0