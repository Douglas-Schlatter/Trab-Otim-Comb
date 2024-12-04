import Bin
'''A primeira linha do arquivo informa o n´umero de
recipientes (n). A segunda linha do arquivo informa o n´umero de bolas
m. Cada linha a partir da terceira linha do arquivo at´e a linha n + 2
possui dois n´umeros inteiros positivos: o limite inferior do recipiente i
e o limite superior do recipiente i, respectivamente.'''


# Open the file in read mode
file = open('./inf05010_2024-2_B_TP_instances_bins-and-balls/01.txt', 'r')
lines = file.readlines()
    # Read each line in the file

for index in range(0,len(lines)):
    #print(index)
    #print (lines[index])
    if(index == 0):
        numBins = lines[index]
    elif(index == 1):
        numBalls = lines[index]
    else:
        targetLine=lines[index].split(" ")
        targetBin = Bin.Bin(index,targetLine[0],targetLine[1])
        print(targetBin.id, " ",targetBin.lowerLimit)
        
        #Todo colocar aqui o vetor que guarda o lower e upper de cada bin
        
    