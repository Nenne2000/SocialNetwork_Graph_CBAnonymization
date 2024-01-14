import pandas as pd
import networkx as nx
import argparse
import random
from VisualizeGraph import Visualize

def LoadGraph():
    """
    Carica il grafo da file CSV e lo restituisce.
    """

    # Carichiamo i dati dal csv
    nodes_df = pd.read_csv("csv/nodes_data.csv")
    edges_df = pd.read_csv("csv/edges_data.csv")

    G = nx.Graph()

    # Aggiungiamo i nodi e i loro attributi dal DataFrame dei nodi
    for _, data in nodes_df.iterrows():
        G.add_node(data["node"], **eval(data["attributes"]))

    # Aggiungiamo gli archi dal DataFrame degli archi
    for _, data in edges_df.iterrows():
        G.add_edge(data["node1"], data["node2"], **eval(data["attributes"]))

    return G

def sort(G,V):
    """
    Ordina i nodi di tipo 0 rispetto al valore dell'attributo year.
    perché in base al contesto poniamo che gli utenti di età simile 
    abbiano più probabilità di essere amici, avere blog condivisi e inviarsi messaggi
    """
    V.sort(key=lambda x: G.nodes[x]["year"], reverse=True)
    return V
 
def safety_condition(G, c, v):
    """
    Funzione che implementa la safety condition
    Verifica che il nodo v non abbia già interazioni con nodi della classe c
    """
    for node_in_class in c:
        # Verifica se hanno almeno un nodo in comune
        if set(G.neighbors(node_in_class)).intersection(set(G.neighbors(v))):
            return False
    return True

def arbitrary_lists_builder(G, arbitrary_lbl_list_size, nodes_0):
    """
    Funzione che implementa la creazione di label lists arbitrarie.
    Per ogni nodo v, crea una lista di nodi random che contenga v
    """
    V = nodes_0  # V è un rename per la lista degli utenti
    random_label_lists = []
    for v in V:
        list = []
        #inseriamo il nodo v nella lista, poiche deve esserci obbligatoriamente
        list.append(v)
        for i in range(arbitrary_lbl_list_size-1):
            #appendiamo un nodo random alla lista che sia diverso da quelli già presenti
            random_node = random.choice(V)
            while random_node in list:
                random_node = random.choice(V)
            random.shuffle(list)
            list.append(random_node)

        random_label_lists.append(list)

    #per ogni nodo assegnamo la corrispettiva classe
    for i, node in enumerate(nodes_0):
        G.nodes[node]["set"] = random_label_lists[i]

    return random_label_lists


def classBuilder(G, nodes_0, class_size):
    """
    Funzione che permette la creazione delle classi che corrisponderanno alle label lists
    Utilizza la safety condition per creare classi di utenti che non hanno interazioni tra loro
    """
    V = nodes_0  # V è un rename per la lista degli utenti
    classes = []

    sort(G,V)
    
    for v in V:
        flag = True
        #finché non troviamo una classe che rispetta la safety condition o che non ha raggiunto la size massima
        for c in classes:
            if safety_condition(G, c, v) and len(c) < class_size:
                c.append(v)
                flag = False
                break
        if flag:
            new_class = []
            new_class.append(v)
            classes.append(new_class)

    for node in nodes_0:
        for c in classes:
            if node in c:
                G.nodes[node]["set"] = c
    
    return classes
    

def partitioning(G, classes, nodes_1, n, m):
    """
    Funzione che implementa il partitioning approach, dove ogni classe creata precedentemente diventerà 
    un "ipernodo" di un nuovo grafo, che rimane bipartito
    Ogni nodo appartentente al precedente grafo permette di mantenere gli archi in cui è coinvolto
    """

    #n_class è il numero di classi che abbiamo creato
    n_class = len(classes)
    G_partitioned = nx.Graph()

    #aggiungo come nodi di tipo bipartite=0 gli array che corrispondono alle classi
    for i in range(n_class):
        G_partitioned.add_node("P"+str(i), bipartite=0)

    #ora da n_class ad m aggiungiamo le interactions, come nel caso precedente
    for i in range(n_class, n_class+m):
        corrispondent_node = nodes_1[i-n_class]
        G_partitioned.add_node(corrispondent_node, bipartite=1)
        
    nodes_0_partitioned = [node for node in G_partitioned.nodes() if G_partitioned.nodes[node]["bipartite"] == 0]
    nodes_1_partitioned = [node for node in G_partitioned.nodes() if G_partitioned.nodes[node]["bipartite"] == 1]

    for i, node in enumerate(nodes_0_partitioned):
        G_partitioned.nodes[node]["ID"] = node
        G_partitioned.nodes[node]["color"] = "green"
        G_partitioned.nodes[node]["set"] = classes[i]

    for i, node in enumerate(nodes_1_partitioned):
        G_partitioned.nodes[node]["ID"] = i+n
        G_partitioned.nodes[node]["interaction"] = G.nodes[i+n]["interaction"]
        G_partitioned.nodes[node]["color"] = "blue"

    for edge in G.edges():
        for node in nodes_0_partitioned:
            if edge[0] in G_partitioned.nodes[node]["set"]:
                G_partitioned.add_edge(node, edge[1])
    
    return G_partitioned

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--type", help=" 'uniform-lists' / 'partitioning' / 'arbitrary-lists' ")

    args = parser.parse_args()

    # Carica il grafo
    G = LoadGraph()

    # Divide nuovamente il grafo in due tipi
    nodes_0 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 0]
    nodes_1 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 1]
    n = len(nodes_0)
    m = len(nodes_1)
    
    if args.type == "partitioning" or args.type == "uniform-lists":
        class_size = int(input("size massima della classe < n → (" + str(n) + "): "))
        while class_size > n or class_size < 1:
            class_size = int(input("size massima della classe < n → (" + str(n) + "): "))
        classes = classBuilder(G, nodes_0, class_size)

        print("Classi:")    
        for c in classes:
            print(c)

        #visualizzazione del grafo bipartito originale
        Visualize(G,False, -1, "original") 
        
        if args.type == "partitioning":
            G_partitioned = partitioning(G, classes, nodes_1, n, m)
            Visualize(G_partitioned,False, class_size, args.type)
        else:
            Visualize(G,True, class_size, args.type)

    elif args.type == "arbitrary-lists":
        arbitrary_lbl_list_size = int(input("size delle label lists arbitrarie < n → (" + str(n) + "): "))
        while arbitrary_lbl_list_size > n or arbitrary_lbl_list_size < 1:
            arbitrary_lbl_list_size = int(input("size delle label lists arbitrarie < n → (" + str(n) + "): "))
        arbitrary_lists = arbitrary_lists_builder(G, arbitrary_lbl_list_size, nodes_0)
        print("label lists associate ad ogni nodo:")
        for c in arbitrary_lists:
            print(c)
        Visualize(G,False, -1, "original") 
        Visualize(G,True,arbitrary_lbl_list_size, args.type)
    else:
        print("choose: 'uniform-lists' / 'partitioning' / 'arbitrary-lists' ")

    

if __name__ == "__main__":
    main()

