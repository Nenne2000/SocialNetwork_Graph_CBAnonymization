#!/bin/python3

def check(G, k, l):
    V, E = G

    neighbors = {
        v: set() for v in V
    }

    # for each edge (u,v) add them to the set of neighbors
    for (u, v) in E:
        neighbors[v].add(u)
        neighbors[u].add(v)

    #for v in V:
    #    print(f"N({v}) = ", neighbors[v])

    # check the definition of all the vertices in V
    for v in V:
        #print("CHECKING", v)
        counts = 0
        # count the number of vertices that shares at least l neighbors
        for w in V:
            if w == v: # skip if i'm checking the same node
                continue
            # count common neighbors between v, w

            common_neighbors = len(neighbors[v].intersection(neighbors[w]))
            #print("\t", f"COMMON NEIGHBOURS({v}, {w}) =", common_neighbors, "SET =", neighbors[v].intersection(neighbors[w]))
            if common_neighbors >= l:
                counts += 1
            # add 1 to counts if common neighbors >= l

        # graph is not (k,l)-anonymous
        # because for node v there are not at least k different
        # vertices with at least l common neighbors
        #print("\t", "COMMON NEIGHBOURS = ", counts)
        if counts < k:
            return False

    return True # pass all the checks


def checkStrongly(G, k, l):
    V, E = G

    neighbors = {v: set() for v in V}

    for (u, v) in E:
        neighbors[v].add(u)
        neighbors[u].add(v)

    # DEBUG
    '''
    for v in V:
        print(f"N({v}) = ", neighbors[v])
    '''
        
    for v in V:
        counts = 0
        for w in neighbors[v]:  # Iterate over neighbors of v

            common_neighbors = len(neighbors[v].intersection(neighbors[w]))
            
            if common_neighbors >= l:
                counts += 1

        if counts < k:
            # print("Vertice che fa fallire:", v) #DEBUG
            return False

    return True


V = [1,2,3,4,5,6,7,8,9,10]

E = [ 
    (1,2),
    (1,3),
    (2,3),
    (3,5),
    (4,7),
    (5,7),
    (5,8),
    (6,8),
    (7,8),
    (8,9),
    (8,10)
]

G = (V, E)

print(f"G is ({1},{1})-anonymous", check(G, 1, 1))
print(f"G is ({2},{1})-anonymous", check(G, 2, 1))
print(f"G is ({3},{1})-anonymous", check(G, 3, 1))
print(f"G is ({4},{1})-anonymous", check(G, 4, 1))
print(f"G is ({5},{1})-anonymous", check(G, 5, 1))
print(f"G is ({5},{1})-anonymous", check(G, 6, 1))

print(f"G is ({1},{1})-anonymous (strong)", checkStrongly(G, 1, 1))
print(f"G is ({2},{1})-anonymous (strong)", checkStrongly(G, 2, 1))
print(f"G is ({3},{1})-anonymous (strong)", checkStrongly(G, 3, 1))
print(f"G is ({4},{1})-anonymous (strong)", checkStrongly(G, 4, 1))
print(f"G is ({5},{1})-anonymous (strong)", checkStrongly(G, 5, 1))
print(f"G is ({5},{1})-anonymous (strong)", checkStrongly(G, 6, 1))

'''
if G is (k,l) anonymous then is also (1, l)-anonymoius, ..., (k-1, anonymous)
'''

V = [1,2,3,4,5,6,7] 
# (1,2,3,4,5) is a clique of N = 5 and x = 6 and y = 7
# u = 3


E = [
    (1,2),
    (1,3),
    (1,4),
    (1,5),
    (2,1),
    (2,3),
    (2,4),
    (2,5),
    (3,1),
    (3,2),
    (3,4),
    (3,5),
    (4,1),
    (4,2),
    (4,3),
    (4,5),
    (5,1),
    (5,2),
    (5,3),
    (5,4),
    (6,7), # x - y edge
    (3,6), # u - x edge
    (3,7) # u - y edge
    
]


G = (V, E)

# k = 5
print("")
print("")
print(f"G is ({1},{1})-anonymous", check(G, 1, 1))
print(f"G is ({2},{1})-anonymous", check(G, 2, 1))
print(f"G is ({3},{1})-anonymous", check(G, 3, 1))
print(f"G is ({4},{1})-anonymous", check(G, 4, 1))
print(f"G is ({5},{1})-anonymous", check(G, 5, 1))
print(f"G is ({6},{1})-anonymous", check(G, 6, 1))
print(f"G is ({7},{1})-anonymous", check(G, 7, 1))
print(f"G is ({1},{1})-anonymous(strongly)", checkStrongly(G, 1, 1))
print(f"G is ({2},{1})-anonymous(strongly)", checkStrongly(G, 2, 1))
print(f"G is ({3},{1})-anonymous(strongly)", checkStrongly(G, 3, 1))
print(f"G is ({4},{1})-anonymous(strongly)", checkStrongly(G, 4, 1))
print(f"G is ({5},{1})-anonymous(strongly)", checkStrongly(G, 5, 1))
print(f"G is ({6},{1})-anonymous(strongly)", checkStrongly(G, 6, 1))
print(f"G is ({7},{1})-anonymous(strongly)", checkStrongly(G, 7, 1))