import random
import numpy as np 
import math

from pandas import array
import matplotlib.pyplot as plt


def fitness_function(position):
    #Modularizando para melhor manutencao da funcao
    seno_raiz = math.sin(math.sqrt(abs((position[0] / 2) + (position[1] + 47))))
    x_seno_raiz = position[0] * (math.sin(math.sqrt(abs(position[0] - (position[1] + 47)))))
    return (-1*(position[1]+47) * seno_raiz) - x_seno_raiz


def random_position():
    #Intervalos designados na especificacao do trabalho
    return [random.uniform(-512, 512),random.uniform(-512, 512)] 

def random_velocidade():
    #Intervalos designados na especificacao do trabalho
    return [random.uniform(-77, 77),random.uniform(-77, 77)]

def update_velocidade(velocidade_atual,Watual, pbest, gbest, posicao, c1, c2):
	x = (Watual * velocidade_atual[0]) + c1 * random.uniform(0,1)*(pbest[0] - posicao[0]) + c2 * random.uniform(0,1)*(gbest[0] - posicao[0])
	y = (Watual * velocidade_atual[1]) + c1 * random.uniform(0,1)*(pbest[1] - posicao[1]) + c2 * random.uniform(0,1)*(gbest[1] - posicao[1])
	
	return [x,y]


def update_posicao(posicao, velocidade):
	x = posicao[0] + velocidade[0]
	y = posicao[1] + velocidade[1]
	
	return [x,y]

def update_w(iteracao, Wmax, Wmin, n_iterations):
	return Wmax - (iteracao*(Wmax-Wmin) / n_iterations)


def run_pso(n_iterations, qtd_particulas):

	#Setup
	Wmax = 15
	Wmin = 1
	Watual = Wmax
	c1 = 2.5
	c2 = 2.5

	#2 - Inicializar aleatoriamente a posicao inicial(x) de cada particula
	posicao_particulas = []
	pbest_fitness_value = []
	vetor_velocidade = []

	#3 - Velocidade inicial(v) para todas as particulas
	velocidade_inicial = random_velocidade()

	for i in range(qtd_particulas):
		posicao_particulas.append(random_position())
		pbest_fitness_value.append(float('inf'))
		vetor_velocidade.append(velocidade_inicial)

	pbest_position = posicao_particulas
	gbest_fitness_value = float('inf')
	gbest_position = [0,0]
	
	all_gbest_iteration = []

	iteration = 0
	while iteration < n_iterations:
		for i in range(qtd_particulas):
			#4 a) - Calculando aptidao de 'p'
			fitness_cadidate = fitness_function(posicao_particulas[i])

			#4 b) - Verificando a melhor posicao de 'p'
			if(pbest_fitness_value[i] > fitness_cadidate):
				pbest_fitness_value[i] = fitness_cadidate
				pbest_position[i] = posicao_particulas[i]

			#5 - Verificando a melhor aptdao da populacao
			if(gbest_fitness_value > fitness_cadidate):
				gbest_fitness_value = fitness_cadidate
				gbest_position = posicao_particulas[i]

		Watual = update_w(iteration, Wmax, Wmin, n_iterations)
		for i in range(qtd_particulas):
			#6 a) - Atualizando velocidade
			nova_velocidade = update_velocidade(vetor_velocidade[i], Watual, pbest_position[i], gbest_position, posicao_particulas[i], c1, c2)
			#Limitando a velocidade x
			if(nova_velocidade[0] < -77):
				nova_velocidade[0] = -77
			elif(nova_velocidade[0] > 77):
				nova_velocidade[0] = 77
			
			#Limitando a velocidade y
			if(nova_velocidade[1] < -77):
				nova_velocidade[1] = -77
			elif(nova_velocidade[1] > 77):
				nova_velocidade[1] = 77

			vetor_velocidade[i] =nova_velocidade
			#6 b) - Atualizando a posicao
			nova_posicao = update_posicao(posicao_particulas[i], vetor_velocidade[i])
			if(nova_posicao[0] < -512):
				nova_posicao[0] = -512
			elif(nova_posicao[0] > 512):
				nova_posicao[0] = 512
			
			if(nova_posicao[1] < -512):
				nova_posicao[1] = -512
			elif(nova_posicao[1] > 512):
				nova_posicao[1] = 512
			
			posicao_particulas[i] =nova_posicao
		
		#Salvar o gbest no array de cata iteracao
		all_gbest_iteration.append(gbest_fitness_value)
		#media_gbest_iteration[iteration] += gbest_fitness_value
		
		#7 - Condicao de terminao nao foi alcancada
		iteration = iteration + 1
	
	#Calcular media de cada iteracao e plotar grafico
	# for i in range(n_iterations):
	# 	media_gbest_iteration[i] = media_gbest_iteration[i] / n_iterations
	
	#Salvar valores do melhor valor da iteracao
	#6 graficos com 2 tracados cada(50 e 100 particulas, media de cada iteracao e qual iteracao encontrei o melhor resultado)
	return [gbest_fitness_value, gbest_position, all_gbest_iteration]


