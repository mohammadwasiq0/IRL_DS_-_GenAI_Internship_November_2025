""""
338. Counting Bits

Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), ans[i] is the number of 1's in the binary representation of i.

Example 1:

Input: n = 2
Output: [0,1,1]
Explanation:
0 --> 0
1 --> 1
2 --> 10
Example 2:

Input: n = 5
Output: [0,1,1,2,1,2]
Explanation:
0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100
5 --> 101
 

Constraints:

0 <= n <= 10^5
"""

from typing import List

class Solution:
    def countBits(self, n: int) -> List[int]:
        ans = [0] * (n + 1)
        
        # Use the relation: ans[i] = ans[i >> 1] + (i & 1)
        for i in range(1, n + 1):
            ans[i] = ans[i >> 1] + (i & 1)
        
        return ans


solution = Solution()

test_cases = [
    {"n": 2},   
    {"n": 5},   
    {"n": 0},  
    {"n": 10},  
]

for case in test_cases:
    n = case["n"]
    print(f"Input: n={n}")
    print(f"Output: {solution.countBits(n)}")
    print("-" * 40)
