

'''
영어 대문자로 이루어진 단어들을 각 대문자에 대항하는 숫자로 변환 후 최대합을 구하는 문제.
큰 숫자가 높은 자릿수로 가는게 이득. 
알파벳이 최대 10개이므로 0 ~ 9까지, 최대 길이 = 8

그리디 알고리즘으로 접근.
1. dictionary 자료형에 해당 알파벳 key 넣고 자릿수에 해당하는 weight값을 summation.
자릿수할당
 ex. dic['A'] = 10000, B = 1 -> N * len(word)
딕셔너리 정렬
dic.items().sort(key = lambda x: x[1]) -> 10 + NlogN
정렬된 list 돌면서 자릿수 할당 및 값 추가. -> N
최종 3N + NlogN

리뷰 : dict을 사용하는 것보다 26개의 알파벳 배열을 선언하여 진행하는 것이 time complexity가 더 낮다.
'''

import sys

input = sys.stdin.readline

def solution():
    ITER = int(input())
    digit_dict = dict()
    
    for _ in range(ITER):
        word = input().rstrip()
        for digit in range(len(word)-1, -1, -1): # digit = 1 ~ 10 ** len(word), weight = 
            if word[len(word)-digit-1] in digit_dict:
                digit_dict[word[len(word)-digit-1]] += 1 * (10 ** digit)
            else:
                digit_dict[word[len(word)-digit-1]] = 1 * (10 ** digit)
    digit_list_asc = sorted(digit_dict.items(),key = lambda x: x[1], reverse=True)
    max_sum = 0
    num = 9
    for (char, digit) in digit_list_asc:
        max_sum += digit*num
        num -= 1
    print(max_sum)
            
    
solution()