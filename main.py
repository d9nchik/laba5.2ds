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
            # print(line, end='')
        # print()
    return e_data


def create_adjacency_matrix(e_data):
    matrix = [0] * e_data[0][0]
    for x in range(e_data[0][0]):
        matrix[x] = [float('inf')] * e_data[0][0]
    for y in range(1, len(e_data)):
        matrix[e_data[y][0] - 1][e_data[y][1] - 1] = e_data[y][2]
    return matrix


def belman_ford_algorithm(adjacency_matrix, start_point):
    a = [0] * len(adjacency_matrix)
    matrix_of_history = [float('inf')] * len(adjacency_matrix)
    matrix_of_history[start_point] = 0
    a[0] = [float('inf')] * len(adjacency_matrix)
    a[0][start_point] = 0
    for i in range(1, len(adjacency_matrix)):
        a[i] = copy.deepcopy(a[i - 1])
        for u in range(len(adjacency_matrix)):
            for v in range(len(adjacency_matrix)):
                if a[i][v] > a[i - 1][u] + adjacency_matrix[u][v]:
                    a[i][v] = a[i - 1][u] + adjacency_matrix[u][v]
                    matrix_of_history[v] = u
        if a[i] == a[i - 1]:
            return matrix_of_history, a[i]
    for u in range(len(adjacency_matrix)):
        for v in range(len(adjacency_matrix)):
            if a[-1][v] > a[-1][u] + adjacency_matrix[u][v]:
                print("Граф містить негативні цикли!")
                exit(0)
    return matrix_of_history, a[-1]


def show_belman_path(belman_data, finish_point):
    if belman_data[finish_point] != 0 and belman_data[finish_point] != float('inf'):
        show_belman_path(belman_data, belman_data[finish_point])
    print(finish_point + 1, end="->")


def show_belman_path_multiple(distance):
    for finish_point in range(len(distance)):
        print("До %d відстань %d" % (finish_point + 1, distance[finish_point]))


def create_adjacency_matrix_with_stroke(adjacency_matrix):
    adjacency_matrix_with_stroke = copy.deepcopy(adjacency_matrix)
    size = len(adjacency_matrix)
    for x in range(len(adjacency_matrix)):
        adjacency_matrix_with_stroke[x].append(float('inf'))
    adjacency_matrix_with_stroke.append([0] * (size + 1))
    return adjacency_matrix_with_stroke


def create_weight_matrix_stroke(matrix, distance):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] = matrix[i][j] + distance[i] - distance[j]
    return matrix


class Heights:
    def __init__(self, position, weight, father):
        self.position = position
        self.weight = weight
        self.father = father


def find_minimum_weight(unvisited):
    y = 0
    for x in range(len(unvisited)):
        if unvisited[y].weight > unvisited[x].weight:
            y = x
    return y


def close_height(adjacency_matrix, height):
    for x in range(len(adjacency_matrix)):
        adjacency_matrix[x][height] = float('inf')


def find_neighbours(matrix_of_unvisited, height):
    positions_of_neighbour = []
    for x in range(len(matrix_of_unvisited)):
        if matrix_of_unvisited[height][x] != float('inf'):
            positions_of_neighbour.append(x)
    return positions_of_neighbour


def position_in_array(unvisited, searched_position):
    for x in range(len(unvisited)):
        if unvisited[x].position == searched_position:
            return x
    return -1


def dijkstra_algorithm_multiple(adjacency_matrix, height):
    matrix_of_unvisited = copy.deepcopy(adjacency_matrix)
    visited = []
    unvisited = [Heights(height, 0, None)]
    while len(unvisited) > 0:
        position_of_minimum = find_minimum_weight(unvisited)
        visited.append(unvisited[position_of_minimum])
        dijkstra_algorithm_main_part(matrix_of_unvisited, position_of_minimum, unvisited, visited)
    return visited


def show_path_dijkstra_multiple(dijkstra_data, size):
    for x in range(size):
        path = [Heights(None, None, x)]
        show_path_dijkstra_main_part(dijkstra_data, path)


