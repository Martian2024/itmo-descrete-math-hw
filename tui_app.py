import argparse
import sys
from main import read_file, kosaraju, tarjan

if __name__ == '__main__':
    graph = None
    print('''Добро пожаловать в программу по поиску Компонент Сильной Связности (КСС) при помощи алгоритма Косарайю и Тарьяна! Просим вас внимательно прочитать этот текст! 
1) Программа принимает граф в качестве txt-файла. Файл должен четко соответствовать формату: 1-я строка - названия вершин через пробел, 
   далее, каждый раз на новой строке, записываются две вершины одного ребра через пробел. 
2) Язык реализации программы (Python) накладывает некоторые ограничения на максимальный размер графа, поэтому с чрезмерно большими графами программа работать не сможет(((''')
    print()
    while graph == None:
        try:
            graph = read_file(input('Введите абсолютный путь к файлу с графом: '))
        except FileNotFoundError:
            print('Данный файл не найден!')
        except KeyError:
            print('Файл не соответствует необходимому формату!')

    prefered_algorithm = input('Введите предпочитаемый алгоритм: Косарайю[k], Тарьяна[t] или оба[b]: ')
    while prefered_algorithm not in ['b', 't', 'k']:
        print('Проверьте свой ввод!')
        prefered_algorithm = input('Введите предпочитаемый алгоритм: Косарайю[k], Тарьяна[t] или оба[b]: ')

    print(f'Количество вершин в графе: {len(graph.keys())}, количество ребер: {sum([len(i) for i in graph.values()])}')
    print()

    try:
        if prefered_algorithm == 'b':
            print('Поиск Компонент Сильной Связности (КСС) при помощи алгоритма Тарьяна')
            answer, answer_time = tarjan(graph)
            print('Список компонент связности:\n', '\n'.join([f'КСС-{i + 1}: ' + ', '.join(answer[i]) for i in range(len(answer))]))
            print(f'Время выполнения алгоритма: {answer_time} мс.')
            print()

            print('Поиск Компонент Сильной Связности (КСС) при помощи алгоритма Косарайю')
            answer, answer_time = kosaraju(graph)
            print('Список компонент связности:\n', '\n'.join([f'КСС-{i + 1}: ' + ', '.join(answer[i]) for i in range(len(answer))]))
            print(f'Время выполнения алгоритма: {answer_time} мс.')
            print()
        elif prefered_algorithm == 'k':
            print('Поиск Компонент Сильной Связности (КСС) при помощи алгоритма Косарайю')
            answer, answer_time = kosaraju(graph)
            print('Список компонент связности:\n', '\n'.join([f'КСС-{i + 1}: ' + ', '.join(answer[i]) for i in range(len(answer))]))
            print(f'Время выполнения алгоритма: {answer_time} мс.')
            print()
        elif prefered_algorithm == 't':
            print('Поиск Компонент Сильной Связности (КСС) при помощи алгоритма Тарьяна')
            answer, answer_time = tarjan(graph)
            print('Список компонент связности:\n', '\n'.join([f'КСС-{i + 1}: ' + ', '.join(answer[i]) for i in range(len(answer))]))
            print(f'Время выполнения алгоритма: {answer_time} мс.')
            print()
    except RecursionError:
        print('Граф слишком большой!')
    
    input('Для выхода нажмите Enter')