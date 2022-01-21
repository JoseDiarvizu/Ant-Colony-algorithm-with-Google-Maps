import numpy as np
import matplotlib.pyplot as plt

def print_solution(X,Y,ant): 
    nnodes = len(ant) 
    plt.figure() 
    plt.scatter(X,Y) 
    for n,node in enumerate(ant): 
        node2 = ant[n+1] if n+1< len(ant) else ant[0] 
        plt.plot( [X[node],X[node2]], [Y[node],Y[node2]] ) 
    plt.scatter(X,Y) 
    plt.show()


def generate_ants(nodes):
  antPopulation = np.zeros((nodes,nodes))
  antPopulation[:,0] = 0#np.random.choice(nodes,nodes,replace=False)
  return antPopulation


def move_ant(ant,mFeromonas,mInvertida):
  n = len(ant)
  visited = np.zeros_like(ant)
  visited[ant[0]] = 1

  currentNode = ant[0]

  for i in range(1,n):
    notVisited = np.where(visited!=1)[0]
    calc = np.array(mFeromonas[currentNode,notVisited] * mInvertida[currentNode,notVisited]**2)
    pr = calc/np.sum(calc)
    currentNode = np.random.choice(notVisited,p=pr)
    ant[i] = currentNode
    visited[currentNode] = 1

  return ant


def get_distance(ant,mdistances):
  distance = 0
  n = len(ant)
  for i in range(n-1):
    distance+=mdistances[ant[i]][ant[i+1]]
  distance+=mdistances[ant[0]][ant[-1]]
  return distance


def ant_colony(nodes,generations,X,Y,mdistances,Q=10,Ro=0.3,early_stopping_generations=10):
  mFeromonas = np.ones_like(mdistances)
  mInvertida = np.zeros_like(mdistances)

  for i in range(nodes):
    for j in range(nodes):
      if i!=j:
        mInvertida[i][j] = 1/mdistances[i][j]

  elite = 0
  eliteFit = 9999999
  max_dist = np.max(mdistances)
  earlystopping_rounds = 0
  for i in range(generations):
    mFeromonas = (1-Ro) * mFeromonas 
    ants = np.copy(generate_ants(nodes))
    ants = [move_ant(ants[k].astype(int),mFeromonas,mInvertida) for k in range(nodes)]
    for j in range(nodes):
      distance = get_distance(ants[j].astype(int),mdistances)
      if distance < eliteFit:
        earlystopping_rounds = 0
        elite = np.copy(ants[j])
        eliteFit = distance
        print('I: ',i)
        print_solution(X,Y,elite.astype(int))
        print(eliteFit)
      earlystopping_rounds += 1
      Q = max_dist * nodes
      for k in range(nodes-1):
        mFeromonas[int(ants[j][k])][int(ants[j][k+1])] += (Q/distance)
        mFeromonas[int(ants[j][k+1])][int(ants[j][k])] += (Q/distance)
    if earlystopping_rounds >= nodes*early_stopping_generations:
      break
      
  return elite,eliteFit


