

def solution():
    num = int(input())
    
    # n 이라는 숫자를 1과 2로 채울건데 순서 상관있음(모양)
    
    # 방법의 수 -> dp로 푸는게 편하다.
    
    # n = 1 이면 1 한개
    # 2 면 1 놓고 n = 1인거 또는 2 놓는거
    # 3이면 1 놓고 2 놓던지 , 2놓고 1놓던지
    
    # top-down이 웬만해서 빠르다.
    # 재귀 시 dict 이용하면 편하다.
    # answer = {1:1, 2:2}
    # def rec(x):
    #     if x in answer:
    #         return answer[x]
    #     else:
    #         answer[x] = rec(x-2) + rec(x-1)
    #         return answer[x]
    # print(int(rec(num))%10007)
    
    # bottom-up
    array = [0] * (num+2)
    array[1] = 1
    array[2] = 2
    
    for idx in range(3, len(array)):
        array[idx] = array[idx-1] + array[idx-2]
    print(int(array[num])%10007)

solution()
    