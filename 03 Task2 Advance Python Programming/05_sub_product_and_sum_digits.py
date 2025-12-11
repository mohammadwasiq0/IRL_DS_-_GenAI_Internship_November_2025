"""
1281. Subtract the Product and Sum of Digits of an Integer

Given an integer number n, return the difference between the product of its digits and the sum of its digits.
 

Example 1:

Input: n = 234
Output: 15 
Explanation: 
Product of digits = 2 * 3 * 4 = 24 
Sum of digits = 2 + 3 + 4 = 9 
Result = 24 - 9 = 15
Example 2:

Input: n = 4421
Output: 21
Explanation: 
Product of digits = 4 * 4 * 2 * 1 = 32 
Sum of digits = 4 + 4 + 2 + 1 = 11 
Result = 32 - 11 = 21
 

Constraints:

1 <= n <= 10^5
"""

class Solution:
    def subtractProductAndSum(self, n: int) -> int:
        product = 1
        total_sum = 0
        
        # Process each digit
        for digit in str(n):
            d = int(digit)
            product *= d
            total_sum += d
        
        return product - total_sum


solution = Solution()

test_cases = [
    {"n": 234},  
    {"n": 4421}, 
    {"n": 5},    
    {"n": 101},  
    {"n": 99999},
]

for case in test_cases:
    n = case["n"]
    print(f"Input: n={n}")
    print(f"Output: {solution.subtractProductAndSum(n)}")
    print("-" * 40)
