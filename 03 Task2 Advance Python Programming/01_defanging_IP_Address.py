"""
1108. Defanging an IP Address

Given a valid (IPv4) IP address, return a defanged version of that IP address.

A defanged IP address replaces every period "." with "[.]".


Example 1:

Input: address = "1.1.1.1"
Output: "1[.]1[.]1[.]1"
Example 2:

Input: address = "255.100.50.0"
Output: "255[.]100[.]50[.]0"
 

Constraints:

The given address is a valid IPv4 address.
"""

class Solution:
    def defangIPaddr(self, address: str) -> str:
        # Replace every '.' with '[.]'
        return address.replace(".", "[.]")


solution = Solution()

test_cases = [
    "1.1.1.1",     
    "255.100.50.0",
    "192.168.0.1",
    "10.0.0.255",      
]

for address in test_cases:
    print(f"Input: {address}")
    print(f"Output: {solution.defangIPaddr(address)}")
    print("-" * 40)
