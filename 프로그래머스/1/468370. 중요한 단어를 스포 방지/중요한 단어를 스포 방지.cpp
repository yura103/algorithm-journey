#include <string>
#include <vector>

using namespace std;

struct Word {
    string text;
    int start;
    int end;
};

bool overlap(int aStart, int aEnd, int bStart, int bEnd) {
    return aStart <= bEnd && bStart <= aEnd;
}

bool contains(vector<string> v, string target) {
    for (int i = 0; i < v.size(); i++) {
        if (v[i] == target) {
            return true;
        }
    }
    return false;
}

int solution(string message, vector<vector<int>> spoiler_ranges) {
    vector<Word> words;

    int n = message.length();
    int i = 0;

    while (i < n) {
        string word = "";
        int start = i;

        while (i < n && message[i] != ' ') {
            word += message[i];
            i++;
        }

        int end = i - 1;

        words.push_back({word, start, end});

        i++;
    }

    vector<string> normalWords;
    vector<string> openedWords;

    for (int i = 0; i < words.size(); i++) {
        bool isSpoiler = false;

        for (int j = 0; j < spoiler_ranges.size(); j++) {
            int s = spoiler_ranges[j][0];
            int e = spoiler_ranges[j][1];

            if (overlap(words[i].start, words[i].end, s, e)) {
                isSpoiler = true;
                break;
            }
        }

        if (!isSpoiler) {
            normalWords.push_back(words[i].text);
        }
    }

    int answer = 0;

    for (int i = 0; i < spoiler_ranges.size(); i++) {
        int s = spoiler_ranges[i][0];
        int e = spoiler_ranges[i][1];

        for (int j = 0; j < words.size(); j++) {
            if (overlap(words[j].start, words[j].end, s, e)) {
                string word = words[j].text;

                if (!contains(normalWords, word) &&
                    !contains(openedWords, word)) {
                    answer++;
                }

                openedWords.push_back(word);
            }
        }
    }

    return answer;
}