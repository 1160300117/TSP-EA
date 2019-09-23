import re
import numpy as np

fileaddr = "data/rl5915.tsp"

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
        # try:
        #     for line in file_obejct:
        #         print(line)
        # finally:
        #     file_obejct.close()
        self.NAME = re.split(r'NAME : |\n', file_obejct.readline())[1]
        self.COMMENT = re.split(r'COMMENT : |\n', file_obejct.readline())[1]
        self.TYPE = re.split(r'TYPE : |\n', file_obejct.readline())[1]
        self.DIMENSION = int(re.split(r'DIMENSION : |\n', file_obejct.readline())[1])
        self.EDGE_WEIGHT_TYPE = re.split(r'EDGE_WEIGHT_TYPE : |\n', file_obejct.readline())[1]
        file_obejct.readline()
        # print(name, comment, _type, dimension, edge_weight_type)

        self.pos = np.zeros((self.DIMENSION, 3))
        # print(pos)
        # line = file_obejct.readline()
        for i in range(self.DIMENSION):
            a = list(filter(None, re.split(r' |\n', file_obejct.readline())))
            self.pos[i][0] = float(a[0])
            self.pos[i][1] = float(a[1])
            self.pos[i][2] = float(a[2])
            # print(a)
        # print(self.pos)

    def print_pos(self):
        print("test")
        print(self.pos)

tsp = TSPlib(fileaddr)
tsp.print_pos()