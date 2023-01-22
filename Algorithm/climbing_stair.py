class Solution:
    def climbStairs(self, n: int) -> int:

        n1 = 1
        n2 = 2
        if n == 1:
            return n1
        elif n == 2:
            return n2
        for i in range(n-2):
            n2, n1 = n1 + n2, n2
        return n2