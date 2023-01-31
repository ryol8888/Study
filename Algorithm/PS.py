import sys

input = sys.stdin.readline

ps = {'(':')'}

def isRight(word):
    stack = []
    for char in word.strip():
        if char in ps: # (
            stack.append(char)
        else: # )
            if stack: # count ( > )
                stack.pop()
            else:
                return False
    if stack:
        return False
    else:
        return True

def solution():
    num = int(input())
    '''
    ( 이면 집어넣고
    ) 일 때 stack에 (가 있으면 pop 없으면 NO
    '''
    for _ in range(num):
        checkPS = isRight(input())
       
        if checkPS:
            print('YES')
        else:
            print('NO')
            
solution()

best answer

import sys
vps = sys.stdin.readlines()[1:]

for v in vps:
	v = v.rstrip()
	while '()' in v:
		v = v.replace('()', '')
	
	if v:
		print('NO')
	else:
		print('YES')