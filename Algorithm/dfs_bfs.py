import sys

input = sys.stdin.readline

def dfs(V, Matrix):
    stack = []
    stack.append(V)
    visit_node = [0 for _ in range(len(Matrix))]
    while stack:
        node = stack.pop()
        visit_node[node-1] = 1
        for i in range(len(Matrix)):
            if Matrix[node][i] == 1 and visit_node[i] == 0:
                stack.append(i)
                break

def bfs(V):
    pass

def solution():
    N, M, V = map(int, input().split(" "))
    Matrix = [[0 for _ in range(N)] for _ in range(N)]
    for _ in range(M):
        i, j = map(int, input().split(" "))
        Matrix[i][j] = Matrix[j][i] = 1
    

solution()    