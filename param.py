import numpy as np
import csv
import math
                                                                         
class param:
    
    minSol = 30                                                                         # Cardinalità minima di possol e negsol
    maxSol = 70                                                                         # Limite di cardinalità per possol e negsol
    omega = 40                                                                          # Peso load excess
    muelite = 1.5                                                                       # Peso diversità (rispetto maxSol) (più è alto e meno pesa)
    Prep = 0.5                                                                          # Probabilità riparazione soluzioni infeasible
    itMax = 2000                                                                        # Numero massimo di iterazioni senza improvements
    itDiv = 0.4                                                                         # Iterazioni (rispetto itMax) prima di diversification
    near = 0.2                                                                          # Percentuale nodi da considerare vicini nell'education
    muclose = 1                                                                         # Percentuali di individui da considerare vicini nel calcolo di diversità
    generation_size = maxSol - minSol
    csi_ref = 0.2
    
    
    def __init__(self, filename, minSol, maxSol, omega, muelite, prep, itMax, itDiv, near, muclose):
        self.filename = filename
        self.minSol = minSol
        self.maxSol = maxSol
        self.omega = omega
        self.muelite = muelite
        self.Prep = prep
        self.itMax = itMax
        self.itDiv = itDiv
        self.near = near
        self.muclose = muclose
        with open(filename) as tsv:
            readpos = False
            readdemand = False
            i = -1
            j = -1
            for line in csv.reader(tsv, dialect="excel-tab"): 
                if line[0].startswith("NODE_COORD_SECTION"):
                    readpos = True
                if line[0].startswith("DEMAND_SECTION"):
                    readpos = False
                    readdemand = True
                if line[0].startswith("DEPOT_SECTION"):
                    readdemand = False
                if line[0].startswith("DIMENSION"):
                    self.n = int(line[1])
                    self.demand = np.zeros(self.n, dtype = int)
                    self.pos = np.zeros((self.n + 1, 2), dtype = int)
                if line[0].startswith("CAPACITY"):
                    self.C = int(line[1])
                if readpos:
                    if i!= -1:
                        self.pos[i][0] = line[1]
                        self.pos[i][1] = line[2]
                    i+=1
                if readdemand:
                    if j != -1:
                        self.demand[j] = int(line[1])
                    j+=1
        
        
        
        self.dist = np.zeros((self.n, self.n), dtype = int)
        for i in range(self.n):
            for j in range(self.n):
                self.dist[i][j] = int(round(math.sqrt(math.pow(self.pos[i][0] - self.pos[j][0], 2) + math.pow(self.pos[i][1] - self.pos[j][1], 2))))
        
        
#        self.omega = int(round(2*np.average(self.dist)/np.average(self.demand)))
        self.neigh = []
        numNeigh = int(self.n*self.near)
        for i in range(1, self.n):
            auxdist = list(self.dist[i])
            auxdist[i] = math.inf
            for k in range(numNeigh):
                j = auxdist.index(min(auxdist))
                self.neigh.append([i, j])
                auxdist[j] = math.inf
#        print(self.neigh, len(self.neigh))
                
    def printparam(self):
        print("filename: ", self.filename)
        print("minsol: ", self.minSol)
        print("maxsol: ", self.maxSol)
        print("omega: ", self.omega)
        print("muelite: ", self.muelite)
        print("Prep: ", self.Prep)
        print("itMax: ", self.itMax)
        print("itDiv: ", self.itDiv)
        print("near: ", self.near)
        print("muclose: ", self.muclose)
    def printonfile(self, filename):
        myfile = open(filename, 'a')
        myfile.write("filename: ")
        myfile.write(self.filename)
        myfile.write("\nminsol: ")
        myfile.write(str(self.minSol))
        myfile.write("\nmaxsol: ")
        myfile.write(str(self.maxSol))
        myfile.write("\nomega: ")
        myfile.write(str(self.omega))
        myfile.write("\nmuelite: ")
        myfile.write(str(self.muelite))
        myfile.write("\nPrep: ")
        myfile.write(str(self.Prep))
        myfile.write("\nitMax: ")
        myfile.write(str(self.itMax))
        myfile.write("\nitDiv: ")
        myfile.write(str(self.itDiv))
        myfile.write("\nnear: ")
        myfile.write(str(self.near))
        myfile.write("\nmuclose: ")
        myfile.write(str(self.muclose))
        myfile.close()