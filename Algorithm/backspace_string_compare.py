class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        stackS = []
        stackT = []
        for i in range(len(s)):
            if s[i] == "#":
                if stackS:
                    stackS.pop(-1)
            else:
                stackS.append(s[i])
        
        for i in range(len(t)):
            if t[i] == "#":
                if stackT:
                    stackT.pop(-1)
            else:
                stackT.append(t[i])

        if ''.join(stackS) == ''.join(stackT):
            print(''.join(stackS),''.join(stackT))
            return True

        else:
            print(''.join(stackS),''.join(stackT))
            return False