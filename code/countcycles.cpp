using namespace std;
#include <bitset>

const int N = 10;

// Предпологается, что входом является перестановка с числами от 0 до n-1
// Добавляет к i-1-ому элементу output количество циклов длины i в перестановке perm
void cycle_couner(int perm[N], int output[N]) {
    std::bitset<N> visited;
    int cnt;
    for (int i = 0; i < N; i++) {
        cnt = 0;
        if (!visited.test(i)) {
            do {
                visited.set(i);
                cnt++;
                i = perm[i];
            }
            while (!visited.test(i));
        }
        output[cnt - 1]++;
    }
}


int main()
{
    int count[N] = {0};

    return 0;
}
