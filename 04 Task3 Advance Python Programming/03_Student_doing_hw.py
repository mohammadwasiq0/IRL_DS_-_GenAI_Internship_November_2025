"""
1450. Number of Students Doing Homework at a Given Time

Given two integer arrays startTime and endTime and given an integer queryTime.

The ith student started doing their homework at the time startTime[i] and finished it at time endTime[i].

Return the number of students doing their homework at time queryTime. More formally, return the number of students where queryTime lays in the interval [startTime[i], endTime[i]] inclusive.

 

Example 1:

Input: startTime = [1,2,3], endTime = [3,2,7], queryTime = 4
Output: 1
Explanation: We have 3 students where:
The first student started doing homework at time 1 and finished at time 3 and wasn't doing anything at time 4.
The second student started doing homework at time 2 and finished at time 2 and also wasn't doing anything at time 4.
The third student started doing homework at time 3 and finished at time 7 and was the only student doing homework at time 4.
Example 2:

Input: startTime = [4], endTime = [4], queryTime = 4
Output: 1
Explanation: The only student was doing their homework at the queryTime.
 

Constraints:

startTime.length == endTime.length
1 <= startTime.length <= 100
1 <= startTime[i] <= endTime[i] <= 1000
1 <= queryTime <= 1000
"""


from typing import List

class Solution:
    def busyStudent(self, startTime: List[int], endTime: List[int], queryTime: int) -> int:
        count = 0
        for i in range(len(startTime)):
            # Check if queryTime lies in [startTime[i], endTime[i]]
            if startTime[i] <= queryTime <= endTime[i]:
                count += 1
        return count


solution = Solution()

test_cases = [
    {"startTime": [1,2,3], "endTime": [3,2,7], "queryTime": 4},   
    {"startTime": [4], "endTime": [4], "queryTime": 4},           
    {"startTime": [1,1,1], "endTime": [1,1,1], "queryTime": 1},  
    {"startTime": [2,5,7], "endTime": [4,6,8], "queryTime": 5},   
]

for case in test_cases:
    startTime, endTime, queryTime = case["startTime"], case["endTime"], case["queryTime"]
    print(f"Input: startTime={startTime}, endTime={endTime}, queryTime={queryTime}")
    print(f"Output: {solution.busyStudent(startTime, endTime, queryTime)}")
    print("-" * 40)
