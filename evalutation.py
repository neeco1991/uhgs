def cost(route, p, penality):
    tot = 0
    carico = 0
    feasible = True
    for i in range(len(route) - 1):
        tot += p.dist[route[i]][route[i+1]]
        carico += p.demand[route[i]]
    if carico > p.C:
        feasible = False
        tot += (carico - p.C)*penality
    return feasible, tot


def evalNWithDepot(sigmaLista):
    sigmaList = []
    for i in range(len(sigmaLista)):
        route = sigmaLista[i][:]
        route.append(0)
        route.insert(0, 0)
        sigmaList.append(route)
    return evalN(sigmaList)


def costWithDepot(r, p, penality):
    try:
        tot = p.dist[0][r[0]] + p.dist[0][r[len(r) - 1]]
    except:
        return True, 0
    feasible = True
    carico = 0
    for i in range(len(r) - 1):
        tot += p.dist[r[i]][r[i+1]]
        carico += p.demand[r[i]]
    carico += p.demand[r[len(r) - 1]]
    if carico > p.C:
        feasible = False
        tot += (carico - p.C)*penality
    return tot


def costWithDepot2(r, p, penality):
    try:
        tot = p.dist[0][r[0]] + p.dist[0][r[len(r) - 1]]
    except:
        return True, 0
    feasible = True
    carico = 0
    for i in range(len(r) - 1):
        tot += p.dist[r[i]][r[i+1]]
        carico += p.demand[r[i]]
    carico += p.demand[r[len(r) - 1]]
    if carico > p.C:
        feasible = False
        tot += (carico - p.C)*penality
    return feasible, tot
