#include <string>
#include <vector>

using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int lcm(int a, int b) {
    return a / gcd(a, b) * b;
}

int solution(vector<vector<int>> signals) {
    int limit = 1;

    for (int i = 0; i < signals.size(); i++) {
        int cycle = signals[i][0] + signals[i][1] + signals[i][2];
        limit = lcm(limit, cycle);
    }

    for (int time = 1; time <= limit; time++) {
        bool allYellow = true;

        for (int i = 0; i < signals.size(); i++) {
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
            return time;
        }
    }

    return -1;
}
