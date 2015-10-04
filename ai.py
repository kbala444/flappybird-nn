import numpy as np
import random

# values population is centered around
# old
#base = [-.31342821235, -0.1139874, -0.59353849, -0.4720327, -.398302309, 2.0122036125]
# goood
base = [-.5524816518, -0.251785039, -1.2697808633, -0.72796955875826, -0.81684247849, 3.97877468847]
#base = [-0.592793429, -0.3034340092, -1.16798685, -0.911873095, -.823201093414, 4.02614127]
#base = [-1.3250002, -0.7360805918, -2.405525383, -1.5978525241, -1.887704711098, 8.09533357862]
#base = [-.61469627, -0.2552426139, -1.1648285816, -0.92243556333, -0.71739226198, 3.9997260310595]
class Net():
    def __init__(self, w1=None, w2=None):
        self.insize = 2
        self.hidsize = 2
        self.outsize = 1
        self.w1 = w1
        self.w2 = w2
        if not w1:
            self.random()

    # produce output given input values
    def forward(self, X):
        # inputs to hidden layer
        hout = self.sigmoid(np.dot(X, self.w1))
        # final output
        fout = self.sigmoid(np.dot(hout, self.w2))
        return fout

    # generate random weights around base value
    def random(self):
        gene = []
        for weight in base:
            gene.append(weight + random.triangular(weight - .3, weight + .3))

        self.decode(gene)

    # create gene from weights
    def encode(self):
        gene = []
        for i in self.w1:
            gene.extend(i)
        for i in self.w2:
            gene.extend(i)

        return gene

    # set weights given gene
    def decode(self, gene):
        w1 = []
        count = 0
        for i in xrange(self.insize):
            n = [] 
            for j in xrange(self.hidsize):
                n.append(gene[count])
                count += 1
            w1.append(n)
        self.w1 = w1

        w2 = []
        for i in xrange(self.hidsize):
            n = [] 
            for j in xrange(self.outsize):
                n.append(gene[count])
                count += 1
            w2.append(n)

        self.w2 = w2

    def sigmoid(self, n):
        return 1/(1 + np.exp(-n))

    def __repr__(self):
        return str(self.encode())

    def __str__(self):
        return str(self.encode())

