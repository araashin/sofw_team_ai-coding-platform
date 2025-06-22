import networkx as nx

def sample_graph() -> nx.Graph:
    G = nx.Graph()
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'),
                ('C', 'E'), ('E', 'F'), ('D', 'F')]
    G.add_edges_from(edges)
    return G

def create_tree_graph() -> nx.Graph:
    G = nx.Graph()
    edges = [('Root', 'A'), ('Root', 'B'), 
                ('A', 'C'), ('A', 'D'),
                ('B', 'E'), ('B', 'F'),
                ('C', 'G'), ('D', 'H')]
    G.add_edges_from(edges)
    return G

def create_linear_graph() -> nx.Graph:
    G = nx.Graph()
    nodes = ['1', '2', '3', '4', '5', '6']
    edges = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
    G.add_edges_from(edges)
    return G

def create_complete_graph(n: int = 4) -> nx.Graph:
    return nx.complete_graph(n)

def create_cycle_graph(n: int = 6) -> nx.Graph:
    return nx.cycle_graph(n)

def create_grid_graph(rows: int = 3, cols: int = 3) -> nx.Graph:
    return nx.grid_2d_graph(rows, cols)

def get_graph_by_type(graph_type: str) -> nx.Graph:
    graph_types = {
        'sample': sample_graph,
        'tree': create_tree_graph,
        'linear': create_linear_graph,
        'complete': lambda: create_complete_graph(5),
        'cycle': lambda: create_cycle_graph(6),
        'grid': lambda: create_grid_graph(3, 3)
    }
    if graph_type in graph_types:
        return graph_types[graph_type]()
    else:
        return sample_graph()

def get_graph_info(G: nx.Graph) -> dict:
    return {
        'nodes': len(G.nodes()),
        'edges': len(G.edges()),
        'is_connected': nx.is_connected(G),
        'is_tree': nx.is_tree(G),
        'has_cycles': not nx.is_tree(G) if nx.is_connected(G) else 'Unknown (disconnected)',
        'diameter': nx.diameter(G) if nx.is_connected(G) else 'Infinite (disconnected)',
        'average_clustering': nx.average_clustering(G)
    }
