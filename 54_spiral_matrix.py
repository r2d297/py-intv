
# Spiral Matrix, boundary simulation
from typing import List

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []      # result container 
        
        # if matrix is empty, return empty result
        if not matrix or not matrix[0]:
            return res
        
        # m rows, n cols
        row, col = len(matrix), len(matrix[0])
        # boundaries for current layer
        top, bottom = 0, row  - 1          # current top row index, bottom row index
        left, right = 0, col - 1          # current left col index, right col index   

        # loop until boundaries cross
        while top <= bottom and left <= right:
            # traverse from left to right on the top row
            for c in range(left, right + 1):
                res.append(matrix[top][c])      # collect top row elements
            top += 1                             # shrink top boundary

            # traverse from top to bottom on the right column
            for r in range(top, bottom + 1):
                res.append(matrix[r][right])     # collect right column elements
            right -= 1                           # shrink right boundary

            # safeguard for single row or single column remaining
            if top <= bottom:
                # traverse from right to left on the bottom row
                for c in range(right, left - 1, -1):
                    res.append(matrix[bottom][c])  # collect bottom row elements
                bottom -= 1                         # shrink bottom boundary

            if left <= right:
                # traverse from bottom to top on the left column
                for r in range(bottom, top - 1, -1):
                    res.append(matrix[r][left])     # collect left column elements
                left += 1                            # shrink left boundary

        return res
