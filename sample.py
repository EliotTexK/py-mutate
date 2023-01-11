# python solution to the first leetcode problem
# sample code - I stole it from https://www.tutorialspoint.com/two-sum-in-python
class Solution(object):
   def twoSum(self, nums, target):
      required = {}
      for i in range(len(nums)):
         if target - nums[i] in required:
            return [required[target - nums[i]],i]
         else:
            required[nums[i]]=i
input_list = [2,8,12,15]
ob1 = Solution()
print(ob1.twoSum(input_list, 20))