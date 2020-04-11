import copy
import random
import numpy as np
from evalutation import costWithDepot
import utils
import evalutation
from collections import Counter

class solution:
    def __init__(self, grandTour, p):
        self.costo = -1
        self.feas = True
        self.GT = grandTour
        self.penality = p.omega
        _, self.delimiters = split(grandTour, p, self.penality)      
        self.sigma = routing(self.GT, self.delimiters, p, self.penality) 
        self.nodeRoutes = ["depot"]
        self.sim = -1
        self.fitness = -1
        self.myarcs = np.zeros((p.n, p.n), dtype = bool)
        self.recomputenodes(p)
    def printsolution(self):
        print("Routes: ")
        for route in self.sigma:
            print(route.customer)
        print("Cost: ", self.costo)
    def printonfile(self, filename):
        myfile = open(filename, 'a')
        myfile.write("\nRoutes: ")
        for route in self.sigma:
            myfile.write("\n")
            myfile.write(utils.listToString(route.customer))
        myfile.write("\nCost: ")
        myfile.write(str(self.costo))
        myfile.close()
    def recomputeparameters(self, p):
        gt = []
        totalcost = 0
        self.feas = True
        for route in self.sigma:
            route.recomputecost(p, self.penality)
            totalcost += route.costo
            if not route.feas:
                self.feas = False
            for node in route.customer:
                if node != 0:
                    gt.append(node)
        self.GT = gt
        self.costo = totalcost
        if self.feas:
            _, self.delimiters = split(self.GT, p, self.penality)
            self.sigma = routing(self.GT, self.delimiters, p, self.penality)
        self.recomputenodes(p)
    def delimiting(self):                                                              
        self.delimiters = [0]
        start = 0
        for route in self.sigma:
            start += len(route.customer)
            self.delimiters.append(start)
    def recomputecost(self, p):
        tot = 0
        for route in self.sigma:
            tot += route.recomputecost(p, self.penality)
        self.costo = tot
    def recomputenodes(self, p):
        self.nodeRoutes = ["depot"]
        for node in range(1, p.n):
            for i, route in enumerate(self.sigma):
                for nodeS in route.customer:
                    if node == nodeS:
                        self.nodeRoutes.append(i)
    def recomputearcs(self, p):
        for route in self.sigma:
            for i in range(len(route.customer) - 1):
                if route.customer[i] < route.customer[i + 1]:
                    self.myarcs[route.customer[i]][route.customer[i + 1]] = 1
                else:
                    self.myarcs[route.customer[i + 1]][route.customer[i]] = 1
    
    def M1(self, p, c1, c1i, r1i, c2, c2i, r2i): # CROSS 1-0
                    
        # stessa route
        if r1i == r2i:
            if c1i == c2i + 1:
                return False
            if c1i < c2i:
                seq1 = [self.sigma[r1i].subseq[0][c1i-1]]
                seq2 = [self.sigma[r1i].subseq[c1i + 1][c2i]]
                seq3 = [self.sigma[r1i].subseq[c1i][c1i]]
                seq4 = [self.sigma[r1i].subseq[c2i + 1][-1]]
                seq = seq1 + seq2 + seq3 + seq4 
            else:
                seq1 = [self.sigma[r1i].subseq[0][c2i]]
                seq2 = [self.sigma[r1i].subseq[c1i][c1i]]
                seq3 = [self.sigma[r1i].subseq[c2i + 1][c1i - 1]]
                seq4 = [self.sigma[r1i].subseq[c1i + 1][-1]]
                seq = seq1 + seq2 + seq3 + seq4 
            newcost = evalN(p, seq, self.penality)
            if newcost < self.sigma[r1i].costo:
                self.sigma[r1i].costo = newcost
                self.sigma[r1i].customer.insert(c2i + 1, c1)
                if c1i < c2i:
                    del self.sigma[r1i].customer[c1i]
                else:
                    del self.sigma[r1i].customer[c1i + 1]
                self.sigma[r1i].update_data(p, self.penality, -1)
                return True
            return False
       
        # route diverse
        r1seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
        r1seq2 = [self.sigma[r1i].subseq[c1i + 1][-1]]
        r2seq1 = [self.sigma[r2i].subseq[0][c2i]]
        r2seq2 = [self.sigma[r1i].subseq[c1i][c1i]]
        r2seq3 = [self.sigma[r2i].subseq[c2i + 1][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2 + r2seq3, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            self.sigma[r2i].customer.insert(c2i + 1, c1)
            del self.sigma[r1i].customer[c1i]
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            self.nodeRoutes[c1] = r2i 
            return True
        return False
    
    
    def M2(self, p, c1, c1i, r1i, c2, c2i, r2i): # CROSS 2-0
        
        if c1i == len(self.sigma[r1i].customer) - 2:
            return False
        
        
        # sessa route   
        if r1i == r2i:
            if c1i == c2i + 1:
                return False
            if c2i == c1i + 1:
                return False
            if c1i < c2i:
                seq1 = [self.sigma[r1i].subseq[0][c1i-1]]
                seq2 = [self.sigma[r1i].subseq[c1i + 2][c2i]]
                seq3 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
                seq4 = [self.sigma[r1i].subseq[c2i + 1][-1]]
                seq = seq1 + seq2 + seq3 + seq4 
            else:
                seq1 = [self.sigma[r1i].subseq[0][c2i]]
                seq2 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
                seq3 = [self.sigma[r1i].subseq[c2i + 1][c1i - 1]]
                seq4 = [self.sigma[r1i].subseq[c1i + 2][-1]]
                seq = seq1 + seq2 + seq3 + seq4 
            newcost = evalN(p, seq, self.penality)
            if newcost < self.sigma[r1i].costo:
                self.sigma[r1i].costo = newcost
                successor = self.sigma[r1i].customer[c1i + 1]
                self.sigma[r1i].customer.insert(c2i + 1, c1)
                self.sigma[r1i].customer.insert(c2i + 2, successor)
                if c1i < c2i:
                    del self.sigma[r1i].customer[c1i]
                    del self.sigma[r1i].customer[c1i]
                else:
                    del self.sigma[r1i].customer[c1i + 2]
                    del self.sigma[r1i].customer[c1i + 2]
                self.sigma[r1i].update_data(p, self.penality, -1)
                return True
            return False
                     
        # route diverse
        r1seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
        r1seq2 = [self.sigma[r1i].subseq[c1i + 2][-1]]
        r2seq1 = [self.sigma[r2i].subseq[0][c2i]]
        r2seq2 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
        r2seq3 = [self.sigma[r2i].subseq[c2i + 1][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2 + r2seq3, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            successor = self.sigma[r1i].customer[c1i + 1]
            self.sigma[r2i].customer.insert(c2i + 1, c1)
            self.sigma[r2i].customer.insert(c2i + 2, successor)
            del self.sigma[r1i].customer[c1i]
            del self.sigma[r1i].customer[c1i]
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            self.nodeRoutes[c1] = r2i
            self.nodeRoutes[successor] = r2i
            return True
        return False
        
        
    def M3(self, p, c1, c1i, r1i, c2, c2i, r2i): # I-CROSS 2-0
        
        if c1i == len(self.sigma[r1i].customer) - 2:
            return False
        
        
        # sessa route   
        if r1i == r2i:
            if c1i == c2i + 1:
                return False
            if c2i == c1i + 1:
                return False
            if c1i < c2i:
                seq1 = [self.sigma[r1i].subseq[0][c1i-1]]
                seq2 = [self.sigma[r1i].subseq[c1i + 2][c2i]]
                seq3 = [self.sigma[r1i].subseq[c1i + 1][c1i]]
                seq4 = [self.sigma[r1i].subseq[c2i + 1][-1]]
                seq = seq1 + seq2 + seq3 + seq4 
            else:
                seq1 = [self.sigma[r1i].subseq[0][c2i]]
                seq2 = [self.sigma[r1i].subseq[c1i + 1][c1i]]
                seq3 = [self.sigma[r1i].subseq[c2i + 1][c1i - 1]]
                seq4 = [self.sigma[r1i].subseq[c1i + 2][-1]]
                seq = seq1 + seq2 + seq3 + seq4 
            newcost = evalN(p, seq, self.penality)
            if newcost < self.sigma[r1i].costo:
                self.sigma[r1i].costo = newcost
                successor = self.sigma[r1i].customer[c1i + 1]
                self.sigma[r1i].customer.insert(c2i + 1, successor)
                self.sigma[r1i].customer.insert(c2i + 2, c1)
                if c1i < c2i:
                    del self.sigma[r1i].customer[c1i]
                    del self.sigma[r1i].customer[c1i]
                else:
                    del self.sigma[r1i].customer[c1i + 2]
                    del self.sigma[r1i].customer[c1i + 2]
                self.sigma[r1i].update_data(p, self.penality, -1)
                return True
            return False
                     
        # route diverse
        r1seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
        r1seq2 = [self.sigma[r1i].subseq[c1i + 2][-1]]
        r2seq1 = [self.sigma[r2i].subseq[0][c2i]]
        r2seq2 = [self.sigma[r1i].subseq[c1i + 1][c1i]]
        r2seq3 = [self.sigma[r2i].subseq[c2i + 1][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2 + r2seq3, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            successor = self.sigma[r1i].customer[c1i + 1]
            self.sigma[r2i].customer.insert(c2i + 1, successor)
            self.sigma[r2i].customer.insert(c2i + 2, c1)
            del self.sigma[r1i].customer[c1i]
            del self.sigma[r1i].customer[c1i]
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            self.nodeRoutes[c1] = r2i
            self.nodeRoutes[successor] = r2i
            return True
        return False
    
    
    
    
    def M4(self, p, c1, c1i, r1i, c2, c2i, r2i): # CROSS 1-1
        
        if c2 == 0:
            return False
        
        # stessa route
        if r1i == r2i:
            reverse = False
            if c1i > c2i:
                tmp = c1i
                c1i = c2i
                c2i = tmp
                reverse = True
            seq1 = [self.sigma[r1i].subseq[0][c1i-1]]
            seq2 = [self.sigma[r1i].subseq[c2i][c2i]]
            if c1i + 1 != c2i:
                seq3 = [self.sigma[r1i].subseq[c1i + 1][c2i - 1]]
            else:
                seq3 = []
            seq4 = [self.sigma[r1i].subseq[c1i][c1i]]
            seq5 = [self.sigma[r1i].subseq[c2i + 1][-1]]
            newcost = evalN(p, seq1 + seq2 + seq3 + seq4 + seq5, self.penality)
            if newcost < self.sigma[r1i].costo:
                self.sigma[r1i].costo = newcost
                if not reverse:
                    self.sigma[r1i].customer[c1i] = c2
                    self.sigma[r1i].customer[c2i] = c1
                else:
                    self.sigma[r1i].customer[c1i] = c1
                    self.sigma[r1i].customer[c2i] = c2
                self.sigma[r1i].update_data(p, self.penality, -1)
                return True
            return False

        # route diverse   
        r1seq1 = [self.sigma[r1i].subseq[0][c1i-1]]
        r1seq2 = [self.sigma[r2i].subseq[c2i][c2i]]
        r1seq3 = [self.sigma[r1i].subseq[c1i + 1][-1]]
        r2seq1 = [self.sigma[r2i].subseq[0][c2i-1]]
        r2seq2 = [self.sigma[r1i].subseq[c1i][c1i]]
        r2seq3 = [self.sigma[r2i].subseq[c2i + 1][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2 + r1seq3, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2 + r2seq3, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            self.sigma[r1i].customer[c1i] = c2
            self.sigma[r2i].customer[c2i] = c1
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            self.nodeRoutes[c1] = r2i
            self.nodeRoutes[c2] = r1i
            return True
        return False
    
    def M5(self, p, c1, c1i, r1i, c2, c2i, r2i): # CROSS 2-1
        
        if c1i == (len(self.sigma[r1i].customer) - 2) or c2 == 0:
            return False
        
        # stessa route
        if r1i == r2i:
            if c2i == c1i + 1:
                return False
            if c1i < c2i:
                seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
                seq2 = [self.sigma[r1i].subseq[c2i][c2i]]
                if c1i + 2 != c2i:
                    seq3 = [self.sigma[r1i].subseq[c1i + 2][c2i - 1]]
                else:
                    seq3 = []
                seq4 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
                seq5 = [self.sigma[r1i].subseq[c2i + 1][-1]]
            else:
                seq1 = [self.sigma[r1i].subseq[0][c2i - 1]]
                seq2 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
                if c2i + 1 != c1i:
                    seq3 = [self.sigma[r1i].subseq[c2i + 1][c1i - 1]]
                else:
                    seq3 = []
                seq4 = [self.sigma[r1i].subseq[c2i][c2i]]
                seq5 = [self.sigma[r1i].subseq[c1i + 2][-1]]
            newcost = evalN(p, seq1 + seq2 + seq3 + seq4 + seq5, self.penality)
            if newcost < self.sigma[r1i].costo:
                self.sigma[r1i].costo = newcost
                successor = self.sigma[r1i].customer[c1i + 1]
                self.sigma[r1i].customer[c1i] = c2
                self.sigma[r1i].customer[c2i] = c1
                self.sigma[r1i].customer.insert(c2i + 1, successor)
                if c1i < c2i:
                    del self.sigma[r1i].customer[c1i + 1]
                else:
                    del self.sigma[r1i].customer[c1i + 2]
                self.sigma[r1i].update_data(p, self.penality, -1)
                return True
            return False
        
        # route diverse
        r1seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
        r1seq2 = [self.sigma[r2i].subseq[c2i][c2i]]
        r1seq3 = [self.sigma[r1i].subseq[c1i + 2][-1]]
        r2seq1 = [self.sigma[r2i].subseq[0][c2i - 1]]
        r2seq2 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
        r2seq3 = [self.sigma[r2i].subseq[c2i + 1][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2 + r1seq3, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2 + r2seq3, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            successor = self.sigma[r1i].customer[c1i + 1]
            self.sigma[r1i].customer[c1i] = c2
            self.sigma[r2i].customer[c2i] = c1
            self.sigma[r2i].customer.insert(c2i + 1, successor)
            del self.sigma[r1i].customer[c1i + 1]
            self.nodeRoutes[c1] = r2i
            self.nodeRoutes[c2] = r1i
            self.nodeRoutes[successor] = r2i
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            return True
        return False
    
    def M6(self, p, c1, c1i, r1i, c2, c2i, r2i): # CROSS 2-2
        
        if c2 == 0:
            return False
        
        if c1i == (len(self.sigma[r1i].customer) - 2) or c2i == (len(self.sigma[r2i].customer) - 2):
            return False
        
        # stessa route
        if r1i == r2i:
            if c1i + 1 == c2i:
                return False
            if c2i + 1 == c1i:
                return False
            reverse = False
            if c1i > c2i:
                tmp = c1i
                c1i = c2i
                c2i = tmp
                reverse = True
            seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
            seq2 = [self.sigma[r1i].subseq[c2i][c2i + 1]]
            if c1i + 2 != c2i:
                seq3 = [self.sigma[r1i].subseq[c1i + 2][c2i - 1]]
            else:
                seq3 = []
            seq4 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
            seq5 = [self.sigma[r1i].subseq[c2i + 2][-1]]
            newcost = evalN(p, seq1 + seq2 + seq3 + seq4 + seq5, self.penality)
            if newcost < self.sigma[r1i].costo:
                self.sigma[r1i].costo = newcost
                successor1 = self.sigma[r1i].customer[c1i + 1]
                successor2 = self.sigma[r1i].customer[c2i + 1]
                if not reverse:
                    self.sigma[r1i].customer[c1i] = c2
                    self.sigma[r1i].customer[c2i] = c1
                    self.sigma[r1i].customer[c1i + 1] = successor2
                    self.sigma[r1i].customer[c2i + 1] = successor1
                else:
                    self.sigma[r1i].customer[c1i] = c1
                    self.sigma[r1i].customer[c2i] = c2
                    self.sigma[r1i].customer[c1i + 1] = successor2
                    self.sigma[r1i].customer[c2i + 1] = successor1
                self.sigma[r1i].update_data(p, self.penality, -1)
                return True
            return False
        
        
        # route diverse
        r1seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
        r1seq2 = [self.sigma[r2i].subseq[c2i][c2i + 1]]
        r1seq3 = [self.sigma[r1i].subseq[c1i + 2][-1]]
        r2seq1 = [self.sigma[r2i].subseq[0][c2i - 1]]
        r2seq2 = [self.sigma[r1i].subseq[c1i][c1i + 1]]
        r2seq3 = [self.sigma[r2i].subseq[c2i + 2][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2 + r1seq3, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2 + r2seq3, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            successor1 = self.sigma[r1i].customer[c1i + 1]
            successor2 = self.sigma[r2i].customer[c2i + 1]
            self.sigma[r1i].customer[c1i] = c2
            self.sigma[r2i].customer[c2i] = c1
            self.sigma[r1i].customer[c1i + 1] = successor2
            self.sigma[r2i].customer[c2i + 1] = successor1
            self.nodeRoutes[c1] = r2i
            self.nodeRoutes[c2] = r1i
            self.nodeRoutes[successor1] = r2i
            self.nodeRoutes[successor2] = r1i
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            return True
        return False
        
        
    
    
    def M7(self, p, c1, c1i, r1i, c2, c2i, r2i): # 2-Opt
        if c2 == 0:
            return False
        
        # stessa route
        if r1i == r2i:
            if c1i > c2i:
                temp = c1i
                c1i = c2i
                c2i = temp
            seq1 = [self.sigma[r1i].subseq[0][c1i - 1]]
            seq2 = [self.sigma[r1i].subseq[c2i][c1i]]
            seq3 = [self.sigma[r1i].subseq[c2i + 1][-1]]
            newcost = evalN(p, seq1 + seq2 + seq3, self.penality)
            if newcost < self.sigma[r1i].costo:
                self.sigma[r1i].costo = newcost
                utils.reverse_sublist(self.sigma[r1i].customer, c1i, c2i + 1)
                self.sigma[r1i].update_data(p, self.penality, -1)
                return True
            return False
        
        # route diverse
        return False

        
    def M8(self, p, c1, c1i, r1i, c2, c2i, r2i): # 2-Opt* alternativa
    
                
        # stessa route
        if r1i == r2i:
            return False
        
        # route diverse
        r1seq1 = [self.sigma[r1i].subseq[0][c1i]]
        r1seq2 = [self.sigma[r2i].subseq[c2i][0]]
        r2seq1 = [self.sigma[r1i].subseq[-1][c1i + 1]]
        r2seq2 = [self.sigma[r2i].subseq[c2i + 1][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            start1 = self.sigma[r1i].customer[:(c1i + 1)]
            end1 = self.sigma[r2i].customer[:(c2i + 1)]
            end1.reverse()
            start2 = self.sigma[r1i].customer[(c1i + 1):]
            start2.reverse()
            end2 = self.sigma[r2i].customer[(c2i + 1):]
            for node in end1:
                self.nodeRoutes[node] = r1i
            for node in start2:
                self.nodeRoutes[node] = r2i
            self.sigma[r1i].customer = start1 + end1
            self.sigma[r2i].customer = start2 + end2
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            return True
        return False
            

    
    def M9(self, p, c1, c1i, r1i, c2, c2i, r2i): # 2-Opt*
        
        # stessa route
        if r1i == r2i:
            return False
        
        # route diverse
        r1seq1 = [self.sigma[r1i].subseq[0][c1i]]
        r1seq2 = [self.sigma[r2i].subseq[c2i + 1][-1]]
        r2seq1 = [self.sigma[r2i].subseq[0][c2i]]
        r2seq2 = [self.sigma[r1i].subseq[c1i + 1][-1]]
        r1newcost = evalN(p, r1seq1 + r1seq2, self.penality)
        r2newcost = evalN(p, r2seq1 + r2seq2, self.penality)
        if r1newcost + r2newcost < self.sigma[r1i].costo + self.sigma[r2i].costo:
            self.sigma[r1i].costo = r1newcost
            self.sigma[r2i].costo = r2newcost
            start1 = self.sigma[r1i].customer[:(c1i + 1)]
            end1 = self.sigma[r2i].customer[(c2i + 1):]
            start2 = self.sigma[r2i].customer[:(c2i + 1)]
            end2 = self.sigma[r1i].customer[(c1i + 1):]
            for node in end1:
                self.nodeRoutes[node] = r1i
            for node in end2:
                self.nodeRoutes[node] = r2i
            self.sigma[r1i].customer = start1 + end1
            self.sigma[r2i].customer = start2 + end2
            self.sigma[r1i].update_data(p, self.penality, -1)
            self.sigma[r2i].update_data(p, self.penality, -1)
            return True
        return False
    
    
        
    def educate(self, p):
        NB = p.neigh[:]
        moves = [self.M1, self.M2, self.M3, self.M4, self.M5, self.M6, self.M7, self.M8, self.M9]
        while NB != []:
            pairindex = random.randint(0, len(NB) - 1)
            c1 = NB[pairindex][0]                           # Customer 1
            r1i = self.nodeRoutes[c1]                       # Route 1 index
            c1i = self.sigma[r1i].customer.index(c1)        # Customer 1 index
            c2 = NB[pairindex][1]                           # Customer 2
            r2i = self.nodeRoutes[c2]                       # Route 2 index
            if c2 == 0:
                r2i = r1i
                c2i = 0
            else:
                c2i = self.sigma[r2i].customer.index(c2)    # Customer 2 index
            random.shuffle(moves)
            
            moved = False
            i = 0
            while (not moved) and i < len(moves):
                moved = moves[i](p, c1, c1i, r1i, c2, c2i, r2i)
                i += 1
            if not moved:
                del NB[pairindex]
            else:
                NB = p.neigh[:]
        self.sigma = [x for x in self.sigma if x.customer != [0,0]]
        self.recomputearcs(p)
        self.recomputeparameters(p)
        
class Route:
    def __init__(self, nodes, p, penality):
        self.customer = [0] + nodes + [0]
        self.recomputecost(p, penality)
    def recomputecost(self, p, penality):
        try:
            self.update_data(p, penality, -1)
            self.costo = self.subseq[0][-1].costo
            self.carico = self.subseq[0][-1].carico
            self.feas = True
            loadexcess = max(0, self.carico - p.C)
            if loadexcess > 0:
                self.feas = False
                self.costo += loadexcess*penality
            return self.costo
        except:
            self.costo = 0
            self.feas = True
    def update_data(self, p, penality, update):
        if update == -1:
            mat_dim = len(self.customer)
            self.subseq = []
            for i in range(mat_dim):
                self.subseq.append([])
                sub_carico = 0
                sub_costo = 0
                for j in range(i):
                    self.subseq[i].append(seqdata(self.subseq[j][i].costo, self.subseq[j][i].carico, self.subseq[j][i].end, self.subseq[j][i].start))
                for j in range(i, mat_dim):
                    sub_carico += p.demand[self.customer[j]]
                    if i != j:
                        sub_costo += p.dist[self.customer[j-1]][self.customer[j]]                   
                    self.subseq[i].append(seqdata(sub_costo, sub_carico, self.customer[i], self.customer[j]))
            
            
class seqdata:
    def __init__(self, costo, carico, start, end):
            self.costo = costo
            self.carico = carico
            self.start = start
            self.end = end
    
def routing(grandTour, delimiters, p, penality):                                          # Torna una sigma da un grand tour e dei delimiters
    sigma = []
    tour = grandTour[:]
    route = []
    for i in range(len(delimiters) - 1):
        routeLen = delimiters[i+1] - delimiters[i]
        for j in range(routeLen):
            route.append(tour[0])
            del tour[0]
        r = Route(route, p, penality)
        sigma.append(r)
        route = []
    return sigma

def split(grandTour, p, penality):                                                        # Calcola i trip delimiters
    route = grandTour[:]
    route.insert(0,0)
    edges = []    
    for i in range(len(route)):
        seqdata = [0]
        for j in range(i+1, len(route)):
            seqdata.append(route[j])
            sigma = seqdata[:]
            sigma.append(0)
            feasible, costo = evalutation.cost(sigma, p, penality)
            if feasible:
                edges.append((i, j, costo))
            else:
                break   
    costo, delimiters = utils.shortestPath(edges, 0, len(route) - 1)        
    return costo, delimiters

def evalN(p, seq, penality):
    carico = 0
    costo = 0
    seq_num = len(seq) - 1
    for i in range(seq_num):
        carico += seq[i].carico
        costo += seq[i].costo
        costo += p.dist[seq[i].end][seq[i+1].start]
    costo += seq[seq_num].costo
    carico += seq[seq_num].carico
    loadexcess = max(0, carico - p.C)
    costo += loadexcess*penality
    return costo
            