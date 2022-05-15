import random
import math
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

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


#Dada o numero de iteracoes e a quantidade de particulas, execute!
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

	#Atribuindo valores iniciais para pbest e gbest
	pbest_position = posicao_particulas
	gbest_fitness_value = float('inf')
	gbest_position = [0,0]
	all_gbest_iteration = []

	#Loop principal, ele que determina quando o algoritmo para
	iteration = 0
	while iteration < n_iterations:
		#Para cada particula, calculo sua fitness
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

		#atualizo W para randomizar a posicao das particulas
		Watual = update_w(iteration, Wmax, Wmin, n_iterations)
		#Para cada particula, atualizo a sua velocidade (tomando cuidado com dominio)
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
		
		#7 - Condicao de terminao nao foi alcancada
		iteration = iteration + 1
	
	return [gbest_fitness_value, gbest_position, all_gbest_iteration]



#Funcao para salvar os resultados obtidos a partir de determinada execucao
def save_graph(x, media, best, leg):
	plt.plot(x, media, label = "Media")
	plt.plot(x, best, label = "Best Result")
	plt.title(leg)
	plt.xlabel("Iteração")
	plt.ylabel("Gbest")
	plt.legend()
	plt.savefig("plot_graphs/%s.png" %leg)
	plt.close()


#Calculo do desvido padrao
def desvio_padrao(lista, media):
	result = 0
	for i in range(len(lista)):
		result += (lista[i] - media) ** 2
	#Dividindo os termos
	result = result / len(lista)

	#Tirando a raiz
	result = result ** 0.5
	return result

#Dada a quantidade de particulas, execute!
#Essa funcao
def run(qtd_particulas):
	
	#Valor, posicao e lista de Gbest da respectiva iteracao
	best_result_20 = [float('inf'), [0,0], []]
	media_result_20 = 0
	array_result_20 = []
	media_iteration_20 = [0] * 20

	best_result_50 = [float('inf'), [0,0], []]
	media_result_50 = 0
	array_result_50 = []
	media_iteration_50 = [0] * 50

	best_result_100 = [float('inf'), [0,0], []]
	media_result_100 = 0
	array_result_100 = []
	media_iteration_100 = [0] * 100
	
	qtd_rodadas = 10

	for i in range(qtd_rodadas):
		result_20 = run_pso(20, qtd_particulas)
		result_50 = run_pso(50, qtd_particulas)
		result_100 = run_pso(100, qtd_particulas)

		array_result_20.append(result_20[0])
		array_result_50.append(result_50[0])
		array_result_100.append(result_100[0])

		#Pegando os melhores resultados
		if(result_20[0] < best_result_20[0]):
			best_result_20 = result_20
		
		if(result_50[0] < best_result_50[0]):
			best_result_50 = result_50

		if(result_100[0] < best_result_100[0]):
			best_result_100 = result_100
		
		#Soma para realizar a media
		media_result_20 += result_20[0]
		media_result_50 += result_50[0]
		media_result_100 += result_100[0]

		#Soma para realizar a media das iteracoes
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

	#Desvio padrao
	desvio_20 = desvio_padrao(array_result_20, media_result_20)
	desvio_50 = desvio_padrao(array_result_50, media_result_50)
	desvio_100 = desvio_padrao(array_result_100, media_result_100)

	#Realizando a media (iteracao)
	for i in range(20):
		media_iteration_20[i] = media_iteration_20[i] / qtd_rodadas

	for i in range(50):
		media_iteration_50[i] = media_iteration_50[i] / qtd_rodadas

	for i in range(100):
		media_iteration_100[i] = media_iteration_100[i] / qtd_rodadas
	
	#Salvando os graficos
	legenda = str(qtd_particulas)  + ' particulas . 20 iteracoes'
	save_graph([x for x in range(20)], media_iteration_20, best_result_20[2], legenda)

	legenda = str(qtd_particulas)  + ' particulas . 50 iteracoes'
	save_graph([x for x in range(50)], media_iteration_50, best_result_50[2], legenda)

	legenda = str(qtd_particulas)  + '_particulas_100_iteracoes'
	save_graph([x for x in range(100)], media_iteration_100, best_result_100[2], legenda)

	#Criando e salvando os valores em planilhas
	dic_20 = {}
	dic_50 = {}
	dic_100 = {}

	dic_20["resultados"] = array_result_20
	dic_20["best_result"] = [best_result_20[0]]
	dic_20["media"] = [media_result_20]
	dic_20["desvio_padrao"] = [desvio_20]

	dic_50["resultados"] = array_result_50
	dic_50["best_result"] = [best_result_50[0]]
	dic_50["media"] = [media_result_50]
	dic_50["desvio_padrao"] = [desvio_50]

	dic_100["resultados"] = array_result_100
	dic_100["best_result"] = [best_result_100[0]]
	dic_100["media"] = [media_result_100]
	dic_100["desvio_padrao"] = [desvio_100]

	df = pd.DataFrame.from_dict(dic_20, orient='index')
	df = (df.T)
	df.to_excel("result_planilhas/%s_particulas_20_iteracoes.xlsx" %str(qtd_particulas))

	df = pd.DataFrame.from_dict(dic_50, orient='index')
	df = (df.T)
	df.to_excel("result_planilhas/%s_particulas_50_iteracoes.xlsx" %str(qtd_particulas))

	df = pd.DataFrame.from_dict(dic_100, orient='index')
	df = (df.T)
	df.to_excel("result_planilhas/%s_particulas_100_iteracoes.xlsx" %str(qtd_particulas))

def main():
	#Criando pasta "plot_graphs" se nao existir
	path = Path("plot_graphs")
	path.mkdir(exist_ok=True)

	#Criando pasta "result_planilhas" se nao existir
	path = Path("result_planilhas")
	path.mkdir(exist_ok=True)

	#Para 50 particulas
	run(50)
	
	#Para 100 particulas]
	run(100)
	print(">> Checar pasta: plot_graphs")
	print(">> Checar pasta: result_planilhas")
main()