#include <bits/stdc++.h>
using namespace std;

vector<int> solution(int m, int n, int h, int w, vector<vector<int>> drops) {
    int INF = (int)drops.size() + 1;

    vector<vector<int>> rain(m, vector<int>(n, INF));

    for (int t = 0; t < drops.size(); t++) {
        int r = drops[t][0];
        int c = drops[t][1];
        rain[r][c] = t + 1;
    }

    vector<vector<int>> rowMin(m, vector<int>(n - w + 1));

    for (int r = 0; r < m; r++) {
        deque<int> dq;

        for (int c = 0; c < n; c++) {
            while (!dq.empty() && rain[r][dq.back()] > rain[r][c]) {
                dq.pop_back();
            }

            dq.push_back(c);

            if (dq.front() <= c - w) {
                dq.pop_front();
            }

            if (c >= w - 1) {
                rowMin[r][c - w + 1] = rain[r][dq.front()];
            }
        }
    }

    vector<vector<int>> areaMin(m - h + 1, vector<int>(n - w + 1));

    for (int c = 0; c < n - w + 1; c++) {
        deque<int> dq;

        for (int r = 0; r < m; r++) {
            while (!dq.empty() && rowMin[dq.back()][c] > rowMin[r][c]) {
                dq.pop_back();
            }

            dq.push_back(r);

            if (dq.front() <= r - h) {
                dq.pop_front();
            }

            if (r >= h - 1) {
                int top = r - h + 1;
                areaMin[top][c] = rowMin[dq.front()][c];
            }
        }
    }

    int best = -1;
    vector<int> answer = {0, 0};

    for (int r = 0; r < m - h + 1; r++) {
        for (int c = 0; c < n - w + 1; c++) {
            if (areaMin[r][c] > best) {
                best = areaMin[r][c];
                answer = {r, c};
            }
        }
    }

    return answer;
}