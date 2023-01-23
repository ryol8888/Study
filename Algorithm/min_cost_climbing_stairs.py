class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        minCost = [0] * (len(cost))
        minCost[0] = cost[0]
        minCost[1] = cost[1]

        for i in range(2, len(cost)):
            if minCost[i - 1] > minCost[i - 2]:
                minCost[i] += (cost[i] + minCost[i - 2])
            else:
                minCost[i] += (cost[i] + minCost[i - 1])
        print(minCost)
        if minCost[-1] < minCost[-2]:
            return minCost[-1]
        else:
            return minCost[-2]