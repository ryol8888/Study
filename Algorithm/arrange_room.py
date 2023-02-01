import sys

input = sys.stdin.readline

def solution():
    num = int(input())
    room = []
    for _ in range(num):
        st_time, end_time = map(int, input().split(" "))
        room.append([st_time, end_time])
    room.sort(key= lambda x: x[0])
    room.sort(key= lambda x: x[1])
            
    cnt = 1
    end = room[0][1]
    for i in range(1, num):
        if room[i][0] >= end:
            cnt += 1
            end = room[i][1]

    print(cnt)
        
solution()