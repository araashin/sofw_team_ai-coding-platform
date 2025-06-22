import networkx as nx
import json

def parse_graph_from_adj_list(adj_list):
    G = nx.Graph()
    for idx, neighbors in enumerate(adj_list):
        for neighbor in neighbors:
            G.add_edge(idx, neighbor)
    return G

def parse_graph_from_edge_list(edge_list):
    G = nx.Graph()
    for u, v in edge_list:
        G.add_edge(u, v)
    return G

def parse_tree_from_list(tree_list):
    G = nx.DiGraph()
    n = len(tree_list)
    for i, val in enumerate(tree_list):
        if val is None:
            continue
        G.add_node(i, val=val)
        left = 2*i+1
        right = 2*i+2
        if left < n and tree_list[left] is not None:
            G.add_edge(i, left)
        if right < n and tree_list[right] is not None:
            G.add_edge(i, right)
    return G

def parse_list_from_str(data_str):
    try:
        data_str = data_str.replace('null', 'None')
        return eval(data_str)
    except Exception:
        return json.loads(data_str.lower().replace('null', 'null'))
