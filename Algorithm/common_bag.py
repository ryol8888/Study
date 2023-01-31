import sys

# input = sys.stdin.readline

# def solution():
#     N, K = map(int, input().split())
#     weight_dict = {}
#     min_w = float("INF") 
    
#     for _ in range(N):
#         weight, value = map(int, input().split())
#         if weight in weight_dict:
#             if weight_dict[weight] < value:
#                 weight_dict[weight] = value
#         else:
#             weight_dict[weight] = value
#         if min_w > weight:
#             min_w = weight

#     '''
#     모든 K를 돌면서 값을 구하기 싫다. = 10만인데?
#     일단 해봐.
#     K 값 중 wieght_dict에 있으면 value값 보고 이 전값과 비교
#     '''
#     # bottom-up
#     bag = {}
#     for i in range(K):
#         if i in weight_dict:
#             bag[i] = max(bag[i-1], weight_dict[i])
#         else:
#             bag[i] = bag[i-1]
#     '''
#     각 W 마다 가지고 있는 가장 큰 value dict이 있고
#     작은 w 부터 K 무게가 될 떄까지 구해보자.
#     bag = {}
#     for idx, k in enumerate(sorted(weight_dict.keys())):
#         bag[k] = weight_dict[k]
#     '''

def knapsack(W, wt, val, n):  # W: 배낭의 무게한도, wt: 각 보석의 무게, val: 각 보석의 가격, n: 보석의 수
    K = [[0 for x in range(W+1)] for x in range(n+1)]  # DP를 위한 2차원 리스트 초기화
    for i in range(n+1):
        for w in range(W+1):  # 각 칸을 돌면서
            if i==0 or w==0:  # 0번째 행/열은 0으로 세팅
                K[i][w] = 0
            elif wt[i-1] <= w:  # 점화식을 그대로 프로그램으로
                K[i][w] = max(val[i-1]+K[i-1][w-wt[i-1]], K[i-1][w])  # max 함수 사용하여 큰 것 선택
            else:
                K[i][w] = K[i-1][w]
    return K[n][W]
    
    
wt = []
val = []
N, K = map(int, sys.stdin.readline().strip().split())
for i in range(N):
    w, v = map(int, sys.stdin.readline().strip().split())
    wt.append(w)
    val.append(v)
print(knapsack(K, wt, val, N))
        