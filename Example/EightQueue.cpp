#include <iostream>
using namespace std;

const int N = 12;

void putQueue(int queuePosition[], int level, int &posCount, int posMark[])
{
    if (level < 0 || level >= N)
        return;

    // 为第level层的皇后找一个可以放置的位置
    bool successFindPos = false;
    for (int i = 0; i < N; ++i)
        posMark[i] = 0;
    for (int i = 0; i < level; ++i)
    {
        int diff = level - i;
        int j = queuePosition[i];
        if (j >= 0 && j < N)
        {
            // 将不能放置的位置标记为1
            if (posMark[j] == 0)
                posMark[j] = 1;
            if (j >= diff && posMark[j - diff] == 0)
                posMark[j - diff] = 1;
            if (j + diff < N && posMark[j + diff] == 0)
                posMark[j + diff] = 1;
        }
    }
    for (int j = 0; j < N; ++j)
    {
        if (posMark[j] == 0 && queuePosition[level] < j)
        {
            queuePosition[level] = j;
            successFindPos = true;
            break;
        }
    }

    // 如果找到了位置则继续找下一层皇后的位置，否则回溯到上一层寻找下一个位置
    if (successFindPos)
    {
        if (level == N - 1)
        {
            for (int i = 0; i < N; ++i)
                cout << queuePosition[i] << " ";
            cout << endl;

            // 继续寻找下一种摆放位置
            putQueue(queuePosition, level, ++posCount, posMark);
        }
        else
            putQueue(queuePosition, level + 1, posCount, posMark);
    }
    else
    {
        for (int i = level; i < N; ++i)
            queuePosition[i] = -1;
        if (level > 0)
            putQueue(queuePosition, level - 1, posCount, posMark);
    }
}
int main()
{
    int queuePosition[N];
    for (int i = 0; i < N; ++i)
        queuePosition[i] = -1;
    int posCount = 0;
    int posMark[N] = {0};
    putQueue(queuePosition, 0, posCount, posMark);
    cout << posCount << endl;

    return 0;
}