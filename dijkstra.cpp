#include <iostream>
#include <queue>
#include <cstring>
#include <vector>
#define inf 200000
using namespace std;

vector<pair<int, int>> adj[200];
priority_queue<pair<int, int>> q;

void addadj(int a, int b, int w) {
    adj[a].push_back({b, w});
    adj[b].push_back({a, w});
}

void dijkstra(int N, int S){
    int distance[N];
    bool visited[N];
    memset(distance, inf, sizeof(distance) + 1);
    memset(visited, false, sizeof(visited) + 1);
    distance[S] = 0;
    q.push({0, S});
    while(!q.empty()){
        int a = q.top().second; q.pop();
        if(visited[a]) continue;
        visited[a] = true;
        for(auto x : adj[a]){
            int b = x.first, w = x.second;
            if(distance[a] + w < distance[b]){
                distance[b] = distance[a] + w;
                q.push({-distance[b], b});
            }
        } 
    }
    for(int i = 1; i <= N; i++){
        cout << distance[i] << endl;
        cout << i << endl;
    }
}

int main(){
    int N, E, S;
    scanf("%d %d %d", &N, &E, &S);
    int a, b, c;
    for(int i = 1; i <= E; i++){
        scanf("%d %d %d", &a, &b, &c);
        addadj(a, b, c);
    }
    for(auto i : adj[S]){
        cout << i.first << " " << i.second << endl;
    }
    dijkstra(N, S);
}