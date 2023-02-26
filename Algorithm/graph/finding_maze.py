# 최소의 칸수 -> BFS , 표만들고 갱신하는 방식

import sys
input = sys.stdin.readline
from collections import deque


def bfs(graph, V):
    queue = deque()
    queue.append(V)
    while queue:
        i, j = queue.popleft()
        dx = (-1, 1, 0, 0)
        dy = (0, 0, -1, 1)
        for nx, ny in zip(dx, dy):
            new_i = i+nx
            new_j = j+ny
            if -1 < new_i < len(graph) and -1 < new_j < len(graph[0]) and graph[new_i][new_j] == 1:
                graph[new_i][new_j] += graph[i][j]
                queue.append((new_i,new_j))
   

N, M = map(int, input().rstrip().split(" "))

maze = [[0 for i in range(M)] for i in range(N)]

for i in range(N):
    info = input().rstrip()
    for j, num in enumerate(info):
        if int(num):
            maze[i][j] = 1
bfs(maze, (0,0))
print(maze[N-1][M-1])


