# Determinar quantas bolas serão depositadas em cada recipiente (não
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
	
	@variable(m, x[i=1:binsTotal,1:bin[i,2]] >= 0, Bin)	# X[i,j] = 1 se o bin i na posição j tem bola
	
	@constraint(m, sum(x) == ballsTotal)		# Toda bola precisa estar em um bin
	
	@constraint(m, [i=1:binsTotal], x[i,bin[i,1]] == 1)	# Cada bin precisa ser maior que o mínimo (O bin mínimo precisa ser 1)
	#@constraint(m, [i=1:binsTotal], x[i,(bin[i,2] + 1)] == 0)	# Cada bin precisa ser menor que o máximo (Só tem X até o máximo, acho que não precisa)
	
	# se X[i+1] = 1 então x[i] = 1
	# x[i+1] -> x[i]
	@constraint(m, [i=1:binsTotal, j=2:bin[i,2]], x[i,j] <= x[i,(j-1)])
	
	@objective(m, Max, sum(x[i,j] * j for i in 1:binsTotal, j in 1:bin[i,2]))
	
	optimize!(m)
	@show objective_value(m)
	for i in 1:binsTotal
		print(i, ": ");
		@show value(sum(x[i,:]));
	end
	
end

main() # comentar aqui se for executar no terminal Julia
