class Solution:
    # recursion
    def fib(self, n: int) -> int:
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
    
    # def fib(self, n: int) -> int:
    #     if n==0:
    #         return 0
    #     if n==1:
    #         return 1
    #     n1=0
    #     n2=1
    #     for i in range(n-1):
    #         n2,n1=n2+n1,n2
    #     return n2