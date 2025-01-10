import argparse
import sys
from main import read_file, kosaraju, tarjan

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Добро пожаловать в программу по поиску Компенент Сильной Связности (КСС) \
                                     при помощи алгоритмов Косарайю и Тарьяна!")
    parser.add_argument("filename", help="Абсолютный путь к файлу")
    parser.add_argument("-k", "--kosaraju", help="Использовать алгоритм Косарайю", action='store_true')
    parser.add_argument("-t", "--tarjan", help="Использовать алгоритм Тарьяна", action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    graph = read_file(namespace.filename)
    if namespace.tarjan:
        print('Поиск Компонент Сильной Связности (КСС) при помощи алгоритма Тарьяна')
        answer, answer_time = tarjan(graph)
    else:
        print('Поиск Компонент Сильной Связности (КСС) при помощи алгоритма Косарайю')
        answer, answer_time = kosaraju(graph)
    print('Список компонент связности:', answer)
    print(f'Количество вершин в графе: {len(graph.keys())}, количество ребер: {sum([len(i) for i in graph.values()])}')
    print(f'Время выполнения алгоритма: {answer_time} мс.')
    input('Для выхода нажмите Enter')

    # if namespace.kosaraju or not any((namespace.kosaraju, namespace.tarjan)):
    #     print(kosaraju(graph))
    # elif namespace.tarjan:
    #     print(tarjan(graph))