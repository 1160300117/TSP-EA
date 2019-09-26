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

# 根据值找到对应下标
def find_index(parent, city):
    for i in range(0, len(parent)):
        if city == parent[i]:
            return i

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

    # order crossover 顺序交叉
    # 每次交叉选择一个基准parent，然后把另一个parent的不重复基因往child中填充
    def order_crossover(self, parent1, parent2):
        child1 = parent1
        child2 = parent2
        cnt = len(parent1)

        # 随机在parent1中选择一段
        start = int(random.uniform(0, cnt / 2))
        end = start + int(cnt / 2)
        gene1 = parent1[start:end]
        gene2 = []
        for city in parent2:
            if city not in gene1:
                gene2.append(city)
        # parent1中基因直接落下，余下位置插入parent2中的city
        child1[0:start] = gene2[0:start]
        child1[end:cnt] = gene2[start:len(gene2)]
        
        # 随机在parent2中选择一段
        start = int(random.uniform(0, cnt / 2))
        gene2 = parent2[start:end]
        gene1 = []
        for city in parent1:
            if city not in gene2:
                gene1.append(city)
        # parent2中基因直接落下，余下位置插入parent1中的city
        child2[0:start] = gene1[0:start]
        child2[end:cnt] = gene1[start:len(gene1)]
        
        return child1, child2

    # cycle crossover 循环交叉
    # 从parent1中循环复制一部分，再从parent2中循环复制一部分，以此类推
    # 奇数次循环标记的部分，parent1落到child1，parent2落到child2，反之同理
    def cycle_crossover(self, parent1, parent2):
        child1 = parent1
        child2 = parent2
        cnt = len(parent1)

        # 初始化标记为0, 奇数循环标1, 偶数循环标2
        mark = []
        for i in range(0, cnt):
            mark.append(0) 

        # 开始循环标记
        start = 0 # 每次循环的起点
        cycle = True # 控制奇偶循环 
        flag = True # 控制上下标记

        while 0 in mark:
            if cycle == True:
                # 奇数循环
                while mark[start] == 0:
                    mark[start] = 1
                    # 来回找下标
                    if flag == True:
                        next = find_index(parent2, parent1[start])
                    else:
                        next = find_index(parent1, parent2[start])
                    flag = not flag
                    start = next
            else:
                # 偶数循环
                while mark[start] == 0:
                    mark[start] = 2
                    # 来回找下标
                    if flag == True:
                        next = find_index(parent2, parent1[start])
                    else:
                        next = find_index(parent1, parent2[start])
                    flag = not flag
                    start = next
            cycle = not cycle
            for i in range(0, cnt):
                if mark[i] == 0:
                    start = i

        # 生成child1和child2    
        for m in mark:
            if m == 2:
                child1[m] = parent2[m]
                child2[m] = parent1[m]
        return child1, child2



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





p = Population(2)
# for ind in p.pop:
#     ind.getLength()
#     ind.print_tour()
#     tsp.plot(ind.tour)
print(p.cycle_crossover(p.pop[0].tour, p.pop[1].tour))