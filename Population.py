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
        self.adaptbility = 1 / self.length  # 个体的适应度，为路径长度的倒数，越大越好

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

    #***************************************************************************************
    # 交叉算法
    # http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/EdgeRecombinationCrossoverOperator.aspx

    # order crossover
    def order_crossover(self, parent1, parent2):
        child = parent1 # 这句要重写
        return child

    # PMX crossover
    def PMX_crossover(self, parent1, parent2):
        child = parent1  # 这句要重写
        return child

    # cycle crossover
    def cycle_crossover(self, parent1, parent2):
        child = parent1  # 这句要重写
        return child

    # edge recombination 边缘重组交叉
    def edge_recombination_crossover(self, parent1, parent2):
        child = parent1  # 这句要重写
        return child

    # ***************************************************************************************
    # 突变算法
    # https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_mutation.htm

    # insert 插入突变。【或许TSP不适合插入突变】
    def insert_mutation(self, ind):
        return 0

    # swap 交换突变，随机选择染色体上的两个位置，并交换值。
    def swap_mutation(self, ind):
        return 0

    # inversion 反转突变，选择基因的一个子集，并将其反转。
    def inversion_mutation(self, ind):
        return 0

    # scramble 加扰突变，从整个染色体中选择基因的一个子集，然后随机扰乱或乱序排列它们的值。
    def scramble_mutation(self, ind):
        return 0

    #***************************************************************************************
    # 选择算法

    # fitness_proportional 适应性比例选择,个体被选择的几率与适应度相关
    def fitness_proportional_selection(self):
        return 0

    # tournament 比赛选择，k个个体竞争产生下一代，优胜劣出！
    #          随机挑选k个竞争者，在交配池中竞争每一位基因遗传，适应性最好的将获得该基因的遗传权。
    def tournament_selection(self):
        return 0

    # elitism 精英主义选择，使当前一代中最好的生物体原封不动地传给下一代
    def elitism_selection(self):
        return 0



p = Population(3)
for ind in p.pop:
    ind.getLength()
    ind.print_tour()
    tsp.plot(ind.tour)