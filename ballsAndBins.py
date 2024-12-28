import Bin
import Solution
import copy
'''A primeira linha do arquivo informa o n´umero de
recipientes (n). A segunda linha do arquivo informa o n´umero de bolas
m. Cada linha a partir da terceira linha do arquivo at´e a linha n + 2
possui dois n´umeros inteiros positivos: o limite inferior do recipiente i
e o limite superior do recipiente i, respectivamente.'''

#Dicionário de bins, chave = id, contem tupla (lower bound e upper bound)
binDict = {}

def SortPerLowerBound(binList):
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

def CalculateSolValue(solucao):
    iValue = 0
    for iBin in solucao:
        iValue += iBin[0]
    return iValue

def CalculateBinValue(balls):
    return int((balls*(balls+1))/2)

#Vizinhança
def Border(solution, listSolution):

    neighbors = []
    #tagetSolution = copy.deepcopy(solution) # tem que verificar se é uma deep copy msm -> TODO talvez isso custe mto processamento
    targetSolution =  Solution.Solution(solution.value,listSolution.copy())

    # iBin[0] = valor
    # iBin[1] = número de bolas
    # iBin[2] = id
    for iBin in targetSolution.bins:
        #targetISolution = Solution.Solution(solution.value,listSolution.copy()) # reseta solution copy
        # Se número de bolas for maior que o mínimo do bin desse id
        if(iBin[1] > binDict[iBin[2]][0]):
            #gera solution
            for jBin in targetSolution.bins: 
                #targetISolution = Solution.Solution(solution.value,listSolution.copy()) # reseta solution copy
                if(jBin[2] == iBin[2]):# se eles têm o mesmo id, n faz mto sentido tu tirar e colocar no mesmo bin
                    #Não gera solução
                    continue
                 # Se número de bolas for menor que o máximo do bin desse id
                elif(jBin[1] < binDict[jBin[2]][1]):
                    #Gera Solution

                    newSol = listSolution.copy()

                    newSol.remove(iBin)
                    newSol.remove(jBin)
                    newBin = (CalculateBinValue(iBin[1]-1), iBin[1]-1, iBin[2])
                    newBin2 = (CalculateBinValue(jBin[1]+1), jBin[1]+1, jBin[2])
                    newSol.append(newBin)
                    newSol.append(newBin2)

                    targetISolution = Solution.Solution(solution.value - iBin[1] - 1 + jBin[1], newSol) # direnfeça de colocar aquela 
                    targetISolution.bins = newSol
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
def CalculateFirstSol(sortedList, numBalls, currentBalls):

    initialSol = sortedList
    # Quantas bolas faltam serem adicionadas
    missingBalls = numBalls - currentBalls
    while(missingBalls > 0):
        for bin in sortedList:
            # Quantidade de bolas adicionadas é igual o máximo - atual
            value = binDict[bin[2]] [1] - bin[1]
            # Se o máximo - atual > 0, então pode adicionar
            if (value > 0):
                # Se value for menor que missingBalls, pode adicionar todas
                if (value <= missingBalls):
                    initialSol.remove(bin)
                    missingBalls -= value
                    bin = (CalculateBinValue(binDict[bin[2]] [1]), binDict[bin[2]] [1], bin[2])
                    initialSol.append(bin)

                else:
                    initialSol.remove(bin)
                    # Se value for menor que missingBalls, pode adicionar só a diferença
                    addedBalls = bin[1] + missingBalls
                    missingBalls -= missingBalls
                    bin = (CalculateBinValue(addedBalls), addedBalls, bin[2])
                    initialSol.append(bin)
                    break

    return Solution.Solution(CalculateSolValue(initialSol), initialSol)

def BuscaLocal(solucao):
    bestValue = solucao.value
    bestSol = solucao
    
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


# Open the file in read mode
file = open('./inf05010_2024-2_B_TP_instances_bins-and-balls/01.txt', 'r')
lines = file.readlines()

#Lista de bins contendo um index, lower bound e upper bound
currentBinList = []

#Dicionário de bins, chave = id, contem tupla (lower bound e upper bound)
#binDict = {}   #Declarado la em cima pra ser global

#Lista da solução atual contendo tupla com (valor do bin, bolas no bin, id do bin)
currentSolList = []

# Read each line in the file
numBins = int(lines[0])
numBalls = int(lines[1])

# Quantas bolas foram colocadas em cada bin (o mínimo)
currentBalls = 0
for index in range(2,len(lines)):
    #print(index)
    #print (lines[index])
    targetLine=lines[index].split(" ")
    targetBin = Bin.Bin((index-1),int(targetLine[0]),int(targetLine[1]))
    binDict[(index-1)] = (int(targetLine[0]),int(targetLine[1]))
    #Bin.SetBalls(targetBin,100)
    currentBinList.append(targetBin)
    teste = int(targetLine[0])
    currentBalls += teste
    currentSolList.append((int(teste*(teste+1)/2), teste, (index-1)))

sortedList = SortPerLowerBound(currentSolList)

targetSolution = CalculateFirstSol(sortedList, numBalls, currentBalls)

   #print(targetBin.id, " ",targetBin.lowerLimit)

print("TargetSolution")
for bin in targetSolution.bins:
     print(bin[2], " ",bin,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print(targetSolution.value)

print(" ")

buscaLocal = BuscaLocal(targetSolution)

print("BuscaLocal valor")
for bin in buscaLocal.bins:
     print(bin[2], " ",bin,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print(buscaLocal.value)

'''
print("Vizinhos")
vizinhos = Border(targetSolution, sortedList)
for i in range(0,len(vizinhos)):
    print(" ")
    print("Sol ", i)
    for iBin in vizinhos[i].bins:
        print("(",iBin[2], ",",iBin[1], ")",end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print(len(vizinhos))
#for iBin in sortedList:
for iBin in targetSolution.bins:
    print(iBin.id, " ",iBin.lowerLimit)
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
#print(CalculateSolValue(currentBinList))    
'''
    