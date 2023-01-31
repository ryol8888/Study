import sys

# input = sys.stdin.readline

def mySolution():
    '''
    떠오르는건 bottom-up 근데 N이 커서 안될듯?
    숫자를 작게 만들 수 있는건 3으로 나누는 것.
    '''
    # bottom-up
    x=int(input()) # 수 입력받기
    d=[0]*(x+1) # 1-based
    for i in range(2,x+1): # 2부터 x까지 반복
        d[i]=d[i-1]+1 # 1을 빼는 연산 -> 1회 진행
        if i%2==0: # 2로 나누어 떨어질 때, 2로 나누는 연산
            d[i]=min(d[i],d[i//2]+1)
        if i%3==0: # 3으로 나누어 떨어질 때, 3으로 나누는 연산
            d[i]=min(d[i],d[i//3]+1)
    print(d[x])
    
    # top-down
    x = int(input())
    array = [0] * (x+1) # 배열대신 dict을 이용해야 시간이 짧아진다. 선언하는데 시간 다보내는듯?
    def rec(x):
        '''
        n % 3 and n % 2, n % 2, n % 3, n - 1
        '''
        if x == 1:
            return 0
        elif x % 3 == 0 and x % 2 == 0:
            return min(rec(x//3)+1, rec(x//2)+1)
        elif x % 3 == 0:
            return min(rec(x//3)+1, rec(x-1)+1)
        elif x % 2 == 0:
            return min(rec(x//2)+1, rec(x-1)+1)
        else:
            return rec(x-1)+1
    print(rec(x))
    
        
mySolution() 