import time
import maincomponents as mc
from sol import solution, Route
from param import param
import random
import numpy as np
import cProfile, pstats, io
import math
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
#start = time.time()
#for i in range(p.n):
#    mc.recomputefitness(possol, p)
#print(time.time() - start)
#
#
#start = time.time()
#route1 = Route([1,2,3,4,5], p, p.omega)
#for i in range(10000):
#    route2 = Route(copy.copy(route1.customer), p, p.omega)
#print(time.time() - start)
#
#
#
#route1 = Route([1,2,3,4,5], p, p.omega)
#route2 = Route(copy.copy(route1.customer), p, p.omega)
#route2.customer[0] = 0
#print(route1.customer, route2.customer)
#
#a = [1,2,3,4,5]
#b = a[3:]
#c = a[:3]
#d = a+b
#d[0] = 0
#print(a,b,c,d)
##
#points = []
#for i in range(1, p.n):
#    points.append(i) 
#start = time.time()
#grandTour = points[:]
#random.shuffle(grandTour)
#sol = solution(grandTour, p) 
#splittime = time.time() - start
#print(splittime)
#start = time.time()
#sol.educate(p)
#edutime = time.time() - start
#print(edutime)

#p = param("./instances/A-n32-k5.dat")
#a = [1, 2, 3]
#b = a[:2]
#b.reverse()

#points = []
#for i in range(1, p.n):
#    points.append(i) 
#grandTour = points[:]
#random.shuffle(grandTour)
#sol2 = solution(grandTour, p) 

#a = Route([1,2,3], p, p.omega, -1)
#a = np.zeros((5,5))
#a[0][0] = Route([1,2,3], p, p.omega, 0)
#points = []    
#for i in range(1, p.n):
#    points.append(i) 
#grandTour = points[:]
#sol = solution(grandTour, p) 

#
#sol.M9(p, 4, 4, 0, 10, 3, 1)
#for i in range(1,7):
#    print(sol.M9(p, i, i, 0, 10, 3, 1))
#for pair in p.neigh:
#    c1 = pair[0]                           # Customer 1
#    r1i = sol.nodeRoutes[c1]                       # Route 1 index
#    c1i = sol.sigma[r1i].customer.index(c1)        # Customer 1 index
#    c2 = pair[1]                           # Customer 2
#    r2i = sol.nodeRoutes[c2]                       # Route 2 index
#    if c2 == 0:
#        r2i = r1i
#        c2i = -1
#    else:
#        c2i = sol.sigma[r2i].customer.index(c2)
#    sol.M1(p, c1, c1i, r1i, c2, c2i, r2i)
#    
#sol.educate(p)
   
p = param("./instances/X-n106-k14.dat", 30, 70, 40, 0.4, 0.5, 100, 1, 0.2, 0.2)

#points = []
#for i in range(1, p.n):
#    points.append(i) 
#grandTour = points[:]
#sol = solution(grandTour, p) 


#sol.M9(p, 4, 3, 0, 10, 2, 1)
#for i in range(1,7):
#    print(sol.M6(p, i, i-1, 0, 8, 0, 1))
#sol.educate(p)

    


#points = []
#for i in range(1, p.n):
#    points.append(i) 
#grandTour = points[:]
#sol = solution(grandTour, p) 


#sol.M9(p, 4, 3, 0, 10, 2, 1)
#for i in range(1,7):
#    print(sol.M6(p, i, i-1, 0, 8, 0, 1))
#sol.educate(p)

    
def profile(fnc):
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream = s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner

@profile
def education():
    points = []
    for i in range(1, p.n):
        points.append(i)
    solutions = []
    for j in range(100):
        grandTour = points[:]
        random.shuffle(grandTour)
        sol = solution(grandTour, p) 
        sol.educate(p)
        solutions.append(sol)
    return solutions





@profile    
def paralleleducation():
    args = []
    grandTour = list(range(1,p.n))
    for i in range(100):
        random.shuffle(grandTour)
        args.append([grandTour, p])
    with ProcessPoolExecutor() as executor:
        result = executor.map(edu, args)
    solutions = list(result)
    return solutions
    
def edu(args):
    gt = args[0]
    p = args[1]
    sol = solution(gt, p)
    sol.educate(p)
    return sol


#
#def getindexes(pair, p):
#    c1 = pair[0]                           # Customer 1
#    r1i = sol.nodeRoutes[c1]                       # Route 1 index
##    print(c1, r1i, self.sigma[r1i].customer)
#    c1i = sol.sigma[r1i].customer.index(c1)        # Customer 1 index
#    c2 = pair[1]                           # Customer 2
#    r2i = sol.nodeRoutes[c2]                       # Route 2 index
#    if c2 == 0:
#        r2i = r1i
#        c2i = -1
#    else:
#        c2i = sol.sigma[r2i].customer.index(c2)    # Customer 2 index
#    return p, c1, c1i, r1i, c2, c2i, r2i
#
#
#for sol in possol:
#    if sol.costo == best.costo:
#        print(sol.__dict__, best.__dict__)
#r = [1,2,3]
#rdemand= [p.demand[x] for x in r] 
#rcost = [p.dist[r[i]][r[i+1]] for i in range(len(r)-1)]
#
#for route in sol.sigma:
#    print(route.customer)
#
#bks = [21,31,19,17,13,7,26,12,1,16,30,27,24,29,18,8,9,22,15,10,25,5,20,14,28,11,4,23,3,2,6]
#bksol = solution(bks,p)

#class subseq:
#    def __init__(self, p, cost, demand):
#        self.demand = demand
#        self.cost = cost
#        self.loadexcess = max(0, demand - p.C)


#class distances:
#    def __init__(self, p):
#        self.d = []
#        for i1 in range(p.n):
#            self.d.append([subseq(p, p.dist[0][i1], p.demand[i1]), []])
#            for i2 in range(p.n):
#                self.d[i1][1].append([subseq(p, self.d[i1][0].cost + p.dist[i1][i2], self.d[i1][0].demand + p.demand[i2]), []])
#                for i3 in range(p.n):
#                    self.d[i1][1][i2][1].append([subseq(p, self.d[i1][1][i2][0].cost + p.dist[i2][i3], self.d[i1][1][i2][0].demand + p.demand[i3]), []])
#                    for i4 in range(p.n):
#                        self.d[i1][1][i2][1][i3][1].append([subseq(p, self.d[i1][1][i2][1][i3][0].cost + p.dist[i3][i4], self.d[i1][1][i2][1][i3][0].demand + p.demand[i4]), []])
#prova = distances(p)       
        
#@profile
#def provatempo():
# for i in range(100000):
    
#def function(val):
#    return val + 1
#
#def paralleltask():
#    args = list(range(1,100000))
#    with ProcessPoolExecutor() as executor:
#        result = executor.map(function, args)
#    result = list(result)
#    return result
#
#def main():
#    test = paralleltask()
#    return test
#
#if __name__ == '__main__': 
#    main()
    

#p = param("./instances/X-n101-k25.dat", 25, 50, 40, 1.5, 0.5, 2000, 0.4, 0.2, 0.5)
#from os import listdir
#from os.path import isfile, join
#mypath = "./instances"
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    
if __name__ == '__main__':
    x = paralleleducation()