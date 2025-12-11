"""
1295. Find Numbers with Even Number of Digits

Given an array nums of integers, return how many of them contain an even number of digits.

Example 1:

Input: nums = [12,345,2,6,7896]
Output: 2
Explanation: 
12 contains 2 digits (even number of digits). 
345 contains 3 digits (odd number of digits). 
2 contains 1 digit (odd number of digits). 
6 contains 1 digit (odd number of digits). 
7896 contains 4 digits (even number of digits). 
Therefore only 12 and 7896 contain an even number of digits.
Example 2:

Input: nums = [555,901,482,1771]
Output: 1 
Explanation: 
Only 1771 contains an even number of digits.
 

Constraints:

1 <= nums.length <= 500
1 <= nums[i] <= 10^5
"""

from typing import List

class Solution:
    def findNumbers(self, nums: List[int]) -> int:
        count = 0
        for num in nums:
            # Convert number to string and check length
            if len(str(num)) % 2 == 0:
                count += 1
        return count


solution = Solution()

test_cases = [
    {"nums": [12, 345, 2, 6, 7896]},       
    {"nums": [555, 901, 482, 1771]},       
    {"nums": [1, 22, 333, 4444]},          
    {"nums": [100000]},                   
    {"nums": [7, 88, 999, 1000, 12345]},   
]

for case in test_cases:
    nums = case["nums"]
    print(f"Input: nums={nums}")
    print(f"Output: {solution.findNumbers(nums)}")
    print("-" * 40)
