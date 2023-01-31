import sys

input = sys.stdin.readline

def solution():
    num = int(input())
    
    count = 0
    for _ in range(num):
        word = input()
        checker = {}
        last_char = ''
        isContinuous = True
        for char in word:
            if char in checker:
                if last_char != char:
                    isContinuous = False
                    break
            else:
                checker[char] = True
                last_char = char
        if isContinuous:
            count += 1        
    print(count)
solution()