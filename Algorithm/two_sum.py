class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # me
        for one in range(len(nums) - 1):
            for two in range(one+1, len(nums)):
                if nums[one]+nums[two] == target:
                    return [one, two]

        # good answer
        hashmap = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in hashmap:
                return [i, hashmap[complement]]
            hashmap[nums[i]] = i