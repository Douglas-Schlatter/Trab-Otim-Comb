import Bin
import Solution
import copy
from collections import deque 
'''A primeira linha do arquivo informa o n´umero de
recipientes (n). A segunda linha do arquivo informa o n´umero de bolas
m. Cada linha a partir da terceira linha do arquivo at´e a linha n + 2
possui dois n´umeros inteiros positivos: o limite inferior do recipiente i
e o limite superior do recipiente i, respectivamente.'''

#Dicionário de bins, chave = id, contem tupla (lower bound e upper bound)
binDict = {}

def SortPerLowerBound(binList: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    if len(binList) > 1:
  
        mid = len(binList)//2
        L = binList[:mid]
        R = binList[mid:]
  
        SortPerLowerBound(L)
        SortPerLowerBound(R)
  
        i = j = k = 0
  
        while i < len(L) and j < len(R):
            # binDict[id] [0] = lowerBound bin id
            # binDict[id] [1] = upperBound bin id
            # L[i] = um bin
            # L[i] [0] = valor, [1] = bolas, [2] = id
            if ((binDict[L[i][2]] [0]) < (binDict[R[j][2]] [0])):
                binList[k] = L[i]
                i += 1
            else:
                binList[k] = R[j]
                j += 1
            k += 1
  
        while i < len(L):
            binList[k] = L[i]
            i += 1
            k += 1
  
        while j < len(R):
            binList[k] = R[j]
            j += 1
            k += 1
  
    return binList

def CalculateSolValue(solucao: list[tuple[int, int, int]]) -> int:
    iValue = 0
    for iBin in solucao:
        iValue += CalculateBinValue(iBin[1])
    return iValue

def CalculateBinValue(balls: int) -> int:
    return int((balls*(balls+1))/2)

#Vizinhança
def Border(solution: Solution, listSolution: list[tuple[int, int, int]]) -> list[Solution]:

    neighbors = []
    #tagetSolution = copy.deepcopy(solution) # tem que verificar se é uma deep copy msm -> TODO talvez isso custe mto processamento
    targetSolution =  Solution.Solution(solution.value,listSolution.copy())

    # iBin[0] = valor
    # iBin[1] = número de bolas
    # iBin[2] = id
    for takenBin in targetSolution.bins:
        #targetISolution = Solution.Solution(solution.value,listSolution.copy()) # reseta solution copy
        # Se número de bolas for maior que o mínimo do bin desse id-> ele eh um bin valido pára pegar
        if(takenBin[1] > binDict[takenBin[2]] [0]):
            #gera solution
            for receiveBin in targetSolution.bins: 
                #targetISolution = Solution.Solution(solution.value,listSolution.copy()) # reseta solution copy
                if(receiveBin[2] == takenBin[2]):# se eles têm o mesmo id, n faz mto sentido tu tirar e colocar no mesmo bin
                    #Não gera solução
                    continue
                 # Se número de bolas for menor que o máximo do bin desse id -> ele eh um bin valido de colocar
                elif(receiveBin[1] < binDict[receiveBin[2]] [1]):
                    #Gera Solution

                    newSol = listSolution.copy()

                    newSol.remove(takenBin)
                    newSol.remove(receiveBin)
                    #newBin = (CalculateBinValue(takenBin[1]-1), takenBin[1]-1, takenBin[2])
                    newBin = (0, takenBin[1]-1, takenBin[2])
                    #newBin2 = (CalculateBinValue(receiveBin[1]+1), receiveBin[1]+1, receiveBin[2])
                    newBin2 = (0, receiveBin[1]+1, receiveBin[2])
                    newSol.append(newBin)
                    newSol.append(newBin2)

                    targetISolution = Solution.Solution(solution.value - takenBin[1] + receiveBin[1]+1, newSol) # direnfeça de colocar aquela 
                    targetISolution.bins = newSol # talvez nao precise pq ja criamos ela com new sol TODO revisar
                    neighbors.append(targetISolution)
                    pass
                else:
                    #Não gera solução
                    pass
        else:
            #Não gera solução
            pass
    # calculo da vizinhança

    return neighbors

#Calcula a primeira solução para ser iterada pelo late hill climbing
    # iBin[0] = valor
    # iBin[1] = número de bolas
    # iBin[2] = id
def CalculateFirstSol(sortedList: list[tuple[int, int, int]], numBalls: int, currentBalls: int) -> Solution:

    initialSol = sortedList # -> talvez aqui valha a pena ser deepcopy por que pode loopar por causa da linha que esta escrito AQUI
    # Quantas bolas faltam serem adicionadas
    missingBalls = numBalls - currentBalls
    while(missingBalls > 0):
        for bin in sortedList:
            # Quantidade de bolas adicionadas é igual o máximo - atual
            value = binDict[bin[2]] [1] - bin[1]
            # Se o máximo - atual > 0, então pode adicionar (ou seja é um bin valido para colocar na nomenclatura antiga)
            if (value > 0):
                # Se value for menor que missingBalls, pode adicionar todas
                if (value <= missingBalls):
                    initialSol.remove(bin)
                    missingBalls -= value
                    #bin = (CalculateBinValue(binDict[bin[2]] [1]), binDict[bin[2]] [1], bin[2])
                    bin = (0, binDict[bin[2]] [1], bin[2])
                    initialSol.append(bin)  #AQUI é readicionado aquele bin a lista

                else:
                    initialSol.remove(bin)
                    # Se value for menor que missingBalls, pode adicionar só a diferença
                    addedBalls = bin[1] + missingBalls
                    missingBalls -= missingBalls # TODO CONFERIR SE NAO ESTAMOS ADICIONANDO BOLAS QUE NAO EXISTEM
                    #bin = (CalculateBinValue(addedBalls), addedBalls, bin[2])
                    bin = (0, addedBalls, bin[2])
                    initialSol.append(bin)
                    break

    return Solution.Solution(CalculateSolValue(initialSol), initialSol)

def BuscaLocal(solucao: Solution) -> Solution:
    bestValue = solucao.value
    bestSol = Solution.Solution(solucao.value,solucao.bins.copy())
    
    melhorou = True
    while(melhorou):
        melhorou = False
        for vizinho in Border(solucao, solucao.bins):
            if vizinho.value > bestValue:
                bestValue = vizinho.value
                bestSol = vizinho
                melhorou = True
                #break # First ou best improvement?
    return bestSol

def LateAcceptanceHillClimbing():
    return 0



# Open the file in read mode
file = open('./inf05010_2024-2_B_TP_instances_bins-and-balls/01.txt', 'r')
lines = file.readlines()

#Lista de bins contendo um index, lower bound e upper bound
#currentBinList = []

#Dicionário de bins, chave = id, contem tupla (lower bound e upper bound)
#binDict = {}   #Declarado la em cima pra ser global

#Lista da solução atual contendo tupla com (valor do bin, bolas no bin, id do bin)
currentSolList = []

# Read each line in the file
numBins = int(lines[0])
numBalls = int(lines[1])

# Quantas bolas que ja foram alocadas em bins (o mínimo para aquele bin ser valido)
currentBalls = 0
for index in range(2,len(lines)):
    #print(index)
    #print (lines[index])
    targetLine=lines[index].split(" ")
    targetBin = Bin.Bin((index-1),int(targetLine[0]),int(targetLine[1]))
    binDict[(index-1)] = (int(targetLine[0]),int(targetLine[1]))
    #Bin.SetBalls(targetBin,100)
    #currentBinList.append(targetBin)
    minBalls = int(targetLine[0])   # Adiciona quantidade de bolas mínimas ao bin para ser válido
    currentBalls += minBalls
    #currentSolList.append((CalculateBinValue(minBalls), minBalls, (index-1)))
    currentSolList.append((0, minBalls, (index-1)))

sortedList = SortPerLowerBound(currentSolList)

initialSolution = CalculateFirstSol(sortedList, numBalls, currentBalls)


print("initialSolution")
for bin in initialSolution.bins:
     print(bin,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print(initialSolution.value)

print(" ")

buscaLocal = BuscaLocal(initialSolution)

print("BuscaLocal valor")
#for bin in buscaLocal.bins:
#     print(bin,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print("")
print("busca local: ", buscaLocal.value)
print("valor real: ", CalculateSolValue(buscaLocal.bins))



# LateAcceptanceHillClimbing
sizeOfAcceptQueue= 4
acceptenceQueue = deque([], maxlen=sizeOfAcceptQueue)
bestSolution = initialSolution
bestSolValue = initialSolution.value
acceptenceQueue.append(bestSolValue)
interatorCount = 0
stopInteration = 10000 # TODO ---> aqui que vai ficar o input para colcocar o criterio de parada
while(interatorCount<stopInteration): #TODO aqui ainda precisa colocar a verificação de tempo
    targetSolution = Solution.Solution(bestSolution.value,bestSolution.bins.copy())
    #Busca local com alteracoes
    melhorou = True
    while(melhorou):
        melhorou = False
        for vizinho in Border(targetSolution, targetSolution.bins):
                #Se a queue ainda não esta cheia -> sim-> so adicione de maneira ordenada
            if(len(acceptenceQueue)<acceptenceQueue.maxlen):
                for i in range(0,len(acceptenceQueue)):
                    #se o que achamos é maior que o valor em i
                    if(vizinho.value>acceptenceQueue[i]):
                        
                        if(i == 0):
                            #se i ==0 estamos no inicio da deque, logo precisamos rotacionar para adicionar a esquerda
                            deque.rotate(1)
                            deque.appendleft(vizinho.value)
                        elif(i ==1):
                            banana=0
            if vizinho.value > bestValue:
                bestValue = vizinho.value
                bestSol = vizinho
                melhorou = True
                #break # First ou best improvement?

    interatorCount+=1

#tem que fazer uma logica para o menor falor sempre ficar num extremo da queue 

'''
print("Vizinhos")
vizinhos = Border(targetSolution, sortedList)
for i in range(0,len(vizinhos)):
    print(" ")
    print("Sol", i, "=", vizinhos[i].value)
    for iBin in vizinhos[i].bins:
        print(f"({iBin[2]})= {iBin[1]}",end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print(len(vizinhos))
#for iBin in sortedList:
for iBin in targetSolution.bins:
    print(iBin.id, " ",iBin.lowerLimit)
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
#print(CalculateSolValue(currentBinList))    
'''
    