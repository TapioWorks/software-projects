class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(nums) != len(set(nums))


solution = Solution()

numbers = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]

print(solution.containsDuplicate(numbers))