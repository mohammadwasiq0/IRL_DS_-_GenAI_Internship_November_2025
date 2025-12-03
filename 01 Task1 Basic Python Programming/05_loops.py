"""
Task
The provided code stub reads an integer, n, from STDIN. For all non-negative integers i<n, print i^2.

Example
n=3

The list of non-negative integers that are less than n=3 is [1, 2, 3]. Print the square of each number on a separate line.

0
1
4
"""

if __name__ == '__main__':
    # Read integer from STDIN
    n = int(input().strip())

    # Loop through all non-negative integers less than n
    for i in range(n):
        print(i ** 2)
