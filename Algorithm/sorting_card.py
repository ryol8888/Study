import sys

input = sys.stdin.readline

def solution():
    lines = int(input())
    '''
    i = 0
    answer = 10 + 20
    i = 1
    answer = (10 + 20) + 30
    i = n
    answer = answer + cards[i+1]
    '''
    cards = []
    for _ in range(lines):
        num = int(input())
        cards.append(num)
    cards.sort()
    
    if len(cards) <=2:
        print(sum(cards))
    else:
        count = cards[0] + cards[1]
        for idx in range(1, len(cards)-1):
            count += (count + cards[idx+1])
        print(count)
solution()