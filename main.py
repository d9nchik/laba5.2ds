import copy


def get_data():
    e_data = []
    with open("input.txt") as iFile:
        while True:
            line = iFile.readline()
            if not line:
                break
            temp = list(map(int, (line[:len(line)] + line[len(line) + 1:]).split()))
            e_data.append(temp)
            print(line, end='')
        print()
    return e_data


def create_adjacency_matrix(e_data):
    matrix = [0] * e_data[0][0]
    for x in range(e_data[0][0]):
        matrix[x] = [float('inf')] * e_data[0][0]
    for y in range(1, len(e_data)):
        matrix[e_data[y][0] - 1][e_data[y][1] - 1] = e_data[y][2]
    return matrix


def belman_ford_algorithm(adjancency_matrix, start_point):
    a = [0] * len(adjancency_matrix)
    matrix_of_history = [float('inf')] * len(adjancency_matrix)
    matrix_of_history[startPoint] = -1
    a[0] = [float('inf')] * len(adjancency_matrix)
    a[0][start_point] = 0
    for i in range(1, len(adjancency_matrix)):
        a[i] = copy.deepcopy(a[i - 1])
        for u in range(len(adjancency_matrix)):
            for v in range(len(adjancency_matrix)):
                if a[i][v] > a[i - 1][u] + adjancency_matrix[u][v]:
                    a[i][v] = a[i - 1][u] + adjancency_matrix[u][v]
                    matrix_of_history[v]=u
        if a[i] == a[i - 1]:
            return matrix_of_history
    for u in range(len(adjancency_matrix)):
        for v in range(len(adjancency_matrix)):
            if a[-1][v] > a[-1][u] + adjancency_matrix[u][v]:
                print("Граф містить негативні цикли!")
                exit(0)
    return matrix_of_history


def show_belman_path(belman_data, finish_point):
    if belman_data[finish_point] != -1 and belman_data[finish_point] != float('inf'):
        show_belman_path(belman_data, belman_data[finish_point])
    print(finish_point+1, end="->")


startPoint = int(input("Введіть початкову вершину: "))
finishPoint = int(input("Введіть кінцеву точку: "))
show_belman_path(belman_ford_algorithm(create_adjacency_matrix(get_data()), startPoint - 1), finishPoint - 1)