def run(qtd_particulas):
	
	best_result_20 = float('inf')
	media_result_20 = 0
	array_result_20 = []
	media_iteration_20 = [0] * 20

	best_result_50 = float('inf')
	media_result_50 = 0
	array_result_50 = []
	media_iteration_50 = [0] * 50

	best_result_100 = float('inf')
	media_result_100 = 0
	array_result_100 = []
	media_iteration_100 = [0] * 100
	
	qtd_rodadas = 5

	for i in range(qtd_rodadas):
		result_20 = run_pso(20, qtd_particulas)
		result_50 = run_pso(50, qtd_particulas)
		result_100 = run_pso(100, qtd_particulas)

		array_result_20.append(result_20[0])
		array_result_50.append(result_50[0])
		array_result_100.append(result_100[0])

		#Pegando os melhores resultados
		if(result_20[0] < best_result_20):
			best_result_20 = result_20[0]
		
		if(result_50[0] < best_result_50):
			best_result_50 = result_50[0]

		if(result_100[0] < best_result_100):
			best_result_100 = result_100[0]
		
		#Soma para realizar a media
		media_result_20 += result_20[0]
		media_result_50 += result_50[0]
		media_result_100 += result_100[0]

		#Soma para realizar a media das iteracoes
		print(result_20[2])
		print("kelvin")
		for i in range(20):
			media_iteration_20[i] += result_20[2][i]

		for i in range(50):
			media_iteration_50[i] += result_50[2][i]

		for i in range(100):
			media_iteration_100[i] += result_100[2][i]

	#Realizando a media (valor)
	media_result_20 = media_result_20 / qtd_rodadas
	media_result_50 = media_result_50 / qtd_rodadas
	media_result_100 = media_result_100 / qtd_rodadas

	#Realizando a media (iteracao)
	for i in range(20):
		media_iteration_20[i] = media_iteration_20[i] / qtd_rodadas

	for i in range(50):
		media_iteration_50[i] = media_iteration_50[i] / qtd_rodadas

	for i in range(100):
		media_iteration_100[i] = media_iteration_100[i] / qtd_rodadas
	
	print("\n\n")
	print(media_iteration_20)

	# print("Best 20: %f. Media 20: %f" %(best_result_20, media_result_20))
	# print("Best 50: %f. Media 50: %f" %(best_result_50, media_result_50))
	# print("Best 100: %f. Media 100: %f" %(best_result_100, media_result_100))

	# print("\n--Results--")
	# print("20 iterations:\n", array_result_20, "\n")
	# print("50 iterations:\n", array_result_50, "\n")
	# print("100 iterations:\n", array_result_100, "\n")
	
	#x = [1,2,3,4,5,6,7,8,9,10]
	#array_result_20.sort(reverse=True)
	#plt.plot(x, array_result_20)
	#plt.show()
	
	#media_result_20.sort(reverse=True)
	#plt.plot(x, media_result_20)
	#plt.show()
	

def main():
	print("--Resultados para 50 particulas--")
	run(50)
	
	print("--Resultados para 100 particulas--")
	run(100)
main()