import math
import random
import operator
import numpy as np

class GA():
    def __init__(self, length,ranges,count):
        # 染色体长度
        self.length = length
        #因变量的范围
        self.ranges = ranges
        # 种群中的染色体数量
        self.count = count
        # 随机生成初始种群
        self.population = self.gen_population(length, count)

    def evolve(self, retain_rate=0.20, random_select_rate=0.5, mutation_rate=0.01):
        """
        进化
        对当前一代种群依次进行选择、交叉并生成新一代种群，然后对新一代种群进行变异
        """
        parents = self.selection(retain_rate, random_select_rate)
        self.crossover(parents)
        self.mutation(mutation_rate)

    def gen_chromosome(self, length):
        """
        随机生成长度为length的染色体，每个基因的取值是0或1
        这里用一个bit表示一个基因
        """
        chromosome = []
        c = 0
        #因变量的数量
        for i in range(3):
            for j in range(length[i]):
                c |= (1 << j) * random.randint(0, 1)
            chromosome.append(c)
        return chromosome

    def gen_population(self, length, count):
        """
        获取初始种群（一个含有count个长度为length的染色体的列表）
        """
        return [self.gen_chromosome(length) for i in range(count)]

    def fitness(self, chromosome):
        """
        计算适应度，将染色体解码为十进制数字，代入函数计算
        因为是求最大值，所以数值越大，适应度越高
        """
        x, y, z = self.decode(chromosome)
        return z/x/y

    def selection(self, retain_rate, random_select_rate):
        """
        选择
        先对适应度从大到小排序，选出存活的染色体
        再进行随机选择，选出适应度虽然小，但是幸存下来的个体
        """
        # 对适应度从大到小进行排序
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.population]
        
        graded1 = [x[1] for x in sorted(graded, reverse=True)]
        graded2 = [x[0] for x in sorted(graded, reverse=True)]
        print(self.decode(graded1[0]),graded2[0])
        # 选出适应性强的染色体
        retain_length = int(len(graded) * retain_rate)
        parents = graded1[:retain_length]
        # 选出适应性不强，但是幸存的染色体
        for chromosome in graded1[retain_length:]:
            if random.random() < random_select_rate:
                parents.append(chromosome)
        return parents

    def crossover(self, parents):
        """
        染色体的交叉、繁殖，生成新一代的种群
        """
        # 新出生的孩子，最终会被加入存活下来的父母之中，形成新一代的种群。
        children = []
        # 需要繁殖的孩子的量
        target_count = len(self.population) - len(parents)
        # 开始根据需要的量进行繁殖
        while len(children) < target_count:
            male = random.randint(0, len(parents)-1)
            female = random.randint(0, len(parents)-1)
            if male != female:
                # 随机选取交叉点
                cross_pos = [random.randint(0, x) for x in self.length]
                # 生成掩码，方便位操作
                mask = []
                mask0 = 0
                for i in range(len(cross_pos)):
                    for j in range(cross_pos[i]):
                        mask0 |= (1 << j)
                    mask.append(mask0)
                male = parents[male]
                female = parents[female]
                # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
                child = ((np.array(male) & np.array(mask)) | (np.array(female) & ~np.array(mask)))
                child = list(child)
                children.append(child)
        # 经过繁殖后，孩子和父母的数量与原始种群数量相等，在这里可以更新种群。
        self.population = parents + children

    def mutation(self, rate):
        """
        变异
        对种群中的所有个体，随机改变某个个体中的某个基因
        """
        for i in range(len(self.population)):
            if random.random() < rate:
                j = np.array([random.randint(0,x-1) for x in self.length])
                ar = np.array(self.population[i])
                ar ^= (1 << j)
                self.population[i] = list(ar)


    def decode(self, chromosome):
        """
        解码染色体，将二进制转化为十进制解
        """
        a = [x[0] for x in self.ranges]
        d = [x[1]-x[0] for x  in self.ranges]
        return np.array(chromosome) * np.array(d) / (2**np.array(self.length)-1) + np.array(a)
    
    def result(self):
        """
        获得当前代的最优值，这里取的是函数取最大值时x的值。
        """
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.population]
        graded1 = [x[1] for x in sorted(graded, reverse=True)]
        graded2 = [x[0] for x in sorted(graded, reverse=True)]
        return self.decode(graded1[0]),graded2[0]

if __name__ == '__main__':
    # 染色体长度，种群数量
    ga = GA([4,5,6], [(5,10),(25,30),(55,60)], 30)
    # 迭代次数
    for x in range(200):
        print('gengeration',x)
        ga.evolve()
