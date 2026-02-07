# Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
# You may assume that each input would have exactly one solution, and you may not use the same element twice.
# You can return the answer in any order.

# Example 1:
# Input: nums = [2,7,11,15], target = 9 # Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
# Example 2:
# Input: nums = [3,2,4], target = 6 # Output: [1,2]
# Example 3:
# Input: nums = [3,3], target = 6 # Output: [0,1]
#========================================
# time complexity is O(n²) for sol1 class
#========================================
class sol1:
    def sum(self, nums:list, target:int)-> list[int]:
        len_nums= len(nums)
        for i in range(len_nums):
            for j in range(i,len_nums):
                if nums[i]+num[j] == target:
                    print([i,j])
                    break
s1 = sol1()
num = [1,2,3]
target = 5
s1.sum(num,target)