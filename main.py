#graph = {0:[1, 4], 1: [2], 2: [3], 3: [1], 4: [3]}
#graph = {0:[], 1: [0], 2: [1]}
#graph = {1: [2], 2: [3], 3: [1], 4: [], 5: [4], 6: [4]}
#graph = {0:[7], 1: [9], 2: [9, 10], 3: [8], 4: [2], 5: [10, 3], 6: [0, 1], 7: [1, 6], 8: [5], 9: [4], 10: [8], 11: [2, 5, 9]}
#graph = {0: [1, 3], 1: [3], 2: [3, 4], 3: [4], 4: []}
#graph = {0:[1, 3], 1: [2], 2: [0], 3: [4], 4: [5], 5:[]}
import time

def read_file(filename): #функция чтения графа из файла
    with open(filename) as file:
        graph = {}
        lines = list(file.readlines())
        for i in lines[0].split():
            graph[i] = []
        for i in lines[1:]:
            graph[i.split()[0]].append(i.split()[1])
    return graph


def reverse_graph(graph): #функция транспонирования графа
    reversed_graph = {}
    for vertex in graph.keys(): #наивно разворачиваем все ребра из словаря
        for connected_vertex in graph[vertex]:
            if connected_vertex in reversed_graph.keys():
                reversed_graph[connected_vertex].append(vertex)
            else:
                reversed_graph[connected_vertex] = [vertex]
    for vertex in graph.keys(): #добавляем в транспонированный граф все вершины, для которых в изначальном графе были только исходящие ребра (они были пропущены предыдущим циклом)
        if vertex not in reversed_graph.keys():
            reversed_graph[vertex] = []
    return reversed_graph

def primary_dfs(graph, vertex, visited, order, counter): #первичный обход в глубину для алгоритма Косарайю
    visited.append(vertex) #помечаем вершину как посещенную
    for i in graph[vertex]: #смотрим на всех ее соседей
        if i not in visited: #если сосед еще не посещен, рекурсивно запускаем dfs от него с увеличенным счетчиком шагов
            counter = primary_dfs(graph, i, visited, order, counter + 1)
    order[vertex] = counter #сохраняем ход выхода из вершины
    return counter + 1 #возвращаем счетчик ходов + 1 родительской вершине

def secondary_dfs(graph, vertex, primary_order, visited): #вторичный dfs для косарайю
    visited.append(vertex)
    tree = {vertex: []}
    for i in sorted(graph[vertex], key=lambda x: primary_order[x], reverse=True): #для вторичного dfs выбираем вершины в порядке убывания хода выхода
        if i not in visited:
            subtree = secondary_dfs(graph, i, primary_order, visited) #получаем поддерево вершины-соседа
            for j in subtree.keys(): #добавляем поддерево вершины-соседа в поддерево данной вершины
                if j in tree.keys():
                    tree[j].extend(subtree[j])
                else:
                    tree[j] = subtree[j]
            tree[vertex].append(i)
            
    return tree #возвращаем поддерево этой вершины


def kosaraju(graph): #функция запуска алгоритма Косарайю
    start_time = time.perf_counter()
    primary_order = {} #словарь для хранения порядка выхода из вершины на первом проходе dfs
    for vertex in graph.keys(): #запуск первичного dfs
        if vertex not in primary_order.keys():
            primary_dfs(graph, vertex, [], primary_order, 1)
    reversed_graph = reverse_graph(graph) #транспонирование графа
    visited = []
    trees = []
    for vertex in sorted(reversed_graph.keys(), key=lambda x: primary_order[x], reverse=True): #запуск вторичного dfs
        if vertex not in visited:
            trees.append(list(secondary_dfs(reversed_graph, vertex, primary_order, visited).keys()))
    return trees, time.perf_counter() - start_time #возвращаем список компонент связности вместе с временем выполнения алгоритма

def tarjan_dfs(vertex, graph, time, small_time, stack, visited, sccs, counter): #вариация dfs для алгоритма Тарьяна
    time[vertex] = counter #сохраняем время входа в вершину
    small_time[vertex] = counter 
    stack.append(vertex) #добавляем вершину в стек
    visited.append(vertex)
    for child in graph[vertex]: #рекурсивно запускаем dfs, увеличивая счетчик времени
        if child not in visited:
            counter = tarjan_dfs(child, graph, time, small_time, stack, visited, sccs, counter + 1)
    
    small_time[vertex] = min([small_time[i] if i in visited and i in stack else len(graph.keys()) for i in graph[vertex] + [vertex]]) #обновляем small_time
    if time[vertex] == small_time[vertex]: #проверка на то, что данная вершина - корень КСС
        scc = []
        current = stack[-1] #если проверка успешна, то снимаем со стека все вершины, лежащие выше данной, а так же ее саму
        scc.append(stack.pop()) 
        while current != vertex:
            current = stack[-1]
            scc.append(stack.pop())
        sccs.append(scc) #снятые вершины образуют КСС
    return counter #независимо от проверки возвращаем счетчик
        
 
def tarjan(graph): #функция запуска алгоритма Тарьяна
    start_time = time.perf_counter()
    stack  = []
    big_time = {}
    small_time = {}
    visited = []
    counter = 0
    sccs = []

    for vertex in graph.keys(): #запуск модифицированного dfs
        if vertex not in visited:
            counter = tarjan_dfs(vertex, graph, big_time, small_time, stack, visited, sccs, counter + 1)

    return sccs, time.perf_counter() - start_time #возвращаем список КСС, а так же время выполнения
    