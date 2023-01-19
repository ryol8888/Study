# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        min_version = n + 1
        left = 1
        right = n
        while left <= right:
            mid = (left + right) // 2
            if isBadVersion(mid):
                if min_version > mid:
                    min_version = mid
                right = mid - 1
            else:
                left = mid + 1
        return min_version