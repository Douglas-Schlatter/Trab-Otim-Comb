# Determinar quantas bolas ser˜ao depositadas em cada recipiente (n˜ao
# pode restar nenhuma bola fora dos recipientes), de forma a maximizar
# o lucro total, enquanto respeitando as restrições de quantidade mínima
# e máxima de cada recipiente. O lucro é calculado da seguinte forma: se
# há uma bola em um recipiente, o valor é 1, se há 2, é 1 + 2, se há 3, é 1
# + 2 + 3, e assim por diante (i.e., (n(n + 1))/2). (Observação: a forma
# mais imediata de calcular essa função objetivo é não-linear e, portanto,
# não pode ser utilizada diretamente na formulação.) Uma solução só é
# válida se a quantidade de bolas dentro do recipiente i fica entre li e ui
# (ambos valores incluídos, ou seja, se li = 3 e ui = 10, a quantidade de
# bolas em i pode ser 3, 10, ou qualquer valor intermediário).

import Pkg
Pkg.activate(@__DIR__)
Pkg.instantiate()

using JuMP
using HiGHS

function main()
	m = Model(HiGHS.Optimizer)
	
	###############################
	#     Leitura do arquivo      #
	###############################
	
	file = open(ARGS[1], "r")
	
	binsTotal = parse(Int, readline(file))
	ballsTotal = parse(Int, readline(file))
	
	bin = zeros(Int32, binsTotal, 2)

	
	for i in 1:binsTotal
		(min, max) = split(readline(file), " ")
		bin[i,1] = parse(Int,min)
		bin[i,2] = parse(Int,max)
		#print(bin[i,:], "\n")
	end
	
	###############################
	#         Formulação          #
	###############################
	
	maxSize = maximum(bin[:,2])
	
	@variable(m, x[1:binsTotal] >= 0, Int)	# Quantas bolas tem em cada bin
	@variable(m, y_mais[i=1:binsTotal,1:bin[i,2]] >= 0, Int)	# Parte positiva de x[i] - j em que i é o bin e j é valor de 1 a valor máximo do bin i
	@variable(m, y_menos[i=1:binsTotal,1:bin[i,2]] >= 0, Int)	# Parte negativa de x[i] - j em que i é o bin e j é valor de 1 a valor máximo do bin i
	@variable(m, z[i=1:binsTotal,1:bin[i,2]] >= 0, Bin)			# Bool para controle do y
	
	@constraint(m, sum(x) == ballsTotal)		# Toda bola precisa estar em um bin
	
	@constraint(m, [i=1:binsTotal], x[i] >= bin[i,1])	# Cada bin precisa ser maior que o mínimo
	@constraint(m, [i=1:binsTotal], x[i] <= bin[i,2])	# Cada bin precisa ser menor que o máximo
	
	# Fazendo x[i] - j para todo valor que o bin possa ter, a parte positiva vai ser o objetivo
	# Como x = j também é válido, adicionar um -1 pra y_mais precisar de um valor a mais
	@constraint(m, [i=1:binsTotal, j=1:(bin[i,2])], x[i]-j == y_mais[i,j] - y_menos[i,j]-1)
	
	
	# Essas restrições garantem que y_mais = 0 ou y_menos = 0
	# Usando a variável z para escolher uma das restrições
	@constraint(m, [i=1:binsTotal, j=1:(bin[i,2])], y_mais[i,j] <= 0 + z[i,j]*bin[i,2])		
	@constraint(m, [i=1:binsTotal, j=1:(bin[i,2])], y_menos[i,j] <= 0 + (1-z[i,j])*bin[i,2])

	@objective(m, Max, sum(y_mais[i,j] for i=1:binsTotal, j=1:bin[i,2]))
	
	optimize!(m)
	@show objective_value(m)
	@show value.(x)
	#@show value.(y_mais)
	#@show value.(y_menos)
	#@show value(sum(y_mais))
	
	
	
end

main() # comentar aqui se for executar no terminal Julia

