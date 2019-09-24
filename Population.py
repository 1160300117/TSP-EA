import re
import random
import numpy as np
import math
import TSP

fileaddr = "data/st70.tsp"
tsp = TSP.TSPlib(fileaddr)

class Individual:
    length = 0
    cnt = 0
    pos = []

    def __init__(self, tsp, src):
        self.cnt = tsp.DIMENSION
        self.pos = tsp.pos
        self.tour = []

        # 确定起点随机构造路径
        self.tour.append(src)
        while len(self.tour) != self.cnt:
            next = int(random.uniform(0, self.cnt + 1))
            if next not in self.tour and next != src:
                self.tour.append(next)
        self.tour.append(src)

    def getLength(self):
        for i in range(0, self.cnt - 1):
            curr = self.pos[self.tour[i] - 1]
            next = self.pos[self.tour[i + 1] - 1]
            x1 = curr[1]
            y1 = curr[2]
            x2 = next[1]
            y2 = next[2]
            self.length = self.length + math.sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )

    def print_tour(self):
        print("tour")
        print(self.tour)
        print("length")
        print(self.length)

class Population:
    # cnt 为种群中个体的个数
    def __init__(self, cnt):
        self.pop = []
        for i in range(0, cnt):
            src = int(random.uniform(0, cnt + 1))
            ind = Individual(tsp, src)
            self.pop.append(ind)

p = Population(3)
for ind in p.pop:
    ind.getLength()
    ind.print_tour()