#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

// signals_rows는 2차원 배열 signals의 행 길이, signals_cols는 2차원 배열 signals의 열 길이입니다.
int solution(vector<vector<int>> signals) {
    int answer = -1;

    for (int time = 1; time <= 1000000; time++) {
        bool allYellow = true;

        for (int i = 0; i < signals_rows(); i++) {
            int G = signals[i][0];
            int Y = signals[i][1];
            int R = signals[i][2];

            int cycle = G + Y + R;

            int now = (time - 1) % cycle + 1;

            if (!(G < now && now <= G + Y)) {
                allYellow = false;
                break;
            }
        }

        if (allYellow) {
            answer = time;
            break;
        }
    }

    return answer;
}