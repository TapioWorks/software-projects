class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i, x in enumerate(nums):
            for j, y in enumerate(nums):
                if x + y == target and i != j:
                    return [i, j]




solution = Solution()

nums = [2, 7, 11, 15]
target = 9

print(solution.twoSum(nums, target))