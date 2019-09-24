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
        self.adaptbility = 0

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
        self.len = cnt
        for i in range(0, cnt):
            src = int(random.uniform(0, cnt + 1))
            ind = Individual(tsp, src)
            self.pop.append(ind)

    # 将种群中所有ind的适应度进行归一化(映射为0到1的float)
    def get_adaptability(self):
        a = []
        min = 1.0 / self.pop[0].length
        max = min
        for ind in self.pop:
            tmp = 1.0 / ind.length
            a.append(tmp)
            if (tmp < min):
                min = tmp
            if (tmp > max):
                max = tmp
            ind.adaptability = tmp
        for ind in self.pop:
            ind.adaptability = (ind.adaptability - min) / (max - min)


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
    # n为选择出来的子集的规模
    # inds为被选择的父集
    # 类似水库抽样，先取inds中前n个ind。接下来的ind到达时，保留概率为其适应度。
    # 若保留，则随机选择子集中的一个ind，其被替换的概率为(1-其适应度)，
    # 若其不被替换则重新随机选择一个ind，直至新ind替换了原子集中的ind
    def fitness_proportional_selection(self, n, inds):
        child = []
        for i in range(n):
            child.append(inds[i])
        for i in range(n, self.len):
            if(random.uniform(0, 1) < inds[i].adaptability):
                flag = 0
                while(flag == 0):
                    tmp_pos = int(random.uniform(0, n))
                    if(random.uniform(0, 1) > child[tmp_pos].adaptability):
                        child[tmp_pos] = inds[i]
                        flag = 1

        return child

    # tournament 比赛选择，k个个体竞争产生下一代，优胜劣出！
    #          随机挑选k个竞争者，在交配池中竞争每一位基因遗传，适应性最好的将获得该基因的遗传权。
    def tournament_selection(self):
        return 0

    # elitism 精英主义选择，使当前一代中最好的生物体原封不动地传给下一代
    # elite_num 为精英数量
    # n为选择出来的子集的总规模(包括精英)
    # inds为被选择的父集
    def elitism_selection(self, elite_num, n, inds):
        elite = [] # 精英子集
        normal = [] # 普通子集
        selected_normal = [] # 从普通子集中选择出来的集

        # 选择出精英子集，可以改为用最大堆实现
        min_elite_adapt = inds[0].adaptability
        for i in range(n):
            # 先向elite中放入前elite_num个ind
            if (i < elite_num):
                elite.append(inds[i])
                if(inds[i].adaptability < min_elite_adapt):
                    # 记录elite中适应度的最小值
                    min_elite_adapt = inds[i].adaptability
            else:
                # 如果新ind的adaptability大于min_elite_adapt
                # 则用它替换elite中adaptability最小的那个ind
                # 然后更新min_elite_adapt
                if(inds[i].adaptability > min_elite_adapt):
                    tmp_min = 1
                    for j in range(elite_num):
                        if (elite[j].adaptability > min_elite_adapt
                                and elite[i].adaptability < tmp_min):
                            tmp_min = elite[i].adaptability
                        if(elite[j].adaptability == min_elite_adapt):
                            normal.append(elite[j])
                            elite[j] = inds[i]
                    min_elite_adapt = tmp_min
                else:
                    normal.append(inds[i])

        # 从normal集中选择
        selected_normal = self.fitness_proportional_selection(n - elite_num, normal)
        return elite.append(selected_normal)





p = Population(3)
for ind in p.pop:
    ind.getLength()
    ind.print_tour()
    tsp.plot(ind.tour)