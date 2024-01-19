#!/bin/python3
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

''',20,30,40,50,60,70'''
V = [1,2,3,4,5,6,7,8,9,10]
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
    (7,10) 
]
''',
    (60,20),
    (30,70),
    (20,30),
    (60,70),
    (50,60),
    (40,50),
    (40,70)
'''


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

neighbors = get_neighbors(G)

def check_isolated_paths(deficit): #checks any isolated valid path combinations

    for v in V:
        if len(neighbors[v]) == 1:
            path = [v]
            curr = neighbors[v][0]
            while len(neighbors[curr]) == 2:
                path.append(curr)
                curr = neighbors[curr][0]    
            if len(neighbors[curr])  == 1:
                if(len(path))==1: #if we find an isolated edge
                    deficit.add(v)
                    deficit.add(curr)
                if(len(path)<4): #if we find an isolated path of max 4 elements
                    print("path:"+str(path),"v:"+str(v))
                    for i in range(1,len(path)):
                        deficit.add(path[i])

def check_paths(deficit):
    for v in V:
        if len(neighbors[v]) <= 2: 
            for u in neighbors[v]:
                if len(neighbors[u]) == 2:
                    deficit.add(u)
                 
# square: uvwx
def check_square(deficit):

    visited = set() #set of visited nodes to avoid visiting them again
    
    for v in V:
        if len(neighbors[v]) >= 2 and v not in visited: #if we have found the first candidate vertix of the square
            path = [v]
            prev = v #we keep track of the last visited node (default: the first one)
            curr = neighbors[v][0]
            c = 0
            while len(neighbors[curr]) == 2 and c < 2: #while we find next neighbors of degree 2 (max: 2 iterations)
                path.append(curr)
                next_vertex = neighbors[curr][0] if neighbors[curr][1] == prev else neighbors[curr][1]
                prev = curr
                curr = next_vertex
                c = c+1

            if len(neighbors[curr]) >= 2 and v in neighbors[curr] and len(path)==3: #if the last vertix closed the square
                path.append(curr)
                if all(len(neighbors[p]) == 2 for p in path):
                    deficit.add(path[0])
                    deficit.add(path[2])           
                elif any(len(neighbors[p]) > 2 for p in path):
                    deficit.add(path[1])
                    
                for p in path:
                    visited.add(p)

def check_component(deficit):
    for v in V:
        y = None #candidate variable for the node that will be put in deficit
        for n in neighbors[v]:
            if len(neighbors[n])>2:
                y = None
                break
            if len(neighbors[n])==2:
                if y==None:
                    y = n #we have found a neighbor that has degree 2
                else: 
                    y = None #cleaning y because we have found more than a 2 degree neighbor
                    break #if there is more than a 2 degree neighbor, v doesn't fit
        if y != None:
            deficit.add(y)

def check_isolated_component(deficit):
    for u in V:
        if len(neighbors[u]) == 1:
            v = neighbors[u][0]
            if len(neighbors[v]) != 1 and all(len(neighbors[w]) == 1 for w in neighbors[v]):
                deficit.add(v)


def main():
    deficit = set()
    neighbors = get_neighbors(G)
    check_isolated_paths(deficit) #cases 1,2 and 3
    check_paths(deficit) #case 4
    check_isolated_component(deficit) #case 5
    check_square(deficit) #cases 6,7 and 8
    check_component(deficit) #case 9

    print("deficit presenti nel grafo: " + str(deficit))

    m = len(deficit) // 2
    non_adjacent_vertices = []
    deficit = list(deficit)
    for _ in range(m):
        v = deficit[0]
        for u in deficit:
            if u == v:
                continue
            if u not in neighbors[v]:
                non_adjacent_vertices.append((v,u))
                deficit.remove(v)
                deficit.remove(u)
                break
                    


    if len(deficit) % 2 == 1:
        for v in V:
            if v not in deficit and len(neighbors[v]) >= 2:
                non_adjacent_vertices.append((v, deficit[0]))
                break
    
    for edge in non_adjacent_vertices:
        E.append(edge)
    
    print("i vertici non adiacenti sono: " + str(non_adjacent_vertices))

    print("(2,1)-anonimizzato? " + str(check(G, 2,1)))



if __name__ == "__main__":
    main()
