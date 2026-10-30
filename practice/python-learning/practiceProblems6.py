class Solution:
    """
    Problem: Second Largest Number

    Given a list of numbers, find and return the second largest
    distinct number.

    Examples:
        [1, 5, 3, 9, 2] -> 5
        [10, 10, 8, 7] -> 8
        [1, 2] -> 1

    If there is no second distinct number, return None.

    Concepts practiced:
    - Lists
    - Loops
    - Comparisons
    - Handling duplicates
    - Edge cases
    """

    def second_largest(self, numbers: list[int]) -> int | None:
        proper_set = sorted(set(numbers))
        if len(proper_set) <= 1:
            return None

        return proper_set[-2]




# Create a Solution object
solution = Solution()

# Test cases
print(solution.second_largest([1, 5, 3, 9, 2]))  # Expected: 5
print(solution.second_largest([10, 10, 8, 7]))   # Expected: 8
print(solution.second_largest([1, 2]))            # Expected: 1
print(solution.second_largest([5]))               # Expected: None
print(solution.second_largest([5, 5, 5]))         # Expected: None
print(solution.second_largest([]))                # Expected: None
