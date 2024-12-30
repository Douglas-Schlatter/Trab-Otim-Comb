import Bin
import Solution
from collections import deque 
import time
'''
Problema balls and bins solucionado por Late Acceptence Hill Climbing com best improvement

Nomes:ANGELO  OLIVEIRA (550162), DOUGLAS  SCHLATTER(332849) e MATHEUS  FONSECA(332800)

'''

#Dicionário de bins, chave = id, contem tupla (lower bound e upper bound)
binDict = {}

#Coloque como input o nome do arquivo sem .txt
#exemplo 01
fileName = input("Nome do arquivo?: ")


file = open(f'./inf05010_2024-2_B_TP_instances_bins-and-balls/{fileName}.txt', 'r') 

#Fazemos o ordenamento no momento do calculo da solucao inicial
def SortPerLowerBound(binList: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    if len(binList) > 1:
  
        mid = len(binList)//2
        L = binList[:mid]
        R = binList[mid:]
  
        SortPerLowerBound(L)
        SortPerLowerBound(R)
  
        i = j = k = 0
  
        while i < len(L) and j < len(R):
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

#Abaixo funcao que calcula a vizinhanca dada uma instancia de solucao
def Border(solution: Solution, listSolution: list[tuple[int, int, int]]) -> list[Solution]:

    neighbors = []
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

#Usada para comparações com a heuristica
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
                
    return bestSol


#Função utilizada no print a cada melhor solução e tambem na solução inicial
def printOnNewBestSolution(isFirstSol,currentTime,numIteracoes,newBestSol: Solution,):
    #Se sim, eh a solução inicial
    print("")
    if(isFirstSol):
        print("Abaixo dados sobre a solucao inicial: ")
        print("Tempo Atual no momento do calculo da solução inicial: {:.2f}".format(currentTime))
        #print("Iteracao atual no momento do calculo da solução inicial: ")
    #Se não, encontrou uma solução melhor e precisamos printar
    else:
        print("Abaixo dados sobre a melhor solucao encontrada: ")
        print("Tempo Atual no momento da melhoria: {:.2f}".format(currentTime))
        print("Quantidade total de iteracoes no momento da melhoria: ",numIteracoes)
    
    print("Valor da solucao atual: ", newBestSol.value)
    print("Representacao da solucao melhor atual: ")
    print("|id, Quantidade de Bolas no bin| ")
    print("|",end = "")
    for bin in newBestSol.bins:
     #print(bin[2],",",bin[1],end='| ')
     print(f"{bin[2]},{bin[1]}",end="|")
    print("")


lines = file.readlines()



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
    targetLine=lines[index].split(" ")
    targetBin = Bin.Bin((index-1),int(targetLine[0]),int(targetLine[1]))
    binDict[(index-1)] = (int(targetLine[0]),int(targetLine[1]))
    minBalls = int(targetLine[0])   # Adiciona quantidade de bolas mínimas ao bin para ser válido
    currentBalls += minBalls
    currentSolList.append((0, minBalls, (index-1)))

#Antes de Começar a contagem do tempo o usuario deve inserir os parametros de execução

#Tamanho do Heap que guarda as melhores valores de solução
sizeOfAcceptHeap= int(input("Qual sera o tamanho do queue de aceitacao do LAHC?: "))

#Tamanho do Heap que guarda as melhores valores de solução
stopAtInteration = int(input("Qual sera a quantidade maxima de iteracoes sem melhoria?: "))

#Relacionado a tempo
timeLimit = int(input("Qual sera o tempo maximo?: "))

#Inicio da contagem de tempo do programa, decidimos colocar aqui, pois aqui que a meta-heuristica começa de fato
timeStart = time.time()
sortedList = SortPerLowerBound(currentSolList)
initialSolution = CalculateFirstSol(sortedList, numBalls, currentBalls)

timeSolInicial = time.time()-timeStart

#Print da solucao inicial
printOnNewBestSolution(True,timeSolInicial,0,initialSolution)
'''
#Codigo antigo para print da solucao inicial
print("initialSolution")
for bin in initialSolution.bins:
     print(bin,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print(initialSolution.value)

print(" ")
'''
#Antes estavamos executando a buscaLocal para comparar com nossa heuristica
'''
buscaLocal = BuscaLocal(initialSolution)

print("BuscaLocal valor")
#for bin in buscaLocal.bins:
#     print(bin,end='| ')
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print("")
print("busca local: ", buscaLocal.value)
print("valor real: ", CalculateSolValue(buscaLocal.bins))
'''



#Abaixo esta a implementação do Late Acceptance Hill Climbing

#Preparação do Heap do LAHC e Melhor solução
acceptenceQueue = deque()
#Copiamos os valores apartir das solução inicial gerada
bestSolution = initialSolution
bestSolValue = initialSolution.value
acceptenceQueue.append(bestSolValue)
#Colocamos a solução inicial como a solução que procuraremos a primeira vizinhança
targetSolution = Solution.Solution(bestSolution.value,bestSolution.bins.copy())

#Relacionado as iterações -> Estamos fazendo a logica de x iterações sem melhora
interatorCount = 0
lastIterationImprovement = 0
while(((interatorCount-lastIterationImprovement)<stopAtInteration) and ((time.time()-timeStart)<timeLimit)):
    #Busca local com alteracoes
    for vizinho in Border(targetSolution, targetSolution.bins):
            #Ta sobrando espaço = so adicionar
        if((acceptenceQueue[-1] <= vizinho.value) or (vizinho.value >= targetSolution.value)):
            #se o tamanho da deque esta no maximo
            if(len(acceptenceQueue) == sizeOfAcceptHeap):
                #de pop na ultima solucao adicionada
                acceptenceQueue.pop()
            #Adicione a nova solucao a esquerda
            acceptenceQueue.appendleft(vizinho.value)
            #caminhe para a nova solucao
            targetSolution = Solution.Solution(vizinho.value,vizinho.bins.copy())
            #Se a solucao do vizinho eh melhor que a solucao global
            if(bestSolValue<vizinho.value):
                #Atualiza a solucao global e printa as informacoes necessarias
                bestSolution = Solution.Solution(vizinho.value,vizinho.bins.copy())
                bestSolValue = bestSolution.value
                printOnNewBestSolution(False,time.time()-timeStart, interatorCount, bestSolution)
                lastIterationImprovement = interatorCount
    interatorCount+=1
timeAtStopExecution = time.time()
print("")

print("--------------------------Programa Chegou ao fim da execução-----------------------------")
#Abaixo alguns prints monstrando qual foi o motivo da parada
if(((interatorCount-lastIterationImprovement)>=stopAtInteration)):#Parada por limite de iterações sem melhora
    print("Parada ocorreu por que chegamos na quantidade maxima de iteração sem melhora")
elif((time.time()-timeStart)>=timeLimit):# Parada por limite de tempo 
    print("Parada ocorreu por que chegamos no tempo maximo de execução")

print(f"Arquivo: {fileName}", f"TamanhoMaxQueue: {sizeOfAcceptHeap}", f"Tempo: {timeLimit}", f"Max Interações sem melhoria: {stopAtInteration}")

print("Quantidade de iteracoes sem melhoria: ",(interatorCount-lastIterationImprovement)," Total de Iteracoes Atingida: ",(interatorCount))
print("Tempo Maximo:",timeLimit," Tempo total: ",f"{timeAtStopExecution-timeStart:.2f}")




#Print da solucao inicial:
printOnNewBestSolution(True,timeSolInicial,0,initialSolution)
#Print da melhor solução encontrada:
printOnNewBestSolution(False,timeAtStopExecution-timeStart,lastIterationImprovement,bestSolution)
'''#prints antigos de fim de programa

    print("")
print("Initial Sol Value: ",initialSolution.value)
print("Best Sol Value: ",bestSolution.value)
print("bestSolution")
for bin in bestSolution.bins:
     print(bin,end='| ')
#Comparação com busca local
#print("busca local: ", buscaLocal.value)
'''




    