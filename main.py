import random
import copy
import time
from param import param
import utils
import cProfile
import pstats
import io
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import maincomponents as mc
from os import listdir
from os.path import isfile, join
import math
import traceback


def uhgs(minSol, maxSol, omega, muelite, itDiv):

    minSol = int(minSol)
    maxSol = int(maxSol)
    instance = "X-n101-k25.dat"
    itMax = 2000
    prep = 0.5
    near = 0.2
    muclose = 0.8
    resultfile = instance + "_results.txt"
    try:
        p = param("./instances/" + instance, minSol, maxSol, omega,
                  muelite, prep, itMax, itDiv, near, muclose)
        possol = []
        while(len(possol) == 0):
            possol, negsol = mc.initializepop(p)
            if len(possol) == 0:
                p.omega += 10
        mc.recomputesimilarity(negsol, p)
        mc.recomputefitness(negsol, p)
        mc.recomputesimilarity(possol, p)
        mc.recomputefitness(possol, p)
        start = time.time()
        it = 0
        itDivCount = 0
        best = copy.deepcopy(min(possol, key=utils.takecost))
        besttime = 0
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
            if min(possol, key=utils.takecost).costo < best.costo:
                it = 0
                itDivCount = 0
                best = copy.deepcopy(min(possol, key=utils.takecost))
                besttime = time.time() - start
            if len(possol) > p.maxSol:
                mc.recomputesimilarity(possol, p)
                mc.recomputefitness(possol, p)

                del possol[p.minSol:]
                if best.costo < min(possol, key=utils.takecost).costo:
                    possol.append(best)
            if len(negsol) > p.maxSol:
                mc.recomputesimilarity(negsol, p)
                mc.recomputefitness(negsol, p)
                del negsol[p.minSol:]
            if itDivCount > p.itDiv*p.itMax:
                possol.sort(key=utils.takefitness, reverse=True)
                negsol.sort(key=utils.takefitness, reverse=True)
                del possol[int(p.minSol/3):]
                del negsol[int(p.minSol/3):]
                possol, negsol = mc.fillpop(possol, negsol, p)
                mc.recomputesimilarity(possol, p)
                mc.recomputefitness(possol, p)
                mc.recomputesimilarity(negsol, p)
                mc.recomputefitness(negsol, p)
                itDivCount = 0

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
        return -999999999


if __name__ == '__main__':
    hp1 = random.randint(10, 50)
    hp2 = random.randint(60, 100)
    hp3 = random.randint(5, 500)
    hp4 = 0.5 + random.random()*1.5
    hp5 = 0.1 + random.random()*(0.51-0.1)
    print(hp1, hp2, hp3, hp4, hp5)
    for i in range(10):
        best = uhgs(hp1, hp2, hp3, hp4, hp5)

