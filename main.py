#graph = {0:[1, 4], 1: [2], 2: [3], 3: [1], 4: [3]}
#graph = {0:[], 1: [0], 2: [1]}
#graph = {1: [2], 2: [3], 3: [1], 4: [], 5: [4], 6: [4]}
#graph = {0:[7], 1: [9], 2: [9, 10], 3: [8], 4: [2], 5: [10, 3], 6: [0, 1], 7: [1, 6], 8: [5], 9: [4], 10: [8], 11: [2, 5, 9]}
#graph = {0: [1, 3], 1: [3], 2: [3, 4], 3: [4], 4: []}
#graph = {0:[1, 3], 1: [2], 2: [0], 3: [4], 4: [5], 5:[]}

def read_file(filename):
    with open(filename) as file:
        graph = {}
        lines = list(file.readlines())
        for i in lines[0].split():
            graph[i] = []
        for i in lines[1:]:
            graph[i.split()[0]].append(i.split()[1])
    return graph


def reverse_graph(graph):
    reversed_graph = {}
    for vertex in graph.keys():
        for connected_vertex in graph[vertex]:
            if connected_vertex in reversed_graph.keys():
                reversed_graph[connected_vertex].append(vertex)
            else:
                reversed_graph[connected_vertex] = [vertex]
    for vertex in graph.keys():
        if vertex not in reversed_graph.keys():
            reversed_graph[vertex] = []
    return reversed_graph

def primary_dfs(graph, vertex, visited, order, counter):
    visited.append(vertex)
    for i in graph[vertex]:
        if i not in visited:
            counter = primary_dfs(graph, i, visited, order, counter + 1)
    order[vertex] = counter + 1
    return counter + 1

def secondary_dfs(graph, vertex, primary_order, visited):
    visited.append(vertex)
    tree = {vertex: []}
    for i in sorted(graph[vertex], key=lambda x: primary_order[x], reverse=True):
        if i not in visited:
            subtree = secondary_dfs(graph, i, primary_order, visited)
            for j in subtree.keys():
                if j in tree.keys():
                    tree[j].extend(subtree[j])
                else:
                    tree[j] = subtree[j]
            tree[vertex].append(i)
            
    return tree


def kosaraju(graph):
    primary_order = {}
    for vertex in graph.keys():
        if vertex not in primary_order.keys():
            primary_dfs(graph, vertex, [], primary_order, 0)
    reversed_graph = reverse_graph(graph)
    visited = []
    trees = []
    for vertex in sorted(reversed_graph.keys(), key=lambda x: primary_order[x], reverse=True):
        if vertex not in visited:
            trees.append(secondary_dfs(reversed_graph, vertex, primary_order, visited))
    return trees
