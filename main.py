import random
import numpy as np 
import math


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

def update_velocidade(velocidade_atual,Watual, pbest, gbest, posicao):
	x = (Watual * velocidade_atual[0]) + c1 * random.uniform(0,1)*(pbest[0] - posicao[0]) + c2 * random.uniform(0,1)*(gbest[0] - posicao[0])
	y = (Watual * velocidade_atual[1]) + c1 * random.uniform(0,1)*(pbest[1] - posicao[1]) + c2 * random.uniform(0,1)*(gbest[1] - posicao[1])
	
	return [x,y]


def update_posicao(posicao, velocidade):
	x = posicao[0] + velocidade[0]
	y = posicao[1] + velocidade[1]
	
	return [x,y]

def update_w(iteracao):
	return Wmax - (iteracao*(Wmax-Wmin) / n_iterations)
    
#Setup
Wmax = 15
Wmin = 1
Watual = Wmax
c1 = 1
c2 = 1.5

#Quantidade de iteracoes vai variar conforme testes
n_iterations = 1000

#1 - Determinar o numero de particulas P da populacao
qtd_particulas = 30

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
			print(gbest_position)

	Watual = update_w(iteration)
	for i in range(qtd_particulas):
		#6 a) - Atualizando velocidade
		nova_velocidade = update_velocidade(vetor_velocidade[i], Watual, pbest_position[i], gbest_position, posicao_particulas[i])
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
	
	#7 - Condicao de terminao nao foi alcancada
	iteration = iteration + 1

print("Posicao GBEST: ", gbest_position, "Valor: ", gbest_fitness_value)