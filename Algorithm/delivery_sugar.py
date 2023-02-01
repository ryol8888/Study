import sys

input = sys.stdin.readline

def solution():
    num = int(input())
    '''
    5 와 3 중 5 먼저 그 다음 3 마지막 -1
    '''
    # first
    quotient = num // 5
    isTrue = False
    for qt in range(quotient, -1, -1):
        candidate = num - qt*5
        if candidate % 3 == 0:
            print(qt+candidate//3)
            isTrue = True
            break
    if not isTrue:
        print(-1)
solution()