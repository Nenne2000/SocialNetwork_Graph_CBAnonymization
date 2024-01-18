#!/bin/python3

from collections import deque
from collections import defaultdict


def check(G, k, l):
    V, E = G

    neighbors = {
        v: set() for v in V
    }

    for (u, v) in E:
        neighbors[v].add(u)
        neighbors[u].add(v)

    for v in V:
        counts = 0
        for w in V:
            if w == v:
                continue
            common_neighbors = len(neighbors[v].intersection(neighbors[w]))
            if common_neighbors >= l:
                counts += 1

        if counts < k:
            return False

    return True


V = [1,2,3,4,5,6,7,8,9,10,20,30,40,50]
E = [ 
    (1,2),
    (1,3),
    (2,3),
    (3,4),
    (4,6),
    (6,7),
    (5,7),
    (9,7),
    (8,7),
    (7,10),
    (20,30),
    (30,40),
    (40,50),
    (50,20),
    (40,10)
]

G = (V, E)

def get_neighbors(G):
    V, E = G
    graph = defaultdict(list)
    for u, v in E:
        graph[u].append(v)
        graph[v].append(u)

    res = {}
    for node in V:
        res[node] = graph[node]
    return res

def get_neighbors_vecchia(G, k):
    G = (V, E)
    graph = defaultdict(list)
    for u, v in E:
        graph[u].append(v)
        graph[v].append(u)

    res = {}
    for node in V:
        visited = set()
        queue = [(node, 0)]
        reachable = []
        while queue:
            curr, dist = queue.pop(0)
            if dist > k:
                break
            if curr not in visited:
                visited.add(curr)
                reachable.append(curr)
                for neighbor in graph[curr]:
                    queue.append((neighbor, dist + 1))
        reachable.remove(node)
        res[node] = reachable
    return res

def check_paths(G, deficit):
    V, E = G
    neighbors = get_neighbors(G)

    for v in V:
        if len(neighbors[v]) == 1:
            path = [v]
            curr = neighbors[v][0]
            while len(neighbors[curr]) == 2:
                path.append(curr)
                curr = neighbors[curr][0]    
            if len(neighbors[curr])  == 1:
                if(len(path))==1: #se abbiamo trovato un isolated edge
                    deficit.add(v)
                    deficit.add(curr)
                if(len(path)<4): #se abbiamo trovato un isolated path di max 4 elementi
                    print(path)
                    for i in range(1,len(path)):
                        deficit.add(path[i])
            elif len(path) == 2:
                deficit.add(curr)

# square: uvwx
def check_isolated_square(G, deficit):
    V, E = G
    neighbors = get_neighbors(G)
    visited = set()
    for v in V:
        print("v:"+str(v))
        if len(neighbors[v]) == 2 and v not in visited:
            path = [v]
            curr = neighbors[v][0]
            print("curr: "+ str(curr))
            c = 0
            while len(neighbors[curr]) == 2 and c < 2:
                path.append(curr)
                curr = neighbors[curr][1]
                print("vicino prossimo di curr: "+str(curr) + " - len dei vicini di curr: "+ str(len(neighbors[curr])))
                c = c+1
                print(c)
            print("len dei vicini di curr: "+str(len(neighbors[curr])))
            if len(neighbors[curr]) == 2 and v in neighbors[curr]:
                print("qualcosa è entrato! è "+str(v))
                deficit.add(path[0])
                deficit.add(path[2])
                path.append(curr)
                for p in path:
                    visited.add(p)


def check_square(G, deficit):
    V, E = G
    neighbors = get_neighbors(G)
    visited = set()
    for v in V:
        if len(neighbors[v]) >= 2 and v not in visited:
            path = [v]
            curr = neighbors[v][0]
            c = 0
            while len(neighbors[curr]) == 2 and c < 2:
                path.append(curr)
                curr = neighbors[curr][1]
                c = c+1
            if c != 2: #se non ci sono due nodi a grado 2 non c'è neanche un quadrato
                break
            if len(neighbors[curr]) >= 2 and v in neighbors[curr]:
                deficit.add(path[1])
                path.append(curr)
                for p in path:
                    visited.add(p)

""""
For a subgraph consisting of a square uvwx with edges (one or more)
uxi coming out of the square, we assign deficit 1 to v.
"""
#scrivi la funzione sopra indicata nel commento


            

def main():
    deficit = set()
    #neighbors = isolated_edges(G, deficit)
    neighbors = get_neighbors(G)
    print(neighbors)
    check_isolated_square(G, deficit)
    print(deficit)

if __name__ == "__main__":
    main()
