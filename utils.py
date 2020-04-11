import collections
import numpy as np
import heapq
import random

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += str(ele)
        str1 += " " 
    
    # return string   
    return str1  
        

def delimiting(sigma):                                                              # Torna delimiters a partire da una sigma
    delimiters = [0]
    start = 0
    for route in sigma:
        start += len(route)
        delimiters.append(start)
    return delimiters

def shortestPath(edges, source, sink):                                              # Algoritmo di Dijkstra
    graph = collections.defaultdict(list)
    for l, r, c in edges:
        graph[l].append((c,r))
    queue, visited = [(0, source, [])], set()
    heapq.heapify(queue)
    while queue:
        (costo, node, path) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            if node == sink:
                return (costo, path)
            for c, neighbour in graph[node]:
                if neighbour not in visited:
                    heapq.heappush(queue, (costo+c, neighbour, path))
    return float("inf")   



def OXcrossover(sol1, sol2, p):                                                        # Crossover tra due soluzioni
    tour1 = sol1.GT[:]
    tour2 = sol2.GT[:]
    
    son1 = list(np.zeros(p.n-1))
    son2 = list(np.zeros(p.n-1))
    start = 2
    end = 1
    while start >= end:
        start = random.randint(0, p.n - 3)
        end = random.randint(0, p.n - 2)
    fixed1 = tour1[start:(end+1)]
    fixed2 = tour2[start:(end+1)]
    son1[start:(end+1)] = fixed1
    son2[start:(end+1)] = fixed2
    j = end + 1
    k = end + 1
    for i in range(end + 1, p.n + start - 1):
        while tour2[j%(p.n-1)] in fixed1:
            j += 1
        while tour1[k%(p.n-1)] in fixed2:
            k += 1
        son1[i%(p.n-1)] = tour2[j%(p.n-1)]
        son2[i%(p.n-1)] = tour1[k%(p.n-1)]
        j += 1
        k += 1
    
    if random.randint(0,1):
        return son1
    else:
        return son2
    
def takesimilarity(sol):
    return sol.sim

def takefitness(sol):
    return sol.fitness

def takecost(sol):
    return sol.costo

def deduplicate(solutions):
    newsolutions = []
    for sol in solutions:
        visited = False
        for othersol in newsolutions:
            if sol.costo == othersol.costo:
                visited = True
                sol.costo = -2
        if not visited and sol.costo != -2:
            newsolutions.append(sol)
    newsolutions.sort(key = takecost)
    return newsolutions

def reverse_sublist(lst,start,end):
    lst[start:end] = lst[start:end][::-1]
    return lst