def show_path_dijkstra_main_part(dijkstra_data, path, total_weight=0):
    for y in range(len(dijkstra_data) - 1, 0, -1):
        if path[-1].father == dijkstra_data[y].position:
            path.append(dijkstra_data[y])
            total_weight += path[-1].weight
    if path[-1].father != 0:
        show_path_dijkstra_main_part(dijkstra_data, path, total_weight)
    if len(path) != 0:
        path.reverse()
        for z in range(0, len(path)):
            print(path[z].father + 1, end=" - > ")
        print("%s Шлях = %s" % (path[-1].position + 1, total_weight))


def dijkstra_algorithm_single(adjacency_matrix, height_start, height_finish):
    matrix_of_unvisited = copy.deepcopy(adjacency_matrix)
    visited = []
    unvisited = [Heights(height_start, 0, None)]
    while len(unvisited) > 0:
        position_of_minimum = find_minimum_weight(unvisited)
        visited.append(unvisited[position_of_minimum])
        if height_finish == visited[-1].position:
            break
        dijkstra_algorithm_main_part(matrix_of_unvisited, position_of_minimum, unvisited, visited)
    return visited


def dijkstra_algorithm_main_part(matrix_of_unvisited, position_of_minimum, unvisited, visited):
    close_height(matrix_of_unvisited, visited[-1].position)
    del unvisited[position_of_minimum]
    neighbours = find_neighbours(matrix_of_unvisited, visited[-1].position)
    for x in neighbours:
        position_of_neighbour = position_in_array(unvisited, x)
        if position_of_neighbour == -1:
            unvisited.append(
                Heights(x, matrix_of_unvisited[visited[-1].position][x] + visited[-1].weight, visited[-1].position))
        elif unvisited[position_of_neighbour].weight > matrix_of_unvisited[visited[-1].position][x] \
                + visited[-1].weight:
            unvisited[position_of_neighbour].weight = matrix_of_unvisited[visited[-1].position][
                                                          x] + visited[-1].weight
            unvisited[position_of_neighbour].father = visited[-1].position


def show_path_dijkstra_single(dijkstra_data):
    path = [dijkstra_data[-1]]
    show_path_dijkstra_main_part(dijkstra_data, path)


def de_stroke_weight_matrix(matrix, distance):
    for x in range(1, len(matrix)):
        matrix[x].weight = matrix[x].weight - distance[matrix[x].father] + distance[matrix[x].position]
    return matrix


choice = int(input("Працювати за алгоритмом Белмана-Форда(1) чи Джонсона(2): "))
if choice == 1:
    choice = int(input("Визначити найкоротший маршрут між двома точками(1) чи між усіма(2): "))
    if choice == 1:
        startPoint = int(input("Введіть початкову вершину: "))
        finishPoint = int(input("Введіть кінцеву точку: "))
        path, a = belman_ford_algorithm(create_adjacency_matrix(get_data()), startPoint - 1)
        show_belman_path(path, finishPoint - 1)
        print("Відстань: %s" % a[finishPoint - 1])
    elif choice == 2:
        startPoint = int(input("Введіть початкову вершину: "))
        points, a = belman_ford_algorithm(create_adjacency_matrix(get_data()), startPoint - 1)
        show_belman_path_multiple(a)
elif choice == 2:
    weight_matrix = create_adjacency_matrix(get_data())
    path, a = belman_ford_algorithm(create_adjacency_matrix_with_stroke(weight_matrix), -1)
    weight_matrix_stroke = create_weight_matrix_stroke(weight_matrix, a)
    choice = int(input("Визначити найкоротший маршрут між двома точками(1) чи від заданої вершини до всіх інших(2): "))
    if choice == 1:
        heightStart = int(input("Введіть вершину початку: ")) - 1
        heightFinish = int(input("Введіть вершину кінця: ")) - 1
        single = dijkstra_algorithm_single(weight_matrix_stroke, heightStart, heightFinish)
        de_stroke_weight_matrix(single, a)
        show_path_dijkstra_single(single)
