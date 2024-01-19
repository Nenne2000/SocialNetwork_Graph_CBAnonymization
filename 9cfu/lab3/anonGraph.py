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


V = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
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
    (10,11),
    (11,12),
    (11,13),
    (11,14),
    (14,15)
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
def check_square(G, deficit):
    V, E = G
    neighbors = get_neighbors(G)
    visited = set()
    for v in V:
        if len(neighbors[v]) >= 2 and v not in visited: #se abbiamo trovato un primo vertice candidato del quadrato  
            path = [v]
            prev = v #teniamo traccia dell'ultimo nodo visitato (default: il primo)
            curr = neighbors[v][0]
            c = 0
            while len(neighbors[curr]) == 2 and c < 2: #finchè troviamo prossimi vicini di grado 2 (max: 2 iterazioni)
                path.append(curr)
                next_vertex = neighbors[curr][0] if neighbors[curr][1] == prev else neighbors[curr][1]
                prev = curr
                curr = next_vertex
                c = c+1

            if len(neighbors[curr]) >= 2 and v in neighbors[curr] and len(path)==3: #se l'ultimo vertice chiude il quadrato
                path.append(curr)
                if all(len(neighbors[p]) == 2 for p in path):
                    print("v:"+str(v),"curr:"+str(curr))
                    deficit.add(path[0])
                    deficit.add(path[2])           
                elif any(len(neighbors[p]) > 2 for p in path):
                    print("v:"+str(v),"curr:"+str(curr))
                    deficit.add(path[1])
                    
                for p in path:
                    visited.add(p)


#for a subgraph consisting of a vertex u adjacent to vertices xi of degree 1 and to a vertex y of degree 2,
# assign deficit 1 to y.
def check_component(G, deficit):
    V, E = G
    neighbors = get_neighbors(G)
    for v in V:
        y = None #vicino da ipoteticamente aggiungere a deficit
        for n in neighbors[v]:
            if len(neighbors[n])>2:
                y = None
                break
            if len(neighbors[n])==2:
                if y==None:
                    y = n #abbiamo trovato un vicino che ha grado 2
                else: break #se c'è più di un vicino a grado 2, v non va bene
        if y != None:
            print(v)
            deficit.add(y)
            return



def isolated_component(G, deficit):
    V, E = G
    neighbors = get_neighbors(G)
    for u in V:
        if len(neighbors[u]) == 1:
            v = neighbors[u][0]
            if len(neighbors[v]) != 1 and all(len(neighbors[w]) == 1 for w in neighbors[v]):
                deficit.add(v)


def main():
    deficit = set()
    #neighbors = isolated_edges(G, deficit)
    neighbors = get_neighbors(G)
    print(neighbors)
    check_square(G, deficit)
    check_component(G,deficit)
    print(deficit)


if __name__ == "__main__":
    main()
