import re
import random
import numpy as np
import TSP

fileaddr = "data/st70.tsp"
tsp = TSP.TSPlib(fileaddr)
cnt = tsp.DIMENSION

class Individual:
    tour = []

    def __init__(self, tsp, src):
        self.tour.append(src)

        # 随机构造路径
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
    pop = []
    
    def __init__(self):
        # 目前跑多个解决方案还有点慢，只能先生成一个
        src = int(random.uniform(0, cnt + 1))
        ind = Individual(tsp, src)
        self.pop.append(ind.tour)

p = Population()
print(p.pop)