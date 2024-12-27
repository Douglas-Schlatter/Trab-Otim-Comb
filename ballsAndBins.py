import Bin
import Solution
import copy
'''A primeira linha do arquivo informa o n´umero de
recipientes (n). A segunda linha do arquivo informa o n´umero de bolas
m. Cada linha a partir da terceira linha do arquivo at´e a linha n + 2
possui dois n´umeros inteiros positivos: o limite inferior do recipiente i
e o limite superior do recipiente i, respectivamente.'''


def SortPerLowerBound(binList):
    if len(binList) > 1:
  
        mid = len(binList)//2
        L = binList[:mid]
        R = binList[mid:]
  
        SortPerLowerBound(L)
        SortPerLowerBound(R)
  
        i = j = k = 0
  
        while i < len(L) and j < len(R):
            if int(L[i].lowerLimit) < int(R[j].lowerLimit):
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
        iValue += iBin.currentValue
    return iValue

#Vizinhança
def Border(solution):

    neighbors = []
    #tagetSolution = copy.deepcopy(solution) # tem que verificar se é uma deep copy msm -> TODO talvez isso custe mto processamento
    tagetISolution =  Solution.Solution(copy.deepcopy(solution.value),copy.deepcopy(solution.bins))
    for iBin in tagetISolution.bins:
        tagetISolution =  Solution.Solution(copy.deepcopy(solution.value),copy.deepcopy(solution.bins)) # reseta solutuion copy
        if(Bin.IsValidToTake(iBin)):
            #gera solution
            oldIBinValue = iBin.currentValue
            for jBin in tagetISolution.bins: 
                tagetISolution =  Solution.Solution(copy.deepcopy(solution.value),copy.deepcopy(solution.bins)) # reseta solutuion copy
                if(jBin.id == iBin.id):# se eles têm o mesmo id, n faz mto sentido tu tirar e colocar no mesmo bin
                    #Não gera solução
                    pass
                elif(Bin.IsValidToPut(jBin)):
                    #Gera Solution
                    newIBinValue = Bin.SetBalls(iBin,(iBin.numberOfBalls-1))
                    #Diferença entre antes de tirar e dps de tirar a bola
                    diffIBinValue = abs(oldIBinValue - newIBinValue)

                    oldJBinValue = jBin.currentValue
                    newJBinValue = Bin.SetBalls(jBin,(jBin.numberOfBalls+1))

                    diffJBinValue = abs(newJBinValue - oldJBinValue)

                    tagetISolution.value = solution.value - diffIBinValue + diffJBinValue # direnfeça de colocar aquela 
                    neighbors.append(targetSolution)
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
def CalculateFistSol():
    return 0 

def BuscaLocal(solucao):
    bestValor = CalculateSolValue(solucao)
    bestSol = solucao
    
    melhorou = True
    while(melhorou):
        melhorou = False
        for vizinho in Border(solucao):
            solVizinho = CalculateSolValue(vizinho) # Isso é oq não é pra fazer, recalcular a solução toda!!!
            if solVizinho > bestValor:
                bestValor = solVizinho
                bestSol = vizinho
                melhorou = True
                #break # First ou best improvement?
    return bestSol


# Open the file in read mode
file = open('./inf05010_2024-2_B_TP_instances_bins-and-balls/01.txt', 'r')
lines = file.readlines()

#Lista de bins contendo um index, lower bound e upper bound
currentBinList = []

# Read each line in the file
numBins = lines[0]
numBalls = lines[1]
for index in range(2,len(lines)):
    #print(index)
    #print (lines[index])
    targetLine=lines[index].split(" ")
    targetBin = Bin.Bin((index-1),int(targetLine[0]),int(targetLine[1]))
    Bin.SetBalls(targetBin,100)
    currentBinList.append(targetBin)
targetSolution = Solution.Solution(CalculateSolValue(currentBinList),currentBinList)
   #print(targetBin.id, " ",targetBin.lowerLimit)

#sortedList = SortPerLowerBound(currentBinList)
print("TargetSolution")
for iBin in targetSolution.bins:
     print(iBin.id, " ",iBin.numberOfBalls,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin

print(" ")
print("Vizinhos")
vizinhos = Border(targetSolution)
for i in range(0,len(vizinhos)):
    print(" ")
    print("Sol ", i)
    for iBin in vizinhos[i].bins:
        print(iBin.id, " ",iBin.numberOfBalls,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
'''
#for iBin in sortedList:
for iBin in targetSolution.bins:
    print(iBin.id, " ",iBin.lowerLimit)
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
#print(CalculateSolValue(currentBinList))    
'''
    