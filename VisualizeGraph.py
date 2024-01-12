import networkx as nx
import matplotlib.pyplot as plt


def Visualize(G, class_reppresentation, size, type):
    """ 
    Funzione ausiliaria per la visualizzazione del grafo bipartito.
    """
    #riprendi i dati circa i nodi del grafo
    nodes_0 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 0]
    nodes_1 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 1]

    n = len(nodes_0)
    m = len(nodes_1)


    # Visualizza il grafo caricato. in alto voglio leggere il numero di ndodi di tipo 0 = n, il numero di nodi di tipo 1 = m e la size = size
    pos = nx.bipartite_layout(G, nodes_0)

    nx.draw(G, pos, with_labels=False, node_color=[G.nodes[node]["color"] for node in G.nodes()], verticalalignment="bottom")
    nx.draw_networkx_labels(G, pos, {node: G.nodes[node]["interaction"] for node in G.nodes() if G.nodes[node]["bipartite"] == 1}, font_size=10, font_color="black", verticalalignment="center")
    
    if(not class_reppresentation):
        nx.draw_networkx_labels(G, pos, {node: node for node in G.nodes() if G.nodes[node]["bipartite"] == 0}, font_size=10, font_color="black", verticalalignment="center")
    else:
        nx.draw_networkx_labels(G, pos, {node: G.nodes[node]["set"] for node in G.nodes() if G.nodes[node]["bipartite"] == 0}, font_size=10, font_color="black", verticalalignment="center")
    
    if (type == "uniform-lists"):
        title_text = "uniform lists approach → numero utenti = " + str(n) + ", numero interazioni = " + str(m) + ", size di ogni classe/lista = " + str(size)
    elif (type == "arbitrary-lists"):
        title_text = "arbitrary lists approach → numero utenti = " + str(n) + ", numero interazioni = " + str(m) + ", size di ogni lista = " + str(size)
    elif (type == "partitioning"):
        title_text = "partitioning approach → numero partizioni = " + str(n) + ", numero interazioni = " + str(m) + ", size di ogni partizione = " + str(size)
    else:
        title_text = "Original graph → numero utenti = " + str(n) + ", numero interazioni = " + str(m)
    
    print(title_text)
    plt.title(title_text)
    plt.show()