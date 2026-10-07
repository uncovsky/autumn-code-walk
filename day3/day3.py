from collections import deque

def build_graph(lines):
    def _add_edge(edges, u, v):
        if u not in edges:
            edges[u] = []
        edges[u].append(v)

    edges : dict[str, str] = {}
    for line in lines:
        u, v = line.split("--")
        u = u.strip()
        v = v.strip()
        _add_edge(edges, u, v)
        _add_edge(edges, v, u)

    return edges




def dfs(edges, flags, u, parent):
    flags[u] = 1
    for v in edges[u]:
        if parent is not None and v == parent:
            continue
        # back/cross edge is cycle in undirected
        if flags[v] > 0:
            return True

        if flags[v] == 0:
            if dfs(edges, flags, v, u):
                print(v)
                return True

    flags[u] = 2
    return False

def bfs(edges, start_vertex):
    visited = set()
    distances : dict[str, int] = {start_vertex : 0}
    queue = deque([start_vertex])

    while queue:
        vertex = queue.popleft()
        for neighbor in edges[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[vertex] + 1
                queue.append(neighbor)
    return vertex, distances[vertex]



with open('input.txt', 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    G = build_graph(lines)

    nodes = G.keys()
    flags = { k : 0 for k in nodes }


    # arbitrary node since sc, connected & acyclic -> tree
    print("does graph contain cycle?", dfs(G, flags, 'assh', None))

    # dirty trick, this is used to find center vertice(s) of tree when checking tree iso
    furthest_leaf, _ = bfs(G, 'assh')
    _, max_path_distance = bfs(G, furthest_leaf)
    print(max_path_distance)


