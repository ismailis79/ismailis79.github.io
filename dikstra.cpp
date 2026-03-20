/*
   Author: Steven Ismaili
   Date Created: 2025-04-03
   Class CSC 2710
   Path to file: ~/students/sismaili/dijkstra_lab6.cpp
   Compile with: g++ dijkstra_lab6.cpp -o dijkstra
   Execute with: ./dijkstra
   Description: Implements Dijkstra's algorithm based on textbook pseudocode.
   Outputs shortest distances and paths from Node 1 to all others,
   and tracks execution time in microseconds for two graph scenarios.
*/

#include <iostream>
#include <vector>
#include <limits>
#include <queue>
#include <stack>
#include <chrono>

using namespace std;

const int INF = numeric_limits<int>::max();

// Structure to represent a weighted edge to a node
struct Edge {
    int to;
    int weight;
};

// Dijkstra's algorithm based on textbook pseudocode
void dijkstra(int source, const vector<vector<Edge>>& graph, const string& townName) {
    int n = graph.size();
    vector<int> dist(n, INF);
    vector<int> prev(n, -1);
    vector<bool> visited(n, false);

    auto start = chrono::high_resolution_clock::now();

    dist[source] = 0;
    for (int i = 1; i < n; ++i) {
        int u = -1;
        for (int j = 1; j < n; ++j) {
            if (!visited[j] && (u == -1 || dist[j] < dist[u])) {
                u = j;
            }
        }

        if (dist[u] == INF) break;
        visited[u] = true;

        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            int w = edge.weight;
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                prev[v] = u;
            }
        }
    }   

    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(end - start);

    // Output
    cout << townName << "\n\n";
    cout << "Shortest path from Node 1:\n";
    for (int i = 2; i < n; ++i) {
        cout << "- To Node " << i << ": Distance = " << dist[i] << ", Path = ";
        stack<int> path;
        for (int at = i; at != -1; at = prev[at]) {
            path.push(at);
        }
        while (!path.empty()) {
                        cout << path.top();
            path.pop();
            if (!path.empty()) cout << " -> ";
        }
        cout << endl;
    }
    cout << "Total time taken: " << duration.count() << " microseconds\n\n";
}

int main() {
    // Nodes are indexed from 1 to 6, so size is 7 to include index 6
    vector<vector<Edge>> town1(7);
    town1[1].push_back({2, 2});
    town1[1].push_back({3, 4});
    town1[2].push_back({3, 1});
    town1[2].push_back({4, 7});
    town1[3].push_back({5, 3});
    town1[4].push_back({6, 1});
    town1[5].push_back({4, 1});
    town1[5].push_back({6, 5});

    vector<vector<Edge>> town2(7);
    town2[1].push_back({2, 4});
    town2[1].push_back({3, 20});
    town2[1].push_back({4, 6});
    town2[1].push_back({5, 15});
    town2[2].push_back({3, 12});
    town2[2].push_back({5, 8});
    town2[3].push_back({6, 1});
    town2[4].push_back({1, 15});
    town2[4].push_back({5, 9});
    town2[4].push_back({6, 22});
    town2[5].push_back({3, 7});
    town2[5].push_back({6, 6});

    dijkstra(1, town1, "Town One");
    dijkstra(1, town2, "Town Two");

    return 0;
}