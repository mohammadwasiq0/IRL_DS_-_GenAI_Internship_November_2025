"""
1512. Number of Good Pairs

Given an array of integers nums, return the number of good pairs.

A pair (i, j) is called good if nums[i] == nums[j] and i < j.


Example 1:

Input: nums = [1,2,3,1,1,3]
Output: 4
Explanation: There are 4 good pairs (0,3), (0,4), (3,4), (2,5) 0-indexed.
Example 2:

Input: nums = [1,1,1,1]
Output: 6
Explanation: Each pair in the array are good.
Example 3:

Input: nums = [1,2,3]
Output: 0
 

Constraints:

1 <= nums.length <= 100
1 <= nums[i] <= 100
"""

from collections import Counter
from typing import List

class Solution:
    def numIdenticalPairs(self, nums: List[int]) -> int:
        freq = Counter(nums)
        count = 0
        # For each number, if it appears k times, it contributes k*(k-1)/2 pairs
        for k in freq.values():
            count += k * (k - 1) // 2
        return count


solution = Solution()

test_cases = [
    {"nums": [1,2,3,1,1,3]},   
    {"nums": [1,1,1,1]},       
    {"nums": [1,2,3]},         
    {"nums": [5,5,5,5,5]},  
    {"nums": [10,20,30,40]},
]

for case in test_cases:
    nums = case["nums"]
    print(f"Input: nums={nums}")
    print(f"Output: {solution.numIdenticalPairs(nums)}")
    print("-" * 40)

