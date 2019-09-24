import re
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

fileaddr = "data/st70.tsp"

class TSPlib:
    # NAME : <string> Identifies the data file
    NAME = ""

    # TYPE : <string> Specifies the type of the data. Possible types are
    TYPE = "TSP"

    # COMMENT : <string> Additional comments
    COMMENT = ""

    # DIMENSION : <integer> the dimension is the number of its nodes.
    DIMENSION = 0

    # CAPACITY : <integer> Specifies the truck capacity in a CVRP.
    # CAPACITY = 0;

    # EDGE WEIGHT TYPE : <string> Specifies how the edge weights (or distances) are given.
    EDGE_WEIGHT_TYPE = "EUC_2D"

    # EDGE WEIGHT FORMAT : <string> Describes the format of the edge weights if they are given explicitly.
    # EDGE_WEIGHT_FORMAT = "EDGE_WEIGHT_FORMAT";

    # EDGE DATA FORMAT : <string> Describes the format in which the edges of a graph are given, if the graph is not complete.
    # EDGE_DATA_FORMAT = "EDGE_DATA_FORMAT";

    # NODE COORD TYPE : <string> Specifies whether coordinates are associated with each node
    # NODE_COORD_TYPE = "NODE_COORD_TYPE";

    # DISPLAY DATA TYPE : <string> Specifies how a graphical display of the nodes can be obtained.
    # DISPLAY_DATA_TYPE = "DISPLAY_DATA_TYPE";

    def __init__(self, file_address):
        file_obejct = open(file_address)

        self.NAME = re.split(r'NAME : |\n', file_obejct.readline())[1]
        self.COMMENT = re.split(r'COMMENT : |\n', file_obejct.readline())[1]
        self.TYPE = re.split(r'TYPE : |\n', file_obejct.readline())[1]
        self.DIMENSION = int(re.split(r'DIMENSION : |\n', file_obejct.readline())[1])
        self.EDGE_WEIGHT_TYPE = re.split(r'EDGE_WEIGHT_TYPE : |\n', file_obejct.readline())[1]

        file_obejct.readline()

        self.pos = np.zeros((self.DIMENSION, 3))

        for i in range(self.DIMENSION):
            a = list(filter(None, re.split(r' |\n', file_obejct.readline())))
            self.pos[i][0] = int(a[0])
            self.pos[i][1] = float(a[1])
            self.pos[i][2] = float(a[2])

    def print_pos(self):
        print("test")
        print(self.pos)

    def plot(self, route):
        # route为点序列，表示依次连接的点

        figure, ax = plt.subplots()
        # 标点
        for i in range(self.DIMENSION):
            x = self.pos[i][1]
            y = self.pos[i][2]
            ax.scatter(x, y, c='r', s=20, alpha=0.5)

        # 连线
        s = int(route[0])
        source_dot = [self.pos[s-1][1], self.pos[s-1][2]]

        for j in range(self.DIMENSION - 1):
            a = int(route[j + 1] - 1)
            target_dot = [self.pos[a][1], self.pos[a][2]]
            ax.add_line(Line2D([source_dot[0], target_dot[0]], [source_dot[1], target_dot[1]], linewidth=1, color='blue'))
            source_dot = target_dot

        plt.plot()
        plt.show()


    def get_opt_tour(self):
        opt_tour_path = 'opt_tour/pcb442.opt.tour'
        file_obejct = open(opt_tour_path)
        self.given_opt_tour = np.zeros(self.DIMENSION)
        for i in range(5):
            file_obejct.readline()

        for j in range(self.DIMENSION):
            self.given_opt_tour[j] = int(file_obejct.readline())


def get_simple_route(n):
    r = np.zeros(n)
    for i in range(n):
        r[i] = i + 1
    return r

# tsp = TSPlib(fileaddr)
# tsp.get_opt_tour()
# tsp.print_pos()
# tsp.plot(get_simple_route(tsp.DIMENSION))
# print(tsp.given_opt_tour)

