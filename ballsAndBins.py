import Bin
'''A primeira linha do arquivo informa o n´umero de
recipientes (n). A segunda linha do arquivo informa o n´umero de bolas
m. Cada linha a partir da terceira linha do arquivo at´e a linha n + 2
possui dois n´umeros inteiros positivos: o limite inferior do recipiente i
e o limite superior do recipiente i, respectivamente.'''

def CalculateSolValue(solucao):
    iValue = 0
    for iBin in solucao:
        iValue += iBin.currentValue
    return iValue

def vizinhanca(solucao):
    vizinhos = []

    # calculo da vizinhança

    return vizinhos

def BuscaLocal(solucao):
    bestValor = CalculateSolValue(solucao)
    bestSol = solucao
    
    melhorou = True
    while(melhorou):
        melhorou = False
        for vizinho in vizinhanca(solucao):
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
targetSolucao = []

# Read each line in the file
numBins = lines[0]
numBalls = lines[1]
for index in range(2,len(lines)):
    #print(index)
    #print (lines[index])
    targetLine=lines[index].split(" ")
    targetBin = Bin.Bin((index-1),targetLine[0],targetLine[1])
    Bin.setBalls(targetBin,2)
    targetSolucao.append(targetBin)
   #print(targetBin.id, " ",targetBin.lowerLimit)
        
for iBin in targetSolucao:
    print(iBin.id, " ",iBin.lowerLimit)
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
print(CalculateSolValue(targetSolucao))    
    