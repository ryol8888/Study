import sys

input = sys.stdin.readline

def mySolution():
    for _ in range(int(input())):
        inputs = list(map(int, input().split(" ")))
        a, b = inputs[0], inputs[1]
        if a == b:
            answer = factorial(b) // factorial(a)
        else:
            answer = factorial(b) // (factorial(a) * factorial(b-a))
        print(answer)
        
def dp():
    for _ in range(int(input())):
        N, M = map(int, input().split(" "))
        a = b = 1
        for i in range(M, M-N, -1):
            a *= i
        for i in range(N, 1, -1):
            b *= i
        print(int(a/b))
        
def built_in_func():
    import math
    for _ in range(int(input())):
        N, M = map(int, input().split(" "))
        print(int(math.comb(M, N)))
    
built_in_func()
