import sys
input = sys.stdin.readline

# 해당 node를 방문 처리 후 인접한 node를 다시 탐색한다.
# 방문할 곳이 없다면 탐색을 종료한다.

# recursive
def dfs_rec(graph, visit_node, node):
    if not node in visit_node:
        visit_node.append(node)
        if graph[node]:
            for idx in range(len(graph[node])):
                if graph[node][idx] == 1:
                    dfs_rec(graph, visit_node, idx)
        


def bfs(graph, start, visit_node):
    queue = [start]
    visit_node.append(start)
    while queue:
        v = queue.pop(0)
        for i in range(len(graph[v])):
            if graph[v][i] == 1 and not i in visit_node:
                queue.append(i)
                visit_node.append(i)
        

def solution():
    # make graph
    N, M, V = map(int, input().split(" "))
    graph = [[0 for _ in range(N+1)] for _ in range(N+1)]
    dfs = []
    bfs_list = []
    for _ in range(M):
        V1, V2 = map(int, input().split(" "))
        graph[V1][V2] = 1
        graph[V2][V1] = 1
    
    # dfs recursive
    dfs_rec(graph, dfs, V)
    bfs(graph, V, bfs_list)
    
    print(dfs)
    print(bfs_list)
    
    

solution()    
