import random
import copy
import time
from param import param
import utils
import cProfile, pstats, io
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import maincomponents as mc
from os import listdir
from os.path import isfile, join
import math
import traceback

###################################################################### NOTE ###
# concurrent.features seems to need a restarting of the cosole kernel and
# launch all the imported file to work correctly.
# If the program doesn't start, restart kernel and run all files in this folder
# (except test.py and GPGOoptimaizer.py), then execute main.py again.
###############################################################################




######## UNCOMMENT THIS LINES TO PRIFILE ######################################
#def profile(fnc):
#    def inner(*args, **kwargs):
#        pr = cProfile.Profile()
#        pr.enable()
#        retval = fnc(*args, **kwargs)
#        pr.disable()
#        s = io.StringIO()
#        sortby = 'cumulative'
#        ps = pstats.Stats(pr, stream = s).sort_stats(sortby)
#        ps.print_stats()
#        print(s.getvalue())
#        return retval
#    return inner
#
#@profile   ###################################################################                                              
def uhgs(minSol, maxSol, omega, muelite, itDiv):
    
    minSol = int(minSol)
    maxSol = int(maxSol)
    instance = "X-n101-k25.dat"
    itMax = 2000
    prep = 0.5
    near = 0.2
    muclose = 0.8
    
    resultfile = instance + "_results.txt"
 
####### UNCOMMENT THIS LINE AND INDENT TO SOLVE FOR ALL INSTANCES #############
#    mypath = "./instances"
#    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]   
#    for cvrpProblem in onlyfiles:
###############################################################################    
    try:
        # Loading instance and setting parameters
        p = param("./instances/" + instance, minSol, maxSol, omega, muelite, prep, itMax, itDiv, near, muclose)
        
        # Initialize population - possol contains feasible solutions, negsol the infeasible ones
        possol = []
        while(len(possol) == 0):
            possol, negsol = mc.initializepop(p)
            if len(possol) == 0:
                p.omega += 10
        # Similarity of individuals calculation
        mc.recomputesimilarity(negsol, p)
        mc.recomputefitness(negsol, p)
        mc.recomputesimilarity(possol, p)
        mc.recomputefitness(possol, p)
         
        # Iterative structure of UHGS
        start = time.time()
        it = 0
        itDivCount = 0
        best = copy.deepcopy(min(possol, key = utils.takecost))
        besttime = 0
#        print("best is:", best.costo)
        while it < p.itMax and (time.time() - start)/60 < 30:                                                 
            args = []
            for _ in range(10):
                args.append([possol, negsol, p])
            with ProcessPoolExecutor() as executor:
                result = executor.map(mc.crossandedu, args)
            solutions = list(result)
            solutions = [item for sublist in solutions for item in sublist]
            for sol in solutions:
                if sol.feas:
                    possol.append(sol)
                else:
                    negsol.append(sol)
            
            it += int(10)
            itDivCount += int(10)        
#            if not it % 100:
#                print("iteration number:", it, " - best here is:", best.costo)
            if min(possol, key = utils.takecost).costo < best.costo:                        # Saving best solution
                it = 0
                itDivCount = 0
                best = copy.deepcopy(min(possol, key = utils.takecost))
                besttime = time.time() - start
#                print("new best finded:", best.costo)
            if len(possol) > p.maxSol:                                                      # Survivor selection                                          
#                print("deduplicating and deleting feasible solutions")
                mc.recomputesimilarity(possol, p)
                mc.recomputefitness(possol, p)
#                possol = utils.deduplicate(possol)
    
                del possol[p.minSol:]
                if best.costo < min(possol, key = utils.takecost).costo:
#                    p.muelite = round(p.muelite + 0.05, 3)
#                    print("best deleted, muelite updated to", p.muelite)
#                    print("best deleted")
                    possol.append(best)
#                    it = 0
#                    itDivCount = 0
            if len(negsol) > p.maxSol:
#                print("deduplicating and deleting infeasible solutions")
                mc.recomputesimilarity(negsol, p)
                mc.recomputefitness(negsol, p)
#                negsol = utils.deduplicate(negsol)
                del negsol[p.minSol:]
            if itDivCount > p.itDiv*p.itMax:                                                # Diversification
#                print("coming back to mu/3 and introducing new genetic material")
#                print("best here is still: ", best.costo)
                possol.sort(key = utils.takefitness, reverse = True)
                negsol.sort(key = utils.takefitness, reverse = True)
                del possol[int(p.minSol/3):]
                del negsol[int(p.minSol/3):]
                possol, negsol = mc.fillpop(possol, negsol, p)
                mc.recomputesimilarity(possol, p)
                mc.recomputefitness(possol, p)
                mc.recomputesimilarity(negsol, p)
                mc.recomputefitness(negsol, p)
                itDivCount = 0
        
#        p.printparam()        
#        print("finished in:", (time.time() - start)/3600, "h. Best founded after", besttime/3600, "h.")        
#        best.printsolution()
        
        p.printonfile(resultfile)
        best.printonfile(resultfile)
        file = open(resultfile, 'a')
        file.write("\nBest founded after ")
        file.write(str(besttime/60))
        file.write(" min\nProgram ended in: ")
        file.write(str((time.time() - start)/60))
        file.write(" min\n\n\n\n")
        file.close()
        return -best.costo
    except Exception:
        print("error")
        traceback.print_exc()
        
####### UNCOMMENT THIS LINES TO DEBUG #########################################        
#        myfile = open(resultfile, 'a')
#        myfile.write("\nerror")
#        myfile.close()        
#        myfile = open(resultfile, 'a')
#        myfile.write("\n\n\n\n\nERROR ON FILE:")
#        myfile.write(instance)
#        myfile.write("\n")
#        myfile.close()
#        p.printonfile(resultfile)
#        myfile = open(resultfile, 'a')
#        myfile.write("\n\n\n")
#        myfile.close()
###############################################################################
        
        return -999999999

if __name__ == '__main__':
############ THESE ARE 10 EXCEC FOR A RANDOM SETTING OF HPs ###################
    hp1 = random.randint(10,50)
    hp2 = random.randint(60,100)
    hp3 = random.randint(5,500)
    hp4 = 0.5 + random.random()*1.5
    hp5 = 0.1 + random.random()*(0.51-0.1)
    print(hp1,hp2,hp3,hp4,hp5)
    for i in range(10):
        best = uhgs(hp1, hp2, hp3, hp4, hp5)
###############################################################################

