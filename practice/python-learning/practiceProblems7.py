class Solution:
    """
    Problem: Most Common Number

    Given a list of numbers, find and return the number that appears
    the most times.

    If two or more numbers have the same highest frequency, return
    the number that appears first in the original list.

    Examples:
        [1, 2, 2, 3, 3, 3] -> 3
        [5, 5, 1, 1, 1] -> 1
        [7] -> 7
        [4, 4, 2, 2, 7] -> 4

    If the list is empty, return None.
    """

    def most_common(self, numbers: list[int]) -> int | None:
        numdic = {}
        for x in numbers:
            if x in numdic:
                numdic[x] += 1
            else:
                numdic[x] = 1

        highest = 0
        answer = None

        for x in numbers:
            if numdic[x] > highest:
                highest = numdic[x]
                answer = x

        return answer


# Create a Solution object
solution = Solution()


# Test cases
print(solution.most_common([1, 2, 2, 3, 3, 3]))  # Expected: 3
print(solution.most_common([5, 5, 1, 1, 1]))      # Expected: 1
print(solution.most_common([7]))                  # Expected: 7
print(solution.most_common([2, 2, 4, 4, 7]))      # Expected: 2
print(solution.most_common([]))                   # Expected: None
