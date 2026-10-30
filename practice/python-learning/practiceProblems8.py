class Solution:
    """
    Problem: First Repeated Number

    Given a list of numbers, find and return the first number that
    appears more than once.

    "First" means the number whose second occurrence happens earliest
    while scanning the list from left to right.

    If no number appears more than once, return None.

    Examples:
        [1, 2, 3, 2, 4, 1] -> 2
        [5, 5, 1, 2, 3] -> 5
        [7, 8, 9] -> None
        [4, 2, 4, 2] -> 4
        [3] -> None

    If the list is empty, return None.
    """

    def first_repeated(self, numbers: list[int]) -> int | None:
        counts = {}
        for x in numbers:
            if x in counts:
                return x
            else:
                counts[x] = 1


# Create a Solution object
solution = Solution()


# Test cases
print(solution.first_repeated([1, 2, 3, 2, 4, 1]))  # Expected: 2
print(solution.first_repeated([5, 5, 1, 2, 3]))      # Expected: 5
print(solution.first_repeated([7, 8, 9]))             # Expected: None
print(solution.first_repeated([4, 2, 4, 2]))          # Expected: 4
print(solution.first_repeated([3]))                   # Expected: None
print(solution.first_repeated([]))                    # Expected: None
