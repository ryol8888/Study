
'''
하나의 기준으로 오름차순 정렬.
처음껀 합격
그 이후 맨 마지막 친구보다 더 떨어지는 친구가 있으면 pop

'''

import sys

input = sys.stdin.readline

def solution():
    T = int(input())
    for _ in range(T):
        candidates = []
        N = int(input())
        for _ in range(N):
            D, I = map(int, input().split(" "))
            candidates.append([D, I])
            
        # Document 로 정렬
        candidates.sort(key=lambda x: x[0])
        count = 1
        temp = candidates[0][1]
        for idx in range(1, len(candidates)):
            if temp > candidates[idx][1]:
                temp = candidates[idx][1]
                count += 1
        print(count)
solution()