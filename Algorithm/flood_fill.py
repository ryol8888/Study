class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        m = len(image)
        n = len(image[0])
        value = image[sr][sc]
        if value == color:
            return image

        def dfs(r, c):
            if image[r][c] == value:
                image[r][c] = color
                if r>=1: dfs(r-1,c)
                if r+1<m: dfs(r+1,c)
                if c >= 1: dfs(r, c-1)
                if c+1 <n: dfs(r, c+1)
        dfs(sr, sc)
        return image