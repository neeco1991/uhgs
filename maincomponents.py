from sol import solution
import utils
import time
import random
import copy
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
from param import param
import cProfile
import pstats
import io


def initializepop(p):
    possol = []
    negsol = []
    togenerate = 4*p.minSol
    grandTour = list(range(1, p.n))
    args = []
    for _ in range(togenerate):
        args.append([grandTour, p])
    with ProcessPoolExecutor() as executor:
        result = executor.map(generateindividuals, args)
    solutions = list(result)
    solutions = [item for sublist in solutions for item in sublist]
    for sol in solutions:
        if sol.feas:
            possol.append(sol)
        else:
            negsol.append(sol)
    return possol, negsol


def generateindividuals(args):
    gradTour = args[0]
    p = args[1]
    solutions = []
    sol = solution(gradTour, p)
    sol.educate(p)
    solutions.append(sol)
    if not sol.feas:
        if random.random() < p.Prep:
            newsol = copy.deepcopy(sol)
            newsol.penality *= 10
            newsol.recomputecost(p)
            newsol.educate(p)
            solutions.append(newsol)
            if not newsol.feas:
                newnewsol = copy.deepcopy(newsol)
                newnewsol.penality *= 10
                newnewsol.recomputecost(p)
                newnewsol.educate(p)
                solutions.append(newnewsol)
                if not newnewsol.feas:
                    newnewnewsol = copy.deepcopy(newnewsol)
                    newnewnewsol.penality *= 10
                    newnewnewsol.recomputecost(p)
                    newnewnewsol.educate(p)
                    solutions.append(newnewnewsol)
    return solutions


def fillpop(possol, negsol, p):
    grandTour = []
    for i in range(1, p.n):
        grandTour.append(i)
    while len(possol) < p.minSol or len(negsol) < p.minSol:
        random.shuffle(grandTour)
        sol = solution(grandTour, p)
        sol.educate(p)
        if sol.feas:
            possol.append(sol)
        else:
            negsol.append(sol)
            if random.random() < p.Prep:
                newsol = copy.deepcopy(sol)
                newsol.penality *= 10
                newsol.recomputecost(p)
                newsol.educate(p)
                if newsol.feas:
                    possol.append(newsol)
                else:
                    negsol.append(newsol)
        if len(possol) > 4*p.maxSol or len(negsol) > 4*p.maxSol:
            return possol, negsol
    return possol, negsol


def brokenpair(sol1, sol2, p):
    trues = np.logical_and(sol1.myarcs, sol2.myarcs)
    _, counts = np.unique(trues, return_counts=True)
    return counts[1]


def calcsimilarity(sol, solutions, p):
    dist = []
    for othersol in solutions:
        if othersol != sol:
            dist.append(brokenpair(sol, othersol, p))
    dist.sort(reverse=True)
    if int(p.muclose*len(solutions)) > 1:
        del dist[int(p.muclose*len(solutions)):]
    if len(dist) > 0:
        sol.sim = sum(dist)/len(dist)
    else:
        sol.sim = 0
    return 1


def recomputesimilarity(solutions, p):
    for sol in solutions:
        calcsimilarity(sol, solutions, p)
    return 1


def crossover(possol, negsol, p):
    totlen = len(possol) + len(negsol) - 1
    genitore1 = -1
    genitore2 = -1

    while genitore1 == genitore2:
        i = random.randint(0, totlen)
        j = i
        while j == i:
            j = random.randint(0, totlen)
        if i < len(possol):
            pick1 = possol[i]
        else:
            pick1 = negsol[i - len(possol)]
        if j < len(possol):
            pick2 = possol[j]
        else:
            pick2 = negsol[j - len(possol)]
        if pick1.fitness > pick2.fitness:
            genitore1 = pick1
        else:
            genitore1 = pick2
        i = random.randint(0, totlen)
        j = i
        while j == i:
            j = random.randint(0, totlen)
        if i < len(possol):
            pick1 = possol[i]
        else:
            pick1 = negsol[i - len(possol)]
        if j < len(possol):
            pick2 = possol[j]
        else:
            pick2 = negsol[j - len(possol)]
        if pick1.fitness > pick2.fitness:
            genitore2 = pick1
        else:
            genitore2 = pick2
    print("genitore1: ", genitore1.costo, genitore1.feas,
          "genitore2:", genitore2.costo, genitore2.feas)
    sonGT = OXcrossover(genitore1, genitore2, p)
    son = solution(sonGT, p)
    return son


def OXcrossover(sol1, sol2, p):
    tour1 = sol1.GT[:]
    tour2 = sol2.GT[:]
    print(tour1)
    print(tour2)
    son1 = list(np.zeros(p.n-1))
    son2 = list(np.zeros(p.n-1))
    start = 2
    end = 1
    while start >= end:
        start = random.randint(0, p.n - 3)
        end = random.randint(0, p.n - 2)
    print(start, end)
    fixed1 = tour1[start:(end+1)]
    fixed2 = tour2[start:(end+1)]
    son1[start:(end+1)] = fixed1
    son2[start:(end+1)] = fixed2
    j = end + 1
    k = end + 1
    for i in range(end + 1, p.n + start - 1):
        while tour2[j % (p.n-1)] in fixed1:
            j += 1
        while tour1[k % (p.n-1)] in fixed2:
            k += 1
        son1[i % (p.n-1)] = tour2[j % (p.n-1)]
        son2[i % (p.n-1)] = tour1[k % (p.n-1)]
        j += 1
        k += 1
    print(son1)
    print(son2)
    if random.randint(0, 1):
        return son1
    else:
        return son2


def recomputefitness(solutions, p):
    solutions.sort(key=utils.takecost, reverse=True)
    for rank, sol in enumerate(solutions):
        sol.fitness = rank
    solutions.sort(key=utils.takesimilarity, reverse=True)
    for rank, sol in enumerate(solutions):
        sol.fitness += (1-p.muelite*p.minSol/len(solutions))*rank
    solutions.sort(key=utils.takefitness, reverse=True)
    return 1


def crossandedu(args):
    solutions = []
    possol = args[0]
    negsol = args[1]
    p = args[2]
    son = crossover(possol, negsol, p)
    son.educate(p)
    if son.feas:
        solutions.append(son)
    else:
        solutions.append(son)
        if random.random() < p.Prep:
            newson = copy.deepcopy(son)
            newson.penality *= 10
            newson.recomputecost(p)
            newson.educate(p)
            solutions.append(newson)
            if not newson.feas:
                newnewson = copy.deepcopy(newson)
                newnewson.penality *= 10
                newnewson.recomputecost(p)
                newnewson.educate(p)
                solutions.append(newnewson)
    return solutions
