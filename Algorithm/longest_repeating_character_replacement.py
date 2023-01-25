class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # count = {}   # count character in window hashmap
        # res = 0

        # l = 0
        # for r in range(len(s)):
        #     count[s[r]] = 1 + count.get(s[r], 0)
            
        #     # length of the window - most frequent char = no. of replacements to match with the most frequent character
        #     while (r - l + 1) - max(count.values()) > k:
        #         count[s[l]] -= 1   # decrement the count of element which will not be in the next window after shifting the left ptr
        #         l += 1
        #     res = max(res, r - l + 1)   # r-l+1 is the size of the window
        # return res


        # More optimization
        # count = {}   # count character in window hashmap
        # res = 0

        # l = 0
        # maxFreq = 0
        # for r in range(len(s)):
        #     count[s[r]] = 1 + count.get(s[r], 0)
        #     maxFreq = max(maxFreq, count[s[r]])

        #     while (r - l + 1) - maxFreq > k:
        #         count[s[l]] -= 1   # decrement the count of element which will not be in the next window after shifting the left ptr
        #         l += 1
        #     res = max(res, r - l + 1)   # r-l+1 is the size of the window
        # return res


        # OR BEST
        kori = k
        if len(s) == 0 or len(s) == 1:
            return len(s)
        i = max_count = 0
        counts = defaultdict(int)
        for char in s:
            counts[char] += 1
            if counts[char] > max_count:
                max_count = counts[char]
            else:
                k -= 1
            if k < 0:
                counts[s[i]] -= 1
                i += 1
                k += 1
        return max_count + kori - k