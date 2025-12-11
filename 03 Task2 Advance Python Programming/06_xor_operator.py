"""
1486. XOR Operation in an Array

You are given an integer n and an integer start.

Define an array nums where nums[i] = start + 2 * i (0-indexed) and n == nums.length.

Return the bitwise XOR of all elements of nums.

Example 1:

Input: n = 5, start = 0
Output: 8
Explanation: Array nums is equal to [0, 2, 4, 6, 8] where (0 ^ 2 ^ 4 ^ 6 ^ 8) = 8.
Where "^" corresponds to bitwise XOR operator.
Example 2:

Input: n = 4, start = 3
Output: 8
Explanation: Array nums is equal to [3, 5, 7, 9] where (3 ^ 5 ^ 7 ^ 9) = 8.
 

Constraints:

1 <= n <= 1000
0 <= start <= 1000
n == nums.length
"""

class Solution:
    def xorOperation(self, n: int, start: int) -> int:
        result = 0
        for i in range(n):
            result ^= start + 2 * i   # XOR with nums[i]
        return result


solution = Solution()

test_cases = [
    {"n": 5, "start": 0}, 
    {"n": 4, "start": 3}, 
    {"n": 1, "start": 7}, 
    {"n": 10, "start": 5},
]

for case in test_cases:
    n, start = case["n"], case["start"]
    print(f"Input: n={n}, start={start}")
    print(f"Output: {solution.xorOperation(n, start)}")
    print("-" * 40)
