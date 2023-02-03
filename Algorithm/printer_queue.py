import sys
from collections import deque

tc = int(sys.stdin.readline())

for _ in range(tc):
    n, wtk = map(int, sys.stdin.readline().split())
    li = list(map(int, sys.stdin.readline().split()))
    que = deque([(i, li[i]) for i in range(len(li))])
    li.sort(reverse=True)
    k = 0
    for el in li:
        while que[0][1] != el:
            tmp = que.popleft()
            que.append(tmp)
        k += 1
        if que.popleft()[0] == wtk:
            break
    print(k)