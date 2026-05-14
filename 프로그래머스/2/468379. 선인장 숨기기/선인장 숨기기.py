from collections import deque

def solution(m, n, h, w, drops):
    INF = len(drops) + 1

    rain = [[INF] * n for _ in range(m)]

    for t, (r, c) in enumerate(drops, start=1):
        rain[r][c] = t

    row_min = [[0] * (n - w + 1) for _ in range(m)]

    for r in range(m):
        dq = deque()

        for c in range(n):
            while dq and rain[r][dq[-1]] > rain[r][c]:
                dq.pop()

            dq.append(c)

            if dq[0] <= c - w:
                dq.popleft()

            if c >= w - 1:
                row_min[r][c - w + 1] = rain[r][dq[0]]

    area_min = [[0] * (n - w + 1) for _ in range(m - h + 1)]

    for c in range(n - w + 1):
        dq = deque()

        for r in range(m):
            while dq and row_min[dq[-1]][c] > row_min[r][c]:
                dq.pop()

            dq.append(r)

            if dq[0] <= r - h:
                dq.popleft()

            if r >= h - 1:
                top = r - h + 1
                area_min[top][c] = row_min[dq[0]][c]

    best = -1
    answer = [0, 0]

    for r in range(m - h + 1):
        for c in range(n - w + 1):
            if area_min[r][c] > best:
                best = area_min[r][c]
                answer = [r, c]

    return answer