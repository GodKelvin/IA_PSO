import random
import numpy as np 
import math

#function that models the problem
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

def update_velocidade(velocidade_atual, pbest, gbest, posicao):
    return (W * velocidade_atual) + c1 * random.uniform(pbest - posicao[0]) + c2 * random.uniforme(gbest - posicao[0])


def update_posicao(posicao, velocidade):
    return posicao[0] + velocidade

    
#Setup
W = 0.5
c1 = 0.5
c2 = 0.9
#target = 1

#Quantidade de iteracoes vai variar conforme testes
n_iterations = 100

#1 - Determinar o numero de particulas P da populacao
qtd_particulas = 30

#2 - Inicializar aleatoriamente a posicao inicial(x) de cada particula
posicao_particulas = np.array([np.array(random_position()) for _ in range(qtd_particulas)])

pbest_position = posicao_particulas
pbest_fitness_value = np.array([float('inf') for _ in range(qtd_particulas)])
gbest_fitness_value = float('inf')
gbest_position = np.array([float('inf'), float('inf')])

#3 - Velocidade inicial(v) para todas as particulas
#AJUSTAR ISSO AQUI / VERIFICAR
velocidade_inicial = random_velocidade()
vetor_velocidade = ([np.array(velocidade_inicial) for _ in range(qtd_particulas)])
#vetor_velocidade = ([np.array([0, 0]) for _ in range(qtd_particulas)])

#RENOMEAR ITERATION
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
    
    for i in range(qtd_particulas):
        #6 a) - Atualizando velocidade
        #nova_velocidade = (W*vetor_velocidade[i]) + (c1*random.random()) * (pbest_position[i] - particulas[i]) + (c2*random.random()) * (gbest_position-particulas[i])
        nova_velocidade = update_velocidade(vetor_velocidade[i], pbest_fitness_value[i], gbest_fitness_value, posicao_particulas[i])
        
        #Limites de 'v(i)'
        if(nova_velocidade < -77):
            nova_velocidade = -77
        elif(nova_velocidade > 77):
            nova_velocidade = 77
        
        vetor_velocidade[i] = nova_velocidade

        nova_posicao = update_posicao(posicao_particulas[i], vetor_velocidade[i])
        posicao_particulas[i] = nova_posicao

    iteration = iteration + 1
    
print("The best position is ", gbest_position, "in iteration number ", iteration)