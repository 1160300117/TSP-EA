import re
import random
import numpy as np
import TSP

fileaddr = "data/st70.tsp"
tsp = TSP.TSPlib(fileaddr)
cnt = tsp.DIMENSION

class Individual:
    
    def __init__(self, tsp, src):
        self.tour = []
        # 确定起点随机构造路径
        self.tour.append(src)
        while len(self.tour) != cnt:
            next = int(random.uniform(0, cnt + 1))
            if next not in self.tour and next != src:
                self.tour.append(next)
        self.tour.append(src)

    def print_tour(self):
        print("tour")
        print(self.tour)

# ind = Individual(tsp, 1)
# ind.print_tour()

class Population:
    # cnt 为种群中个体的个数
    def __init__(self, cnt):
        self.pop = []
        for i in range(0, cnt):
            src = int(random.uniform(0, cnt + 1))
            ind = Individual(tsp, src)
            self.pop.append(ind.tour)

p = Population(10)
print(p.pop)
