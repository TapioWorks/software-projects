class Solution:
    """
    Problem: Most Frequent Odd Number

    Given a list of integers, return the odd number that appears
    the most times.

    If two or more odd numbers have the same highest frequency,
    return the one that appears first in the original list.

    Even numbers should be completely ignored.

    If there are no odd numbers, return None.

    Examples:
        [2, 3, 3, 4, 5, 5, 5] -> 5
        [1, 2, 1, 3, 3] -> 1
        [2, 4, 6] -> None
        [7, 7, 3, 3, 5] -> 7
        [9] -> 9
        [] -> None
    """

    def most_frequent_odd(self, numbers: list[int]) -> int | None:
        pass


# Create a Solution object
solution = Solution()


# Test cases
print(solution.most_frequent_odd([2, 3, 3, 4, 5, 5, 5]))  # Expected: 5
print(solution.most_frequent_odd([1, 2, 1, 3, 3]))          # Expected: 1
print(solution.most_frequent_odd([2, 4, 6]))                # Expected: None
print(solution.most_frequent_odd([7, 7, 3, 3, 5]))          # Expected: 7
print(solution.most_frequent_odd([9]))                      # Expected: 9
print(solution.most_frequent_odd([]))                       # Expected: None
